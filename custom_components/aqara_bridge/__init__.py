import datetime
import logging
import re

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.event import async_track_time_interval

from .core.aiot_cloud import AiotCloud
from .core.aiot_manager import AiotManager
from .core.const import (
    CONF_ENTRY_APP_ID,
    CONF_ENTRY_APP_KEY,
    CONF_ENTRY_AUTH_ACCESS_TOKEN,
    CONF_ENTRY_AUTH_ACCOUNT,
    CONF_ENTRY_AUTH_ACCOUNT_TYPE,
    CONF_ENTRY_AUTH_COUNTRY_CODE,
    CONF_ENTRY_AUTH_EXPIRES_IN,
    CONF_ENTRY_AUTH_EXPIRES_TIME,
    CONF_ENTRY_AUTH_OPENID,
    CONF_ENTRY_AUTH_REFRESH_TOKEN,
    CONF_ENTRY_DEVICES,
    CONF_ENTRY_KEY_ID,
    DOMAIN,
    HASS_DATA_AIOT_MANAGER,
    HASS_DATA_AIOTCLOUD,
    HASS_DATA_AUTH_ENTRY_ID,
    HASS_DATA_RELOAD_KEYS,
)

_LOGGER = logging.getLogger(__name__)

_DEBUG_ACCESSTOKEN = ""
_DEBUG_REFRESHTOEEN = ""
_DEBUG_STATUS = False


def data_masking(s: str, n: int) -> str:
    return re.sub(f"(?<=.{{{n}}}).(?=.{{{n}}})", "*", str(s))


EXPIRES_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
# 令牌最长有效30天，剩余不足3天时主动刷新
TOKEN_REFRESH_MARGIN = datetime.timedelta(days=3)
TOKEN_CHECK_INTERVAL = datetime.timedelta(hours=12)
# 只有这些字段变化时不需要重载集成
TOKEN_FIELDS = (
    CONF_ENTRY_AUTH_OPENID,
    CONF_ENTRY_AUTH_ACCESS_TOKEN,
    CONF_ENTRY_AUTH_REFRESH_TOKEN,
    CONF_ENTRY_AUTH_EXPIRES_IN,
    CONF_ENTRY_AUTH_EXPIRES_TIME,
)


def apply_token_result(data: dict, token_result: dict) -> dict:
    """把获取/刷新令牌的结果合并到配置数据中"""
    data = {
        **data,
        CONF_ENTRY_AUTH_ACCESS_TOKEN: token_result["accessToken"],
        CONF_ENTRY_AUTH_REFRESH_TOKEN: token_result["refreshToken"],
        CONF_ENTRY_AUTH_EXPIRES_IN: token_result["expiresIn"],
        CONF_ENTRY_AUTH_EXPIRES_TIME: (
            datetime.datetime.now()
            + datetime.timedelta(seconds=int(token_result["expiresIn"]))
        ).strftime(EXPIRES_TIME_FORMAT),
    }
    if "openId" in token_result:
        data[CONF_ENTRY_AUTH_OPENID] = token_result["openId"]
    return data


def gen_auth_entry(
    app_id: str,
    app_key: str,
    key_id: str,
    account: str,
    account_type: int,
    country_code: str,
    token_result: dict,
):
    auth_entry = {
        CONF_ENTRY_APP_ID: app_id,
        CONF_ENTRY_APP_KEY: app_key,
        CONF_ENTRY_KEY_ID: key_id,
        CONF_ENTRY_AUTH_ACCOUNT: account,
        CONF_ENTRY_AUTH_ACCOUNT_TYPE: account_type,
        CONF_ENTRY_AUTH_COUNTRY_CODE: country_code,
    }
    return apply_token_result(auth_entry, token_result)


def reload_key(entry: ConfigEntry) -> tuple[dict, dict]:
    """除令牌外的配置，变化时才需要重载"""
    data = {k: v for k, v in entry.data.items() if k not in TOKEN_FIELDS}
    return data, dict(entry.options)


async def async_ensure_token_fresh(aiotcloud: AiotCloud, expires_time: str) -> bool:
    """令牌即将过期时刷新，返回当前是否有可用的令牌"""
    expires_at = datetime.datetime.strptime(expires_time, EXPIRES_TIME_FORMAT)
    now = datetime.datetime.now()
    if expires_at - now > TOKEN_REFRESH_MARGIN:
        return True
    resp = await aiotcloud.async_refresh_token(aiotcloud.refresh_token)
    if isinstance(resp, dict) and resp.get("code") == 0:
        # 新令牌已由 update_token_event_callback 写回配置
        return True
    # 刷新失败但令牌尚未过期，继续使用，下次检查再试
    return expires_at > now


def init_hass_data(hass):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(HASS_DATA_AUTH_ENTRY_ID, None)
    session = AiotCloud(aiohttp_client.async_create_clientsession(hass))
    if not hass.data[DOMAIN].get(HASS_DATA_AIOTCLOUD):
        hass.data[DOMAIN].setdefault(HASS_DATA_AIOTCLOUD, session)
    if not hass.data[DOMAIN].get(HASS_DATA_AIOT_MANAGER):
        hass.data[DOMAIN].setdefault(HASS_DATA_AIOT_MANAGER, AiotManager(hass, session))


async def async_setup(hass, config):
    """Setup component."""
    init_hass_data(hass)
    return True


