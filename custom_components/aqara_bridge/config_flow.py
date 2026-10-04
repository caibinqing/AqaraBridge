import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import (
    CONN_CLASS_LOCAL_PUSH,
    ConfigFlow,
    OptionsFlow,
    ConfigEntry,
)
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import init_hass_data, data_masking, gen_auth_entry
from .core.aiot_cloud import AiotCloud
from .core.aiot_manager import AiotDevice
from .core.const import *

_LOGGER = logging.getLogger(__name__)

DEVICE_GET_TOKEN_CONFIG = vol.Schema({vol.Required(CONF_FIELD_AUTH_CODE): str})


async def async_query_supported_devices(session) -> dict[str, str]:
    """查询账号下插件支持的设备，返回 {did: 显示名称}"""
    results = await session.async_query_all_devices_info()
    return {
        x["did"]: f"{x.get('deviceName')} ({x.get('model')})"
        for x in results
        if AiotDevice(**x).is_supported
    }


def select_devices_schema(devices: dict[str, str], default=vol.UNDEFINED):
    return vol.Schema(
        {
            vol.Required(CONF_FIELD_SELECTED_DEVICES, default=default): (
                cv.multi_select(devices)
            )
        }
    )


class AqaraBridgeFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle an Aqara Bridge config flow."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self.account = None
        self.country_code = None
        self.account_type = None
        self.app_id = None
        self.app_key = None
        self.key_id = None
        self._session = None
        self._device_manager = None
        self._auth_entry = None
        self._devices = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """get option flow"""
        return OptionsFlowHandler()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        init_hass_data(self.hass)
        self._device_manager = self.hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
        auth_entry_id = self.hass.data[DOMAIN][HASS_DATA_AUTH_ENTRY_ID]
        self._session = self.hass.data[DOMAIN][HASS_DATA_AIOTCLOUD]
        return await self.async_step_get_auth_code()

    async def async_step_get_auth_code(self, user_input=None):
        """Configure an aqara device through the Aqara Cloud."""
        errors = {}
        if user_input:
            self.account = user_input.get(CONF_FIELD_ACCOUNT)
            self.country_code = user_input.get(CONF_FIELD_COUNTRY_CODE)
            self.app_id = user_input.get(CONF_FIELD_APP_ID)
            self.app_key = user_input.get(CONF_FIELD_APP_KEY)
            self.key_id = user_input.get(CONF_FIELD_KEY_ID)
            self.account_type = 0
            self._session.set_country(self.country_code)
            self._session.set_app_id(self.app_id)
            self._session.set_app_key(self.app_key)
            self._session.set_key_id(self.key_id)

            refresh_token = user_input.get(CONF_FIELD_REFRESH_TOKEN)
            if refresh_token and refresh_token != "":
                resp = await self._session.async_refresh_token(refresh_token)
                if resp and resp["code"] == 0:
                    self._auth_entry = gen_auth_entry(
                        self.app_id,
                        self.app_key,
                        self.key_id,
                        self.account,
                        self.account_type,
                        self.country_code,
                        resp["result"],
                    )
                    return await self.async_step_select_devices()
                else:
                    errors["base"] = "refresh_token_error"
            else:
                resp = await self._session.async_get_auth_code(self.account, 0)
                if resp and resp["code"] == 0:
                    return await self.async_step_get_token()
                else:
                    errors["base"] = "auth_code_error"
        def_account = (
            user_input.get(CONF_FIELD_ACCOUNT)
            if user_input and user_input.get(CONF_FIELD_ACCOUNT)
            else ""
        )
        def_country_code = (
            user_input.get(CONF_FIELD_COUNTRY_CODE)
            if user_input and user_input.get(CONF_FIELD_COUNTRY_CODE)
            else SERVER_COUNTRY_CODES_DEFAULT
        )
        def_app_id = (
            user_input.get(CONF_FIELD_APP_ID)
            if user_input and user_input.get(CONF_FIELD_APP_ID)
            else DEFAULT_CLOUD_APP_ID
        )
        def_app_key = (
            user_input.get(CONF_FIELD_APP_KEY)
            if user_input and user_input.get(CONF_FIELD_APP_KEY)
            else DEFAULT_CLOUD_APP_KEY
        )
        def_key_id = (
            user_input.get(CONF_FIELD_KEY_ID)
            if user_input and user_input.get(CONF_FIELD_KEY_ID)
            else DEFAULT_CLOUD_KEY_ID
        )

        config_scheme = vol.Schema(
            {
                vol.Required(CONF_FIELD_ACCOUNT, default=def_account): str,
                vol.Required(CONF_FIELD_COUNTRY_CODE, default=def_country_code): vol.In(
                    SERVER_COUNTRY_CODES
                ),
                vol.Required(CONF_FIELD_APP_ID, default=def_app_id): str,
                vol.Required(CONF_FIELD_APP_KEY, default=def_app_key): str,
                vol.Required(CONF_FIELD_KEY_ID, default=def_key_id): str,
                vol.Optional(CONF_FIELD_REFRESH_TOKEN): str,
            }
        )
        return self.async_show_form(
            step_id="get_auth_code",
            data_schema=config_scheme,
            errors=errors,
        )

    async def async_step_get_token(self, user_input=None):
        errors = {}
        if user_input and CONF_FIELD_AUTH_CODE in user_input:
            auth_code = user_input.get(CONF_FIELD_AUTH_CODE)
            resp = await self._session.async_get_token(auth_code, self.account, 0)
            if resp and resp["code"] == 0:
                self._auth_entry = gen_auth_entry(
                    self.app_id,
                    self.app_key,
                    self.key_id,
                    self.account,
                    self.account_type,
                    self.country_code,
                    resp["result"],
                )
                return await self.async_step_select_devices()
            errors["base"] = "get_auth_code_error"

        return self.async_show_form(
            step_id="get_token", data_schema=DEVICE_GET_TOKEN_CONFIG, errors=errors
        )

    async def async_step_select_devices(self, user_input=None):
        """选择要接入的设备，未选中的设备不查询、不订阅"""
        errors = {}
        if user_input is not None:
            selected = user_input.get(CONF_FIELD_SELECTED_DEVICES, [])
            if selected:
                return self.async_create_entry(
                    title=data_masking(self._auth_entry[CONF_ENTRY_AUTH_ACCOUNT], 4),
                    data=self._auth_entry,
                    options={CONF_ENTRY_DEVICES: selected},
                )
            errors["base"] = "no_device_selected"

        if self._devices is None:
            self._devices = await async_query_supported_devices(self._session)

        return self.async_show_form(
            step_id="select_devices",
            data_schema=select_devices_schema(self._devices),
            errors=errors,
        )


