from homeassistant.components.switch import SwitchEntity

from .core.aiot_manager import AiotManager, AiotToggleableEntityBase
from .core.const import DOMAIN, HASS_DATA_AIOT_MANAGER

TYPE = "switch"

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {"default": AiotSwitchEntity, "wall_switch": AiotWallSwitchEntity}
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotSwitchEntity(AiotToggleableEntityBase, SwitchEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotToggleableEntityBase.__init__(
            self, hass, device, res_params, TYPE, channel, **kwargs
        )
        self._extra_state_attributes.extend([])

    @property
    def icon(self):
        """return icon."""
        return "mdi:power-socket"

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "toggle" or res_name == "decoupled":
            return res_value == "1"
        if res_name == "energy":
            return round(float(res_value) / 1000.0, 3)
        if res_name == "firmware_version":
            return res_value
        if res_name == "zigbee_lqi":
            return int(res_value)
        if res_name == "in_use":
            return res_value == "1"
        return super().convert_res_to_attr(res_name, res_value)


class AiotWallSwitchEntity(AiotToggleableEntityBase, SwitchEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotToggleableEntityBase.__init__(
            self, hass, device, res_params, TYPE, channel, **kwargs
        )
        self._extra_state_attributes.extend(["trigger_time", "trigger_dt"])

    @property
    def icon(self):
        """return icon."""
        return "mdi:light-switch"

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "toggle" or res_name == "decoupled":
            return res_value == "1"
        if res_name == "energy":
            return round(float(res_value) / 1000.0, 3)
        if res_name == "firmware_version":
            return res_value
        if res_name == "zigbee_lqi":
            return int(res_value)
        return super().convert_res_to_attr(res_name, res_value)