async def async_setup_entry(hass, entry):
    @callback
    def token_updated(token_result: dict):
        hass.config_entries.async_update_entry(
            entry, data=apply_token_result(entry.data, token_result)
        )

    # add update handler
    if not entry.update_listeners:
        entry.add_update_listener(async_update_options)
    # 在可能刷新令牌之前记下，刷新令牌引起的配置更新不会触发重载
    reload_keys = hass.data[DOMAIN].setdefault(HASS_DATA_RELOAD_KEYS, {})
    reload_keys[entry.entry_id] = reload_key(entry)

    data = entry.data.copy()
    if _DEBUG_STATUS:
        import time

        data[CONF_ENTRY_AUTH_REFRESH_TOKEN] = _DEBUG_REFRESHTOEEN
        data[CONF_ENTRY_AUTH_ACCESS_TOKEN] = _DEBUG_ACCESSTOKEN
        data[CONF_ENTRY_AUTH_EXPIRES_TIME] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 24 * 3600)
        )

    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    aiotcloud: AiotCloud = hass.data[DOMAIN][HASS_DATA_AIOTCLOUD]
    aiotcloud.set_options(entry.options)
    aiotcloud.set_app_id(data[CONF_ENTRY_APP_ID])
    aiotcloud.set_app_key(data[CONF_ENTRY_APP_KEY])
    aiotcloud.set_key_id(data[CONF_ENTRY_KEY_ID])
    aiotcloud.update_token_event_callback = token_updated
    if manager._msg_handler is not None:
        # 如果重新配置，重新启动mq
        # Use async_stop() (bounded, off-loop) to avoid blocking the
        # event loop / hanging on librocketmq during reconfigure —
        # same failure mode that motivated the HA-stop listener below.
        await manager._msg_handler.async_stop()
    await manager.start_msg_hanlder(
        data[CONF_ENTRY_APP_ID], data[CONF_ENTRY_APP_KEY], data[CONF_ENTRY_KEY_ID]
    )

    # Ensure the RocketMQ consumer is shut down when HA stops.
    # Without this, the consumer's ~49 native worker threads outlive
    # HA's main exit path and block the Python interpreter indefinitely,
    # causing in-container restarts to hang forever and requiring a
    # `docker compose restart` to recover.
    async def _async_stop_consumer(event):
        if manager._msg_handler is not None:
            _LOGGER.info(
                "AqaraBridge: stopping RocketMQ consumer on HA shutdown"
            )
            await manager._msg_handler.async_stop()

    entry.async_on_unload(
        hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP, _async_stop_consumer
        )
    )
    aiotcloud.set_country(data.get(CONF_ENTRY_AUTH_COUNTRY_CODE))
    aiotcloud.access_token = data.get(CONF_ENTRY_AUTH_ACCESS_TOKEN)
    aiotcloud.refresh_token = data.get(CONF_ENTRY_AUTH_REFRESH_TOKEN)
    if not await async_ensure_token_fresh(
        aiotcloud, data[CONF_ENTRY_AUTH_EXPIRES_TIME]
    ):
        # TODO 这里需要处理刷新令牌失败的情况
        reload_keys.pop(entry.entry_id, None)
        return False

    # HA长时间运行时也定期检查，避免令牌过期后无法刷新
    async def _async_check_token(now):
        await async_ensure_token_fresh(
            aiotcloud, entry.data[CONF_ENTRY_AUTH_EXPIRES_TIME]
        )

    entry.async_on_unload(
        async_track_time_interval(hass, _async_check_token, TOKEN_CHECK_INTERVAL)
    )

    hass.data[DOMAIN][HASS_DATA_AUTH_ENTRY_ID] = entry

    # 移除不再接入的设备及其实体；按选项判断，接口查询失败时不会误删
    selected = entry.options.get(CONF_ENTRY_DEVICES)
    if selected:
        dev_reg = dr.async_get(hass)
        for device in dr.async_entries_for_config_entry(dev_reg, entry.entry_id):
            if not any(d == DOMAIN and i in selected for d, i in device.identifiers):
                dev_reg.async_update_device(
                    device.id, remove_config_entry_id=entry.entry_id
                )

    await manager.async_add_all_devices(entry)
    await manager.async_forward_entry_setup(entry)

    return True


async def async_unload_entry(hass, entry):
    hass.data[DOMAIN].get(HASS_DATA_RELOAD_KEYS, {}).pop(entry.entry_id, None)
    hass.data[DOMAIN][HASS_DATA_AIOTCLOUD].update_token_event_callback = None
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    unload_ok = await manager.async_unload_entry(entry)
    if manager._msg_handler is not None:
        await manager._msg_handler.async_stop()
        manager._msg_handler = None
    return unload_ok


async def async_remove_entry(hass, entry):
    if CONF_ENTRY_AUTH_ACCOUNT in entry.data:
        hass.data[DOMAIN][HASS_DATA_AUTH_ENTRY_ID] = None
    else:
        manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
        await manager.async_remove_entry(entry)
    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry):
    """Update Optioins if available"""
    reload_keys = hass.data[DOMAIN].get(HASS_DATA_RELOAD_KEYS, {})
    if entry.state in (
        ConfigEntryState.LOADED,
        ConfigEntryState.SETUP_IN_PROGRESS,
    ) and reload_keys.get(entry.entry_id) == reload_key(entry):
        # 只有令牌变了（刷新或重新授权），同步到会话即可，不重载
        aiotcloud: AiotCloud = hass.data[DOMAIN][HASS_DATA_AIOTCLOUD]
        aiotcloud.access_token = entry.data.get(CONF_ENTRY_AUTH_ACCESS_TOKEN)
        aiotcloud.refresh_token = entry.data.get(CONF_ENTRY_AUTH_REFRESH_TOKEN)
        return
    await hass.config_entries.async_reload(entry.entry_id)


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device_entry
) -> bool:
    """Remove a config entry from a device."""
    return True
