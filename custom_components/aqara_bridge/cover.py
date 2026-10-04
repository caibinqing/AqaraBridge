import logging

from homeassistant.components.cover import CoverEntity

from .core.aiot_manager import (
    AiotEntityBase,
    AiotManager,
)
from .core.const import DOMAIN, HASS_DATA_AIOT_MANAGER

TYPE = "cover"

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {"default": AiotCoverEntity, "airer": AiotAirerEntity}
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotCoverEntity(AiotEntityBase, CoverEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        # self._attr_is_closed = kwargs.get("is_closed")

    async def async_open_cover(self, **kwargs):
        await self.async_set_resource("is_closed", False)

    async def async_close_cover(self, **kwargs):
        await self.async_set_resource("is_closed", True)

    async def async_set_cover_position(self, **kwargs):
        pos = kwargs.get("position")
        await self.async_set_resource("current_cover_position", pos)

    async def async_stop_cover(self, **kwargs):
        await self.async_set_res_value("is_closed", 2)
        self._attr_is_closed = False
        self._attr_is_closing = False
        self._attr_is_opening = False
        self.schedule_update_ha_state()

    def convert_attr_to_res(self, res_name, attr_value):
        if res_name == "is_closed":
            if attr_value:
                return 0
            return 1

        return super().convert_attr_to_res(res_name, attr_value)

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "is_closed":
            if int(res_value) == 1:
                return False
            elif int(res_value) == 0:
                return True

        if res_name == "running_status":
            if int(res_value) == 0:
                self._attr_is_closing = True
            elif int(res_value) == 1:
                self._attr_is_opening = True
            elif int(res_value) == 2:
                self._attr_is_closing = False
                self._attr_is_opening = False
            self.schedule_update_ha_state()

        if res_name == "current_cover_position":
            if int(res_value) == 0:
                self._attr_is_closing = False
                self._attr_is_opening = False
                self._attr_is_closed = True
            elif int(res_value) > 0:
                self._attr_is_closing = False
                self._attr_is_opening = False
                self._attr_is_closed = False
            self.schedule_update_ha_state()
            return res_value
        return super().convert_res_to_attr(res_name, res_value)


class AiotAirerEntity(AiotEntityBase, CoverEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        # self._attr_is_closed = kwargs.get("is_closed")

    async def async_open_cover(self, **kwargs):
        if self.device.model == "lumi.airer.acn02":
            await self.async_set_resource("current_cover_position", 100)
        await self.async_set_resource("is_closed", False)

    async def async_close_cover(self, **kwargs):
        if self.device.model == "lumi.airer.acn02":
            await self.async_set_resource("current_cover_position", 0)
        await self.async_set_resource("is_closed", True)

    async def async_set_cover_position(self, **kwargs):
        pos = kwargs.get("position")
        await self.async_set_resource("current_cover_position", pos)

    async def async_stop_cover(self, **kwargs):
        await self.async_set_res_value("is_closed", 0)
        self.schedule_update_ha_state()

    def convert_attr_to_res(self, res_name, attr_value):
        if res_name == "is_closed" and self.device.model == "lumi.airer.acn001":
            if attr_value:
                return 1
            return 2
        if res_name == "is_closed" and self.device.model == "lumi.airer.acn02":
            if attr_value:
                return 2
            return 1

        return super().convert_attr_to_res(res_name, attr_value)

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "is_closed" and self.device.model == "lumi.airer.acn001":
            if int(res_value) == 1:
                return True
            if int(res_value) == 2:
                return False
        if res_name == "is_closed" and self.device.model == "lumi.airer.acn02":
            if int(res_value) == 2:
                return True
            if int(res_value) == 1:
                return False

        if (
            res_name == "current_cover_position"
            and self.device.model == "lumi.airer.acn02"
        ):
            if int(res_value) == 0:
                self._attr_is_closed = True
            elif int(res_value) > 0:
                self._attr_is_closed = False
            self.schedule_update_ha_state()
            return res_value
        return super().convert_res_to_attr(res_name, res_value)
