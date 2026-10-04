import logging
import re

from homeassistant.components.climate import (
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    PRESET_BOOST,
    PRESET_NONE,
    SWING_OFF,
    SWING_ON,
    ClimateEntity,
    HVACMode,
)

from .core.aiot_manager import (
    AiotEntityBase,
    AiotManager,
)
from .core.const import DOMAIN, HASS_DATA_AIOT_MANAGER

TYPE = "climate"

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{TYPE}.{DOMAIN}"

AC_STATE_RES_ATTR_MAPPING = {
    "hvac_mode": {
        "0": HVACMode.HEAT,
        "1": HVACMode.COOL,
        "2": HVACMode.AUTO,
        "3": HVACMode.DRY,
        "4": HVACMode.FAN_ONLY,
    },
    "fan_mode": {"0": FAN_LOW, "1": FAN_MEDIUM, "2": FAN_HIGH, "3": FAN_AUTO},
    "swing_mode": {"0": SWING_ON, "1": SWING_OFF},
}

AC_STATE_ATTR_RES_MAPPING = {
    "hvac_mode": {
        HVACMode.HEAT: "0",
        HVACMode.COOL: "1",
        HVACMode.AUTO: "2",
        HVACMode.DRY: "3",
        HVACMode.FAN_ONLY: "4",
    },
    "fan_mode": {
        FAN_LOW: "0",
        FAN_MEDIUM: "1",
        FAN_HIGH: "2",
        FAN_AUTO: "3",
    },
    "swing_mode": {SWING_ON: "0", SWING_OFF: "1"},
}


P3_MODE_RES_ATTR_MAPPING = {
    "0": HVACMode.COOL,
    "1": HVACMode.HEAT,
    "2": HVACMode.AUTO,
    "3": HVACMode.FAN_ONLY,
    "4": HVACMode.DRY,
}

P3_MODE_ATTR_RES_MAPPING = {
    HVACMode.COOL: "0",
    HVACMode.HEAT: "1",
    HVACMode.AUTO: "2",
    HVACMode.FAN_ONLY: "3",
    HVACMode.DRY: "4",
}

P3_FAN_RES_ATTR_MAPPING = {
    "0": FAN_AUTO,
    "1": FAN_LOW,
    "2": FAN_MEDIUM,
    "3": FAN_HIGH,
}

P3_FAN_ATTR_RES_MAPPING = {
    FAN_AUTO: "0",
    FAN_LOW: "1",
    FAN_MEDIUM: "2",
    FAN_HIGH: "3",
}

T1_MODE_RES_ATTR_MAPPING = {
    "0": HVACMode.AUTO,
    "1": HVACMode.COOL,
    "2": HVACMode.DRY,
    "3": HVACMode.FAN_ONLY,
    "4": HVACMode.HEAT,
}

T1_MODE_ATTR_RES_MAPPING = {
    HVACMode.AUTO: "0",
    HVACMode.COOL: "1",
    HVACMode.DRY: "2",
    HVACMode.FAN_ONLY: "3",
    HVACMode.HEAT: "4",
}

S3_MODE_RES_ATTR_MAPPING = {
    "0": HVACMode.HEAT,
    "1": HVACMode.COOL,
    "4": HVACMode.FAN_ONLY,
}

S3_MODE_ATTR_RES_MAPPING = {
    HVACMode.HEAT: "0",
    HVACMode.COOL: "1",
    HVACMode.FAN_ONLY: "4",
}

S3_FAN_RES_ATTR_MAPPING = {
    "0": FAN_LOW,
    "1": FAN_MEDIUM,
    "2": FAN_HIGH,
    "3": FAN_AUTO,
}

