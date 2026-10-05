import logging

from homeassistant.components.event import EventEntity

from .core.aiot_manager import (
    AiotEntityBase,
    AiotManager,
)
from .core.const import (
    BUTTON,
    DOMAIN,
    GESTURE_MAPPING,
    HASS_DATA_AIOT_MANAGER,
    HUMAN_MAPPING,
    MOVING_MAPPING,
    PET_MAPPING,
    SOUND_MAPPING,
)

_LOGGER = logging.getLogger(__name__)

TYPE = "event"

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "default": AiotEventEntity,
        "button": AiotButtonEntity,
        "camera": AiotCameraEntity,
        "face": AiotFaceEventEntity,
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotEventEntity(AiotEntityBase, EventEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        mapping = kwargs.get("event_mapping")
        self._attr_event_types = list(mapping.values())
        self.event_mapping = mapping
        icon = kwargs.get("icon")
        if icon:
            self._attr_icon = icon
        elif self._attr_device_class is None:
            # 有device_class时交给HA按类型显示图标，例如门铃
            self._attr_icon = "mdi:button-pointer"
        self._extra_state_attributes.extend(["trigger_time", "trigger_dt"])

    async def async_update(self):
        # 事件只来自消息推送；初始查询会拿到上一次的值，重启时误触发一次事件
        return

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "event":
            trigger = self.event_mapping.get(res_value)
            if trigger is None:
                # 不在event_types中的值会让_trigger_event抛ValueError
                _LOGGER.info(
                    f"[event, {self.device.did}]unmapped value: {res_value}"
                )
            else:
                self._trigger_event(trigger)
                self.schedule_update_ha_state()
        return super().convert_res_to_attr(res_name, res_value)


class AiotButtonEntity(AiotEntityBase, EventEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_event_types = list(BUTTON.values())
        self._extra_state_attributes.extend(["trigger_time", "trigger_dt"])

    @property
    def icon(self):
        """return icon."""
        return "mdi:button-pointer"

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "firmware_version":
            return res_value
        if res_name == "zigbee_lqi":
            return int(res_value)
        if res_name == "button" and res_value not in (0, ""):
            trigger = BUTTON.get(res_value, "unknown")
            self._trigger_event(trigger)
            self.schedule_update_ha_state()
        return super().convert_res_to_attr(res_name, res_value)


class AiotFaceEventEntity(AiotEntityBase, EventEntity):
    """人脸识别：熟人与陌生人合并为一个实体，家庭成员ID放在事件属性 member_id 中

    家庭成员ID是动态的，不能作为 event_types，否则遇到未预设的ID会抛 ValueError。
    """

    _attr_event_types = ["known", "stranger"]
    _attr_icon = "mdi:face-recognition"

    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        # 基类会用云端资源名覆盖名称，两个资源时只剩后一个，这里恢复
        if kwargs.get("entity_name"):
            self._attr_name = kwargs["entity_name"]
        self._extra_state_attributes.extend(["trigger_time", "trigger_dt"])

    async def async_update(self):
        # 事件只来自消息推送；初始查询会拿到上一次的值，重启时误触发一次事件
        return

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "detect_face_event" and res_value not in (0, "", "0"):
            self._trigger_event("known", {"member_id": res_value})
            self.schedule_update_ha_state()
        elif res_name == "detect_stranger_face_event":
            # 陌生人事件的值固定为0
            self._trigger_event("stranger")
            self.schedule_update_ha_state()
        return super().convert_res_to_attr(res_name, res_value)


class AiotCameraEntity(AiotEntityBase, EventEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._extra_state_attributes.extend(["trigger_time", "trigger_dt"])
        event_types = kwargs.get("event_types")
        event_types_mapping = kwargs.get("event_types_mapping")
        if event_types:
            self._attr_event_types = event_types
        if event_types_mapping:
            self._attr_event_types = list(event_types_mapping.values())

    @property
    def icon(self):
        """return icon."""
        return "mdi:alarm-light-outline"

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "detect_face_event" and res_value not in (0, ""):
            self._trigger_event(res_value)
        if res_name == "detect_human_event" and res_value not in (0, ""):
            self._trigger_event(HUMAN_MAPPING.get(res_value, "unknown"))
        if res_name == "detect_pets_event" and res_value not in (0, ""):
            self._trigger_event(PET_MAPPING.get(res_value, "unknown"))
        if res_name == "detect_gesture_event" and res_value not in (0, ""):
            self._trigger_event(GESTURE_MAPPING.get(res_value, "unknown"))
        if res_name == "detect_moving_event" and res_value not in (0, ""):
            self._trigger_event(MOVING_MAPPING.get(res_value, "unknown"))
        if res_name == "detect_sound_event" and res_value not in (0, ""):
            self._trigger_event(SOUND_MAPPING.get(res_value, "unknown"))
        self.schedule_update_ha_state()
        return super().convert_res_to_attr(res_name, res_value)