class OptionsFlowHandler(OptionsFlow):
    def __init__(self) -> None:
        """Initialize options flow."""
        self.account = None
        self.country_code = None
        self.account_type = 0
        self._session = None
        self._devices = None

    async def async_step_init(self, user_input=None):
        return self.async_show_menu(
            step_id="init", menu_options=["select_devices", "auth"]
        )

    async def async_step_select_devices(self, user_input=None):
        """重新选择接入的设备"""
        errors = {}
        manager = self.hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
        # 旧配置没有设备选项，此时接入的是所有支持的设备
        current = (
            self.config_entry.options.get(CONF_ENTRY_DEVICES)
            or manager.managed_device_ids
        )
        if user_input is not None:
            selected = user_input.get(CONF_FIELD_SELECTED_DEVICES, [])
            if selected:
                await manager.async_unsubscribe_devices(
                    [x for x in current if x not in selected]
                )
                return self.async_create_entry(
                    title="",
                    data={**self.config_entry.options, CONF_ENTRY_DEVICES: selected},
                )
            errors["base"] = "no_device_selected"

        if self._devices is None:
            self._devices = await async_query_supported_devices(
                self.hass.data[DOMAIN][HASS_DATA_AIOTCLOUD]
            )

        return self.async_show_form(
            step_id="select_devices",
            data_schema=select_devices_schema(
                self._devices, [x for x in current if x in self._devices]
            ),
            errors=errors,
        )

    async def async_step_auth(self, user_input=None):
        """Configure an aqara device through the Aqara Cloud."""
        errors = {}
        if isinstance(user_input, dict):
            # 用户输入
            self.account = user_input.get(CONF_FIELD_ACCOUNT)
            self.country_code = user_input.get(CONF_FIELD_COUNTRY_CODE)
            if self._session is None:
                # 用独立会话，填错或中途放弃不影响运行中的集成；授权成功后会重载
                self._session = AiotCloud(async_get_clientsession(self.hass))
            self._session.set_country(self.country_code)
            self._session.set_app_id(user_input.get(CONF_FIELD_APP_ID))
            self._session.set_app_key(user_input.get(CONF_FIELD_APP_KEY))
            self._session.set_key_id(user_input.get(CONF_FIELD_KEY_ID))

            refresh_token = user_input.get(CONF_FIELD_REFRESH_TOKEN)
            if refresh_token and refresh_token != "":
                # 更新了token值
                resp = await self._session.async_refresh_token(refresh_token)
                if resp and resp["code"] == 0:
                    auth_entry = gen_auth_entry(
                        self._session.get_app_id(),
                        self._session.get_app_key(),
                        self._session.get_key_id(),
                        self.account,
                        self.account_type,
                        self.country_code,
                        resp["result"],
                    )
                    self.hass.config_entries.async_update_entry(
                        self.config_entry, data=auth_entry
                    )
                    return self.async_abort(reason="complete")
                else:
                    errors["base"] = "refresh_token_error"
            else:
                resp = await self._session.async_get_auth_code(self.account, 0)
                if resp and resp["code"] == 0:
                    return await self.async_step_option_get_token()
                else:
                    errors["base"] = "auth_code_error"

        prev_input = {
            **self.config_entry.data,
            **self.config_entry.options,
        }
        defaults = {
            CONF_FIELD_ACCOUNT: prev_input.get(CONF_ENTRY_AUTH_ACCOUNT),
            CONF_FIELD_COUNTRY_CODE: prev_input.get(
                CONF_ENTRY_AUTH_COUNTRY_CODE, SERVER_COUNTRY_CODES_DEFAULT
            ),
            CONF_FIELD_APP_ID: prev_input.get(CONF_ENTRY_APP_ID),
            CONF_FIELD_APP_KEY: prev_input.get(CONF_ENTRY_APP_KEY),
            CONF_FIELD_KEY_ID: prev_input.get(CONF_ENTRY_KEY_ID),
        }
        # 出错重新显示表单时，保留刚才填写的内容
        if user_input:
            defaults.update(
                {k: v for k, v in user_input.items() if k != CONF_FIELD_REFRESH_TOKEN}
            )

        def default(key):
            return defaults.get(key) or vol.UNDEFINED

        config_scheme = vol.Schema(
            {
                vol.Required(
                    CONF_FIELD_ACCOUNT, default=default(CONF_FIELD_ACCOUNT)
                ): str,
                vol.Required(
                    CONF_FIELD_COUNTRY_CODE, default=default(CONF_FIELD_COUNTRY_CODE)
                ): vol.In(SERVER_COUNTRY_CODES),
                vol.Optional(
                    CONF_FIELD_APP_ID, default=default(CONF_FIELD_APP_ID)
                ): str,
                vol.Optional(
                    CONF_FIELD_APP_KEY, default=default(CONF_FIELD_APP_KEY)
                ): str,
                vol.Optional(
                    CONF_FIELD_KEY_ID, default=default(CONF_FIELD_KEY_ID)
                ): str,
                vol.Optional(CONF_FIELD_REFRESH_TOKEN): str,
            }
        )
        return self.async_show_form(
            step_id="auth", data_schema=config_scheme, errors=errors
        )

    async def async_step_option_get_token(self, user_input=None):
        errors = {}
        if user_input and CONF_FIELD_AUTH_CODE in user_input:
            auth_code = user_input.get(CONF_FIELD_AUTH_CODE)
            resp = await self._session.async_get_token(auth_code, self.account, 0)
            if resp and resp["code"] == 0:
                auth_entry = gen_auth_entry(
                    self._session.get_app_id(),
                    self._session.get_app_key(),
                    self._session.get_key_id(),
                    self.account,
                    self.account_type,
                    self.country_code,
                    resp["result"],
                )
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=auth_entry
                )
                return self.async_abort(reason="complete")
            else:
                errors["base"] = "auth_code_error"
        return self.async_show_form(
            step_id="option_get_token",
            data_schema=DEVICE_GET_TOKEN_CONFIG,
            errors=errors,
        )