S3_FAN_ATTR_RES_MAPPING = {
    FAN_LOW: "0",
    FAN_MEDIUM: "1",
    FAN_HIGH: "2",
    FAN_AUTO: "3",
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "airrtc_agl001": AiotAirrtcAgl001Entity,
        "airrtc_pcacn2": AiotAirrtcPcacn2Entity,
        "airrtc_acn02": AiotAirrtcAcn02Entity,
        "ac_partner_p3": AiotACPartnerP3Entity,
        "airrtc_tcpecn02": AiotAirrtcTcpecn02Entity,
        "airrtc_vrfegl01": AiotAirrtcVrfegl01Entity,
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotAirrtcAgl001Entity(AiotEntityBase, ClimateEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_temperature_unit = kwargs.get("temperature_unit")
        self._attr_hvac_modes = kwargs.get("hvac_modes")
        self._attr_target_temperature_step = kwargs.get("target_temperature_step")

        self._attr_max_temp = kwargs.get("max_temp")
        self._attr_min_temp = kwargs.get("min_temp")
        self._attr_target_temperature_high = kwargs.get("max_temp")
        self._attr_target_temperature_low = kwargs.get("min_temp")

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "ac_on_off":
            if res_value == "0":
                self._attr_hvac_mode = HVACMode.OFF
            if res_value == "1":
                self._attr_hvac_mode = HVACMode.HEAT
        if res_name == "ac_mode":
            if res_value == "0":
                self._attr_hvac_mode = HVACMode.HEAT
        if res_name == "ac_temperature":
            self._attr_target_temperature = float(res_value) / 100
        if res_name == "env_temperature":
            self._attr_current_temperature = float(res_value) / 100
        self.schedule_update_ha_state()
        return super().convert_res_to_attr(res_name, res_value)

    async def async_set_hvac_mode(self, hvac_mode):
        if hvac_mode == HVACMode.OFF:
            await self.async_set_res_value("ac_on_off", "0")
        if hvac_mode == HVACMode.HEAT:
            await self.async_set_res_value("ac_mode", "0")
            await self.async_set_res_value("ac_on_off", "1")
        self._attr_hvac_mode = hvac_mode
        self.schedule_update_ha_state()

    async def async_set_temperature(self, **kwargs):
        temp = kwargs.get("temperature")
        await self.async_set_res_value("ac_temperature", str(int(temp * 100)))
        self._attr_target_temperature = temp
        self.schedule_update_ha_state()


class AiotAirrtcPcacn2Entity(AiotEntityBase, ClimateEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._extra_state_attributes.extend(["last_ac_mode"])
        self._attr_temperature_unit = kwargs.get("temperature_unit")
        self._attr_hvac_modes = kwargs.get("hvac_modes")
        self._attr_fan_modes = kwargs.get("fan_modes")
        self._attr_target_temperature_step = kwargs.get("target_temperature_step")

        self._attr_max_temp = kwargs.get("max_temp")
        self._attr_min_temp = kwargs.get("min_temp")
        self._attr_target_temperature_high = kwargs.get("max_temp")
        self._attr_target_temperature_low = kwargs.get("min_temp")

        self._attr_last_ac_mode = None

    @property
    def last_ac_mode(self):
        return self._attr_last_ac_mode

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "ac_on_off":
            if res_value == "0":
                self._attr_hvac_mode = HVACMode.OFF
            if res_value == "1":
                self._attr_hvac_mode = self._attr_last_ac_mode
        if res_name == "ac_mode":
            self._attr_hvac_mode = S3_MODE_RES_ATTR_MAPPING.get(res_value)
            self._attr_last_ac_mode = S3_MODE_RES_ATTR_MAPPING.get(res_value)
        if res_name == "ac_fan_mode":
            self._attr_fan_mode = S3_FAN_RES_ATTR_MAPPING.get(res_value)
        if res_name == "ac_temperature":
            self._attr_target_temperature = float(res_value) / 100
        if res_name == "env_temperature":
            self._attr_current_temperature = float(res_value) / 100
        if res_name == "env_humidity":
            self._attr_current_humidity = float(res_value) / 100
        self.schedule_update_ha_state()
        return super().convert_res_to_attr(res_name, res_value)

    async def async_set_hvac_mode(self, hvac_mode):
        if hvac_mode == HVACMode.OFF:
            await self.async_set_res_value("ac_on_off", "0")
        else:
            await self.async_set_res_value(
                "ac_mode", S3_MODE_ATTR_RES_MAPPING.get(hvac_mode)
            )
            if self._attr_hvac_mode == HVACMode.OFF:
                await self.async_set_res_value("ac_on_off", "1")
        self._attr_hvac_mode = hvac_mode
        self.schedule_update_ha_state()

    async def async_set_temperature(self, **kwargs):
        temp = kwargs.get("temperature")
        await self.async_set_res_value("ac_temperature", str(int(temp * 100)))
        self._attr_target_temperature = temp
        self.schedule_update_ha_state()

    async def async_set_fan_mode(self, fan_mode):
        await self.async_set_res_value(
            "ac_fan_mode", S3_FAN_ATTR_RES_MAPPING.get(fan_mode)
        )
        self._attr_fan_mode = fan_mode
        self.schedule_update_ha_state()


class AiotAirrtcAcn02Entity(AiotEntityBase, ClimateEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._extra_state_attributes.extend(["last_ac_mode"])
        self._attr_temperature_unit = kwargs.get("temperature_unit")
        self._attr_hvac_modes = kwargs.get("hvac_modes")
        self._attr_fan_modes = kwargs.get("fan_modes")
        self._attr_target_temperature_step = kwargs.get("target_temperature_step")

        self._attr_max_temp = kwargs.get("max_temp")
        self._attr_min_temp = kwargs.get("min_temp")
        self._attr_target_temperature_high = kwargs.get("max_temp")
        self._attr_target_temperature_low = kwargs.get("min_temp")

        self._attr_last_ac_mode = None

    @property
    def last_ac_mode(self):
        return self._attr_last_ac_mode

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "ac_on_off":
            if res_value == "0":
                self._attr_hvac_mode = HVACMode.OFF
            if res_value == "1":
                self._attr_hvac_mode = self._attr_last_ac_mode
        if res_name == "ac_mode":
            self._attr_hvac_mode = T1_MODE_RES_ATTR_MAPPING.get(res_value)
            self._attr_last_ac_mode = T1_MODE_RES_ATTR_MAPPING.get(res_value)
        if res_name == "ac_fan_mode":
            self._attr_fan_mode = P3_FAN_RES_ATTR_MAPPING.get(res_value)
        if res_name == "ac_temperature":
            self._attr_target_temperature = int(float(res_value)) / 100
        if res_name == "env_temperature":
            self._attr_current_temperature = int(float(res_value)) / 100
        self.schedule_update_ha_state()
        return super().convert_res_to_attr(res_name, res_value)

    async def async_set_hvac_mode(self, hvac_mode):
        if hvac_mode == HVACMode.OFF:
            await self.async_set_res_value("ac_on_off", "0")
        else:
            await self.async_set_res_value(
                "ac_mode", T1_MODE_ATTR_RES_MAPPING.get(hvac_mode)
            )
            if self._attr_hvac_mode == HVACMode.OFF:
                await self.async_set_res_value("ac_on_off", "1")
        self._attr_hvac_mode = hvac_mode
        self.schedule_update_ha_state()

    async def async_set_temperature(self, **kwargs):
        temp = kwargs.get("temperature")
        await self.async_set_res_value("ac_temperature", str(int(temp * 100)))
        self._attr_target_temperature = temp
        self.schedule_update_ha_state()

    async def async_set_fan_mode(self, fan_mode):
        await self.async_set_res_value(
            "ac_fan_mode", P3_FAN_ATTR_RES_MAPPING.get(fan_mode)
        )
        self._attr_fan_mode = fan_mode
        self.schedule_update_ha_state()


class AiotAirrtcVrfegl01Entity(AiotEntityBase, ClimateEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_temperature_unit = kwargs.get("temperature_unit")
        self._attr_hvac_modes = kwargs.get("hvac_modes")
        self._attr_fan_modes = kwargs.get("fan_modes")
        self._attr_swing_modes = kwargs.get("swing_modes")
        self._attr_target_temperature_step = kwargs.get("target_temperature_step")

        self._attr_max_temp = kwargs.get("max_temp")
        self._attr_min_temp = kwargs.get("min_temp")
        self._attr_target_temperature_high = kwargs.get("max_temp")
        self._attr_target_temperature_low = kwargs.get("min_temp")

        self.airrtc_vrfegl01_bin_cache = {"swing_direction": {}, "other": {}}

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "ac_state":
            # res_value: 十进制字符串
            ac_state_bin = bin(int(res_value))[2:].zfill(32)
            self.ac_state_to_attr(ac_state_bin)

    def ac_state_to_attr(self, bin):
        """空调状态转HA属性."""
        power = int(bin[0:4], 2)
        mode = int(bin[4:8], 2)
        fan = int(bin[8:12], 2)
        swing_direction = int(bin[12:14], 2)
        swing = int(bin[14:16], 2)
        temp = int(bin[16:24], 2)
        other = int(bin[24:32], 2)
        # 暂存不需要的属性以便写回云端
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", self.get_res_id_by_name("ac_state"))
        if match:
            channel_id = match.group(2)
        self.airrtc_vrfegl01_bin_cache["swing_direction"][channel_id] = swing_direction
        self.airrtc_vrfegl01_bin_cache["other"][channel_id] = other

        if power == 0:
            self._attr_hvac_mode = HVACMode.OFF
        elif power == 1:
            self._attr_hvac_mode = AC_STATE_RES_ATTR_MAPPING["hvac_mode"].get(
                str(mode), HVACMode.AUTO
            )

        if temp:
            self._attr_target_temperature = float(temp)

        self._attr_fan_mode = AC_STATE_RES_ATTR_MAPPING["fan_mode"].get(
            str(fan), FAN_AUTO
        )

        self._attr_swing_mode = AC_STATE_RES_ATTR_MAPPING["swing_mode"].get(
            str(swing), SWING_OFF
        )

        self.schedule_update_ha_state()

    def attr_to_ac_state(self, attr, value):
        """HA属性 转 ac_state."""
        power = 0 if self._attr_hvac_mode == HVACMode.OFF else 1
        mode = AC_STATE_ATTR_RES_MAPPING["hvac_mode"].get(self._attr_hvac_mode, "2")
        temp = int(self._attr_target_temperature)
        fan = AC_STATE_ATTR_RES_MAPPING["fan_mode"].get(self._attr_fan_mode, "3")
        swing = AC_STATE_ATTR_RES_MAPPING["swing_mode"].get(self._attr_swing_mode, "1")

        if attr == "hvac_mode":
            old_mode = self._attr_hvac_mode
            if value == HVACMode.OFF:
                power = 0
                mode = AC_STATE_ATTR_RES_MAPPING["hvac_mode"].get(
                    old_mode, HVACMode.AUTO
                )
            else:
                power = 1
                mode = AC_STATE_ATTR_RES_MAPPING["hvac_mode"].get(value, HVACMode.AUTO)
            self._attr_hvac_mode = value

        if attr == "target_temperature":
            self._attr_target_temperature = value
            temp = int(value)

        if attr == "fan_mode":
            self._attr_fan_mode = value
            fan = AC_STATE_ATTR_RES_MAPPING["fan_mode"].get(value, FAN_AUTO)

        if attr == "swing_mode":
            self._attr_swing_mode = value
            swing = AC_STATE_ATTR_RES_MAPPING["swing_mode"].get(value, SWING_OFF)

        self.schedule_update_ha_state()

        match = re.search(r"(\d+)\.(\d+)\.(\d+)", self.get_res_id_by_name("ac_state"))
        if match:
            channel_id = match.group(2)

        power_bin = bin(power)[2:].zfill(4)
        mode_bin = bin(int(mode))[2:].zfill(4)
        fan_bin = bin(int(fan))[2:].zfill(4)
        swing_direction_bin = bin(
            self.airrtc_vrfegl01_bin_cache["swing_direction"][channel_id]
        )[2:].zfill(2)
        swing_bin = bin(int(swing))[2:].zfill(2)
        temp_bin = bin(temp)[2:].zfill(8)
        other_bin = bin(self.airrtc_vrfegl01_bin_cache["other"][channel_id])[2:].zfill(
            8
        )

        bin_str = f"{power_bin}{mode_bin}{fan_bin}{swing_direction_bin}{swing_bin}{temp_bin}{other_bin}"
        return int(bin_str, 2)

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        result = self.attr_to_ac_state("hvac_mode", hvac_mode)
        await self.async_set_res_value("ac_state", result)

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temp = kwargs.get("temperature")
        result = self.attr_to_ac_state("target_temperature", temp)
        await self.async_set_res_value("ac_state", result)

    async def async_set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        result = self.attr_to_ac_state("fan_mode", fan_mode)
        await self.async_set_res_value("ac_state", result)

    async def async_set_swing_mode(self, swing_mode):
        """Set new target swing operation."""
        result = self.attr_to_ac_state("swing_mode", swing_mode)
        await self.async_set_res_value("ac_state", result)


class AiotAirrtcTcpecn02Entity(AiotEntityBase, ClimateEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_temperature_unit = kwargs.get("temperature_unit")
        self._attr_hvac_modes = kwargs.get("hvac_modes")
        self._attr_fan_modes = kwargs.get("fan_modes")
        self._attr_swing_modes = kwargs.get("swing_modes")
        self._attr_target_temperature_step = kwargs.get("target_temperature_step")

        self._attr_max_temp = kwargs.get("max_temp")
        self._attr_min_temp = kwargs.get("min_temp")
        self._attr_target_temperature_high = kwargs.get("max_temp")
        self._attr_target_temperature_low = kwargs.get("min_temp")

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "current_temperature":
            return int(res_value)
        if res_name == "ac_state":
            # res_value: 十进制字符串
            ac_state_bin = bin(int(res_value))[2:].zfill(32)

            self.ac_state_to_attr(ac_state_bin)

    def ac_state_to_attr(self, bin):
        """空调状态转HA属性."""
        power = int(bin[0:4], 2)
        mode = int(bin[4:8], 2)
        fan = int(bin[8:12], 2)
        swing_direction = int(bin[12:14], 2)
        swing = int(bin[14:16], 2)
        temp = int(bin[16:24], 2)
        other = int(bin[24:32], 2)

        self.airrtc_tcpecn02_swing_direction = swing_direction
        self.airrtc_tcpecn02_other = other

        if power == 0:
            self._attr_hvac_mode = HVACMode.OFF
        elif power == 1:
            self._attr_hvac_mode = AC_STATE_RES_ATTR_MAPPING["hvac_mode"].get(
                str(mode), HVACMode.AUTO
            )

        if temp:
            self._attr_target_temperature = float(temp)

        self._attr_fan_mode = AC_STATE_RES_ATTR_MAPPING["fan_mode"].get(
            str(fan), FAN_AUTO
        )

        self._attr_swing_mode = AC_STATE_RES_ATTR_MAPPING["swing_mode"].get(
            str(swing), SWING_OFF
        )

        self.schedule_update_ha_state()

    def attr_to_ac_state(self, attr, value):
        """HA属性 转 ac_state."""
        power = 0 if self._attr_hvac_mode == HVACMode.OFF else 1
        mode = AC_STATE_ATTR_RES_MAPPING["hvac_mode"].get(self._attr_hvac_mode, "2")
        temp = int(self._attr_target_temperature)
        fan = AC_STATE_ATTR_RES_MAPPING["fan_mode"].get(self._attr_fan_mode, "3")
        swing = AC_STATE_ATTR_RES_MAPPING["swing_mode"].get(self._attr_swing_mode, "1")

        if attr == "hvac_mode":
            old_mode = self._attr_hvac_mode
            if value == HVACMode.OFF:
                power = 0
                mode = AC_STATE_ATTR_RES_MAPPING["hvac_mode"].get(
                    old_mode, HVACMode.AUTO
                )
            else:
                power = 1
                mode = AC_STATE_ATTR_RES_MAPPING["hvac_mode"].get(value, HVACMode.AUTO)
            self._attr_hvac_mode = value

        if attr == "target_temperature":
            self._attr_target_temperature = value
            temp = int(value)

        if attr == "fan_mode":
            self._attr_fan_mode = value
            fan = AC_STATE_ATTR_RES_MAPPING["fan_mode"].get(value, FAN_AUTO)

        if attr == "swing_mode":
            self._attr_swing_mode = value
            swing = AC_STATE_ATTR_RES_MAPPING["swing_mode"].get(value, SWING_OFF)

        self.schedule_update_ha_state()

        power_bin = bin(power)[2:].zfill(4)
        mode_bin = bin(int(mode))[2:].zfill(4)
        fan_bin = bin(int(fan))[2:].zfill(4)
        swing_direction_bin = bin(self.airrtc_tcpecn02_swing_direction)[2:].zfill(2)
        swing_bin = bin(int(swing))[2:].zfill(2)
        temp_bin = bin(temp)[2:].zfill(8)
        other_bin = bin(self.airrtc_tcpecn02_other)[2:].zfill(8)

        bin_str = f"{power_bin}{mode_bin}{fan_bin}{swing_direction_bin}{swing_bin}{temp_bin}{other_bin}"
        return int(bin_str, 2)

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        result = self.attr_to_ac_state("hvac_mode", hvac_mode)
        await self.async_set_res_value("ac_state", result)

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temp = kwargs.get("temperature")
        result = self.attr_to_ac_state("target_temperature", temp)
        await self.async_set_res_value("ac_state", result)

    async def async_set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        result = self.attr_to_ac_state("fan_mode", fan_mode)
        await self.async_set_res_value("ac_state", result)

    async def async_set_swing_mode(self, swing_mode):
        """Set new target swing operation."""
        result = self.attr_to_ac_state("swing_mode", swing_mode)
        await self.async_set_res_value("ac_state", result)


class AiotACPartnerP3Entity(AiotEntityBase, ClimateEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_temperature_unit = kwargs.get("temperature_unit")
        self._attr_hvac_modes = kwargs.get("hvac_modes")
        self._attr_fan_modes = kwargs.get("fan_modes")
        self._attr_swing_modes = kwargs.get("swing_modes")
        self._attr_preset_modes = kwargs.get("preset_modes")
        self._attr_target_temperature_step = kwargs.get("target_temperature_step")

        self._attr_max_temp = kwargs.get("max_temp")
        self._attr_min_temp = kwargs.get("min_temp")
        self._attr_target_temperature_high = kwargs.get("max_temp")
        self._attr_target_temperature_low = kwargs.get("min_temp")

        self._attr_preset_mode = None

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "ac_fun_ctl":
            self.ac_fun_ctl_to_attr(res_value)
        elif res_name == "ac_quick_cool":
            self.ac_quick_cool_to_attr(res_value)

    def ac_fun_ctl_to_attr(self, value):
        """空调功能控制 8.0.2116(P3) 转HA属性."""
        if value:
            # 用于处理ac_fun_ctl内容
            pattern = r"^P(\d+)_M(\d+)_T(\d+)_S(\d+)_D(\d+)(?:_L(\d+))?$"
            match = re.fullmatch(pattern, value)
            if not match:
                _LOGGER.error("Invalid 8.0.2116(P3) format.")
                return
            # 提取参数（注意group6可能为None）
            power = int(match.group(1))  # P值
            mode = int(match.group(2))  # M值
            temp = int(match.group(3))  # T值
            fan = int(match.group(4))  # S值
            swing = int(match.group(5))  # D值
            light = match.group(6)  # L值（可能为None）
            light = int(light) if light is not None else None

            if power == 1:
                self._attr_hvac_mode = HVACMode.OFF
            elif power == 0:
                self._attr_hvac_mode = P3_MODE_RES_ATTR_MAPPING.get(
                    str(mode), HVACMode.AUTO
                )

            if temp:
                self._attr_target_temperature = float(temp)

            self._attr_fan_mode = P3_FAN_RES_ATTR_MAPPING.get(str(fan), FAN_AUTO)

            if swing == 0:
                self._attr_swing_mode = SWING_ON
            else:
                self._attr_swing_mode = SWING_OFF

            self.schedule_update_ha_state()

    def ac_quick_cool_to_attr(self, value):
        value = int(value)
        if value == 1:
            self._attr_preset_mode = PRESET_BOOST
        elif value == 0:
            self._attr_preset_mode = PRESET_NONE

        self.schedule_update_ha_state()

    def attr_to_ac_fun_ctl(self, attr, value):
        """HA属性 转 空调功能控制 8.0.2116(P3)."""

        power = 1 if self._attr_hvac_mode == HVACMode.OFF else 0

        mode = P3_MODE_ATTR_RES_MAPPING.get(self._attr_hvac_mode, "0")

        temp = str(int(self._attr_target_temperature))

        fan = P3_FAN_ATTR_RES_MAPPING.get(self._attr_fan_mode, "2")

        swing = 0 if self._attr_swing_mode == SWING_ON else 1

        if attr == "hvac_mode":
            old_mode = self._attr_hvac_mode
            if value == HVACMode.OFF:
                power = 1
                mode = P3_MODE_ATTR_RES_MAPPING.get(old_mode, HVACMode.AUTO)
            else:
                power = 0
                mode = P3_MODE_ATTR_RES_MAPPING.get(value, HVACMode.AUTO)
            self._attr_hvac_mode = value

        if attr == "target_temperature":
            self._attr_target_temperature = value
            temp = int(value)

        if attr == "fan_mode":
            self._attr_fan_mode = value
            fan = P3_FAN_ATTR_RES_MAPPING.get(value, FAN_AUTO)

        if attr == "swing_mode":
            self._attr_swing_mode = value
            swing = 0 if value == SWING_ON else 1

        self.schedule_update_ha_state()

        result = f"P{power}_M{mode}_T{temp}_S{fan}_D{swing}"
        # _LOGGER.info(f"ac_fun_ctl: {result}")
        return result

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        result = self.attr_to_ac_fun_ctl("hvac_mode", hvac_mode)
        await self.async_set_res_value("ac_fun_ctl", result)

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temp = kwargs.get("temperature")
        result = self.attr_to_ac_fun_ctl("target_temperature", temp)
        await self.async_set_res_value("ac_fun_ctl", result)

    async def async_set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        result = self.attr_to_ac_fun_ctl("fan_mode", fan_mode)
        await self.async_set_res_value("ac_fun_ctl", result)

    async def async_set_swing_mode(self, swing_mode):
        """Set new target swing operation."""
        result = self.attr_to_ac_fun_ctl("swing_mode", swing_mode)
        await self.async_set_res_value("ac_fun_ctl", result)

    async def async_set_preset_mode(self, preset_mode):
        """Set new target preset mode."""
        if preset_mode == PRESET_BOOST:
            await self.async_set_res_value("ac_quick_cool", "1")
        elif preset_mode == PRESET_NONE:
            await self.async_set_res_value("ac_quick_cool", "0")
