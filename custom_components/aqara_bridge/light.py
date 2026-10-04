import logging

import homeassistant.util.color as color_util
from homeassistant.components.light import ColorMode, LightEntity

from .core.aiot_manager import AiotManager, AiotToggleableEntityBase
from .core.const import DOMAIN, HASS_DATA_AIOT_MANAGER
from .core.utils import (
    light_convert_argb_to_rgb,
    light_convert_rgb_to_argb,
    light_convert_unit32_to_xy,
    light_convert_xy_to_uint32,
)

TYPE = "light"

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {"default": AiotLightEntity}
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotLightEntity(AiotToggleableEntityBase, LightEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotToggleableEntityBase.__init__(
            self, hass, device, res_params, TYPE, channel, **kwargs
        )
        self._attr_supported_color_modes = kwargs.get("supported_color_modes")
        self._attr_color_mode = kwargs.get("color_mode")
        self._attr_min_color_temp_kelvin = kwargs.get("min_color_temp_kelvin", 2703)
        self._attr_max_color_temp_kelvin = kwargs.get("max_color_temp_kelvin", 6500)
        self._extra_state_attributes.extend(
            [
                "trigger_time",
                "trigger_dt",
                # "supported_color_modes",
                # "color_mode",
                # "min_mireds",
                # "max_mireds",
            ]
        )

    async def async_turn_on(self, **kwargs):
        """Turn the specified light on."""
        xy_color = kwargs.get("xy_color")
        if xy_color:
            await self.async_set_resource("color", xy_color)

        rgb_color = kwargs.get("rgb_color")
        if rgb_color:
            await self.async_set_resource("color", rgb_color)

        # hs_color = kwargs.get("hs_color")
        # if hs_color:
        #     if self._attr_color_mode == ColorMode.HS:
        #         await self.async_set_resource("color", hs_color)
        #     elif self._attr_color_mode == ColorMode.XY:

        #         await self.async_set_resource("color", hs_color)

        brightness = kwargs.get("brightness")
        if brightness:
            await self.async_set_resource("brightness", brightness)

        color_temp = kwargs.get("color_temp")
        if color_temp:
            await self.async_set_resource("color_temp", color_temp)

        color_temp_kelvin = kwargs.get("color_temp_kelvin")
        if color_temp:
            await self.async_set_resource("color_temp_kelvin", color_temp_kelvin)

        await super().async_turn_on(**kwargs)

    def convert_attr_to_res(self, res_name, attr_value):
        if res_name == "brightness":
            # attr_value：0-255，亮度
            return int(attr_value * 100 / 255)
        elif res_name == "color" and self._attr_color_mode == ColorMode.HS:
            # attr_value：hs颜色
            rgb_color = color_util.color_hs_to_RGB(*attr_value)
            brightness = int(self.brightness * 100 / 255)
            r, g, b = rgb_color
            return int(f"{brightness:02x}{r:02x}{g:02x}{b:02x}", 16)
        elif res_name == "color" and self._attr_color_mode == ColorMode.XY:
            return light_convert_xy_to_uint32(attr_value[0], attr_value[1])
        elif res_name == "color" and self._attr_color_mode == ColorMode.RGB:
            return light_convert_rgb_to_argb(attr_value, 25)
        elif res_name == "color_temp":
            # attr_value：color temp
            return int(attr_value)
        elif res_name == "color_temp_kelvin":
            return int(1000000 / int(attr_value))
        return super().convert_attr_to_res(res_name, attr_value)

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "brightness":
            # res_value：0-100，亮度百分比
            return int(int(res_value) * 255 / 100)
        elif res_name == "color" and self._attr_color_mode == ColorMode.HS:
            # res_value：十进制整数字符串
            argb = hex(int(res_value))
            return color_util.color_RGB_to_hs(
                int(argb[4:6], 16), int(argb[6:8], 16), int(argb[8:10], 16)
            )
        elif res_name == "color" and self._attr_color_mode == ColorMode.XY:
            return light_convert_unit32_to_xy(int(res_value))
        elif res_name == "color" and self._attr_color_mode == ColorMode.RGB:
            return light_convert_argb_to_rgb(int(res_value))
        elif res_name == "color_temp":
            # res_value：153-500
            return int(res_value)
        elif res_name == "color_temp_kelvin":
            return int(1000000 / int(res_value))
        return super().convert_res_to_attr(res_name, res_value)
