from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.climate import (
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    PRESET_BOOST,
    PRESET_NONE,
    SWING_OFF,
    SWING_ON,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntityFeature,
    CoverState,
)
from homeassistant.components.event import EventDeviceClass
from homeassistant.components.light import ColorMode, LightEntityFeature
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    LIGHT_LUX,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfRatio,
    UnitOfTemperature,
)

from .const import (
    GESTURE_MAPPING,
    PET_MAPPING,
    HUMAN_MAPPING,
    MOVING_MAPPING,
    SOUND_MAPPING,
    DOORBELL_MAPPING,
    KN_BUTTON_MAPPING,
    KN_BUTTON_3_MAPPING,
    KN_SLIDE_MAPPING,
    FP_MOTION_MAPPING,
)

# AiotDevice Mapping
MK_MAPPING_PARAMS = "mapping_params"
MK_INIT_PARAMS = "init_params"
MK_RESOURCES = "resources"
MK_HASS_NAME = "hass_attr_name"

AIOT_DEVICE_MAPPING = [
    ############################ Aqara M1S网关###################################
    {
        "lumi.gateway.aeu01": ["Aqara", "Gateway M1S", "ZHWG15LM"],
        "lumi.gateway.acn01": ["Aqara", "Gateway M1S", "ZHWG15LM"],
        "lumi.gateway.acn004": ["Aqara", "Gateway M1S 22", "ZHWG15LM"],
        "lumi.gateway.acn008": ["Aqara", "Gateway M1S Gen2", ""],
        "lumi.gateway.agl002": ["Aqara", "Gateway M1S Gen2", "ZHWG15LM"],
        "lumi.gateway.aqhm02": ["Aqara", "Gateway", "ZHWG15LM"],
        "lumi.gateway.aqhm01": ["Aqara", "Gateway", "ZHWG15LM"],
        "params": [
            {
                "light": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "light",
                        "supported_features": LightEntityFeature.EFFECT,
                        "supported_color_modes": {ColorMode.RGB},
                        "color_mode": ColorMode.RGB,
                    },
                    MK_RESOURCES: {
                        "toggle": ("14.7.111", "_attr_is_on"),
                        "color": ("14.7.85", "_attr_rgb_color"),
                        "brightness": ("14.7.1006", "_attr_brightness"),
                    },
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "illuminance",
                        "device_class": SensorDeviceClass.ILLUMINANCE,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": LIGHT_LUX,
                    },
                    MK_RESOURCES: {"illumination": ("0.3.85", "_attr_native_value")},
                }
            },
        ],
    },
    ###########################绿米H1、E1、M2、M3、集悦S1网关#############################
    {
        "lumi.gateway.sacn01": ["Aqara", "Smart Hub H1", "QBCZWG11LM"],
        "lumi.gateway.aqcn02": ["Aqara", "Hub E1", "ZHWG16LM"],
        "lumi.gateway.iragl01": ["Aqara", "GateWay M2", ""],
        "lumi.gateway.iragl5": ["Aqara", "GateWay M2", ""],
        "lumi.gateway.iragl7": ["Aqara", "GateWay M2", ""],
        "lumi.gateway.iragl8": ["Aqara", "GateWay M2 22", ""],
        "lumi.gateway.aq1": ["Aqara", "GateWay M2", ""],
        "lumi.gateway.acn012": ["Aqara", "GateWay M3", ""],
        "lumi.controller.a4acn1": ["Aqara", "GateWay JY S1", ""],
        "params": [],
    },
    ###############################网关/摄像机########################################
    {
        "lumi.camera.gwpagl01": ["Aqara", "Camera G3 (Gateway)", ""],
        "params": [
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "camera",
                        "event_types": [
                            "1",
                            "2",
                            "3",
                            "4",
                            "5",
                            "6",
                            "7",
                            "8",
                            "9",
                            "10",
                        ],
                        "unique_id_extra": "face",
                        "entity_name": "人脸识别",
                    },
                    MK_RESOURCES: {
                        "detect_face_event": ("13.95.85", "_attr_native_value"),
                    },
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "camera",
                        "event_types_mapping": HUMAN_MAPPING,
                        "unique_id_extra": "human",
                        "entity_name": "人体识别",
                    },
                    MK_RESOURCES: {
                        "detect_human_event": ("13.97.85", "_attr_native_value"),
                    },
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "camera",
                        "event_types_mapping": PET_MAPPING,
                        "unique_id_extra": "pet",
                        "entity_name": "宠物识别",
                    },
                    MK_RESOURCES: {
                        "detect_pets_event": ("13.98.85", "_attr_native_value"),
                    },
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "camera",
                        "event_types_mapping": GESTURE_MAPPING,
                        "unique_id_extra": "gesture",
                        "entity_name": "手势识别",
                    },
                    MK_RESOURCES: {
                        "detect_gesture_event": ("13.96.85", "_attr_native_value"),
                    },
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "camera",
                        "event_types_mapping": MOVING_MAPPING,
                        "unique_id_extra": "moving",
                        "entity_name": "移动侦测",
                    },
                    MK_RESOURCES: {
                        "detect_moving_event": ("3.21.85", "_attr_native_value"),
                    },
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "camera",
                        "event_types_mapping": SOUND_MAPPING,
                        "unique_id_extra": "sound",
                        "entity_name": "异常声音",
                    },
                    MK_RESOURCES: {
                        "detect_sound_event": ("3.22.85", "_attr_native_value"),
                    },
                }
            },
        ],
    },
    {
        "lumi.camera.acn005": ["Aqara", "DoorBell G4", ""],
        "params": [
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": DOORBELL_MAPPING,
                        "device_class": EventDeviceClass.DOORBELL,
                        "entity_name": "门铃",
                    },
                    MK_RESOURCES: {"event": ("13.12.85", "_attr_trigger")},
                }
            },
        ],
    },
    ################################墙壁开关#########################################
    ###单键
    {
        # 卡农 智能墙壁开关 Z1 Pro（单键版）
        "lumi.switch.acn056": ["Aqara", "KN Wall Switch Z1 Pro (Single Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                    },
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": KN_BUTTON_MAPPING,
                        "entity_name": "无线开关",
                    },
                    MK_RESOURCES: {"event": ("13.21.85", "_attr_trigger")},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "slide",
                        "event_mapping": KN_SLIDE_MAPPING,
                        "entity_name": "滑条",
                    },
                    MK_RESOURCES: {"event": ("13.1.85", "_attr_trigger")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"current": ("0.14.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 卡农 智能墙壁开关 Z1 Pro（双键版）
        "lumi.switch.acn057": ["Aqara", "KN Wall Switch Z1 Pro (Double Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 2},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": KN_BUTTON_MAPPING,
                        "entity_name": "无线开关",
                    },
                    MK_RESOURCES: {"event": ("13.{}.85", "_attr_trigger")},
                    MK_MAPPING_PARAMS: {"ch_count": 2, "ch_start": 21},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "slide",
                        "event_mapping": KN_SLIDE_MAPPING,
                        "entity_name": "滑条",
                    },
                    MK_RESOURCES: {"event": ("13.1.85", "_attr_trigger")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 卡农 智能墙壁开关 Z1 Pro（三键版）
        "lumi.switch.acn058": ["Aqara", "KN Wall Switch Z1 Pro (Three Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 3},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": KN_BUTTON_3_MAPPING,
                        "entity_name": "无线开关",
                    },
                    MK_RESOURCES: {"event": ("13.{}.85", "_attr_trigger")},
                    MK_MAPPING_PARAMS: {"ch_count": 3, "ch_start": 21},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "slide",
                        "event_mapping": KN_SLIDE_MAPPING,
                        "entity_name": "滑条",
                    },
                    MK_RESOURCES: {"event": ("13.1.85", "_attr_trigger")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 卡农 智能墙壁开关 Z1 Pro（四键版）
        "lumi.switch.acn059": ["Aqara", "KN Wall Switch Z1 Pro (Four Rocker)", ""],
        # 智能墙壁开关 Q1（四键版）
        "lumi.switch.acn065": ["Aqara", "Wall Switch Q1 (Four Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 3},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": KN_BUTTON_3_MAPPING,
                        "entity_name": "无线开关",
                    },
                    MK_RESOURCES: {"event": ("13.{}.85", "_attr_trigger")},
                    MK_MAPPING_PARAMS: {"ch_count": 4, "ch_start": 21},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "slide",
                        "event_mapping": KN_SLIDE_MAPPING,
                        "entity_name": "滑条",
                    },
                    MK_RESOURCES: {"event": ("13.1.85", "_attr_trigger")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 卡农 智能墙壁开关 Z1（单键版）
        "lumi.switch.acn054": ["Aqara", "KN Wall Switch Z1 (Single Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                    },
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": KN_BUTTON_MAPPING,
                        "entity_name": "无线开关",
                    },
                    MK_RESOURCES: {"event": ("13.21.85", "_attr_trigger")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 卡农 智能墙壁开关 Z1（双键版）
        "lumi.switch.acn054": ["Aqara", "KN Wall Switch Z1 (Double Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 2},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": KN_BUTTON_3_MAPPING,
                        "entity_name": "无线开关",
                    },
                    MK_RESOURCES: {"event": ("13.{}.85", "_attr_trigger")},
                    MK_MAPPING_PARAMS: {"ch_count": 2, "ch_start": 21},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 卡农 智能墙壁开关 Z1（三键版）
        "lumi.switch.acn054": ["Aqara", "KN Wall Switch Z1 (Three Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 3},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": KN_BUTTON_3_MAPPING,
                        "entity_name": "无线开关",
                    },
                    MK_RESOURCES: {"event": ("13.{}.85", "_attr_trigger")},
                    MK_MAPPING_PARAMS: {"ch_count": 3, "ch_start": 21},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 卡农 智能墙壁开关 Z1（四键版）
        "lumi.switch.acn055": ["Aqara", "KN Wall Switch Z1 (Four Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 3},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": KN_BUTTON_3_MAPPING,
                        "entity_name": "无线开关",
                    },
                    MK_RESOURCES: {"event": ("13.{}.85", "_attr_trigger")},
                    MK_MAPPING_PARAMS: {"ch_count": 4, "ch_start": 21},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 智能墙壁开关 Q1（单键版）
        "lumi.switch.acn062": ["Aqara", "Wall Switch Q1 (Single Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                    },
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": KN_BUTTON_MAPPING,
                        "entity_name": "无线开关",
                    },
                    MK_RESOURCES: {"event": ("13.21.85", "_attr_trigger")},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "slide",
                        "event_mapping": KN_SLIDE_MAPPING,
                        "entity_name": "滑条",
                    },
                    MK_RESOURCES: {"event": ("13.1.85", "_attr_trigger")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 智能墙壁开关 Q1（双键版）
        "lumi.switch.acn063": ["Aqara", "KN Wall Switch Q1 (Double Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 2},
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "slide",
                        "event_mapping": KN_SLIDE_MAPPING,
                        "entity_name": "滑条",
                    },
                    MK_RESOURCES: {"event": ("13.1.85", "_attr_trigger")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 墙壁开关（零火线单键版）
        "lumi.ctrl_ln1.v1": ["Aqara", "Wall Switch (Single Rocker)", ""],
        # 墙壁开关H1M（零火线单键版）
        "lumi.switch.acn029": ["Aqara", "Wall Switch H1M (Single Rocker)", ""],
        # 墙壁开关X1（零火线单键版）
        "lumi.switch.acn004": ["Aqara", "Wall Switch X1 (Single Rocker)", ""],
        # 墙壁开关H1（零火线单键版）
        "lumi.switch.n1acn1": ["Aqara", "Wall Switch H1 (Single Rocker)", "QBKG27LM"],
        # 墙壁开关T1（零火线单键版）
        "lumi.switch.b1nacn01": ["Aqara", "Wall Switch T1 (Single Rocker)", ""],
        # 墙壁开关D1（零火线单键版）
        "lumi.switch.b1nacn02": ["Aqara", "Wall Switch D1 (Single Rocker)", ""],
        # 墙壁开关E1（零火线单键版）
        "lumi.switch.b1nc01": ["Aqara", "Wall Switch E1 (Single Rocker)", ""],
        # 智能墙壁开关 J1（零火线单键版）
        "lumi.switch.acn044": ["Aqara", "Wall Switch J1 (Single Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 墙壁开关（单火线单键版）
        "lumi.ctrl_neutral1.v1": ["Aqara", "Wall Switch (Single Rocker)", "QBKG04LM"],
        # 墙壁开关X1（单火线单键版）
        "lumi.switch.acn001": ["Aqara", "Wall Switch X1 (Single Rocker)", ""],
        # 墙壁开关H1（单火线单键版）
        "lumi.switch.l1acn1": ["Aqara", "Wall Switch H1 (Single Rocker)", "QBKG27LM"],
        # 墙壁开关T1（单火线单键版）
        "lumi.switch.b1lacn01": ["Aqara", "Wall Switch T1 (Single Rocker)", ""],
        # 墙壁开关D1（单火线单键版）
        "lumi.switch.b1lacn02": ["Aqara", "Wall Switch D1 (Single Rocker)", ""],
        # 墙壁开关E1（单火线单键版）
        "lumi.switch.b1lc04": ["Aqara", "Wall Switch E1 (Single Rocker)", ""],
        # 墙壁开关J1（单火线单键版）
        "lumi.switch.acn041": ["Aqara", "Wall Switch J1 (Single Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            }
        ],
    },
    ###双键
    {
        # 墙壁开关（零火线双键版）
        "lumi.ctrl_ln2.v1": ["Aqara", "Wall Switch (Double Rocker)", ""],
        # 墙壁开关H1M（零火线双键版）
        "lumi.switch.acn030": ["Aqara", "Wall Switch H1M (Double Rocker)", ""],
        # 墙壁开关X1（零火线双键版）
        "lumi.switch.acn005": ["Aqara", "Wall Switch X1 (Double Rocker)", ""],
        # 墙壁开关H1（零火线双键版）
        "lumi.switch.n2acn1": ["Aqara", "Wall Switch H1 (Double Rocker)", "QBKG27LM"],
        # 墙壁开关T1（零火线双键版）
        "lumi.switch.b2nacn01": ["Aqara", "Wall Switch T1 (Double Rocker)", ""],
        # 墙壁开关D1（零火线双键版）
        "lumi.switch.b2nacn02": ["Aqara", "Wall Switch D1 (Double Rocker)", ""],
        # 墙壁开关E1（零火线双键版）
        "lumi.switch.b2nc01": ["Aqara", "Wall Switch E1 (Double Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 2},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 智能墙壁开关 J1（零火线双键版）
        "lumi.switch.acn045": ["Aqara", "Wall Switch J1 (Double Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 2},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 墙壁开关（单火线双键版）
        "lumi.ctrl_neutral2.v1": ["Aqara", "Wall Switch (Double Rocker)", "QBKG04LM"],
        # 墙壁开关X1（单火线双键版）
        "lumi.switch.acn002": ["Aqara", "Wall Switch X1 (Double Rocker)", ""],
        # 墙壁开关H1（单火线双键版）
        "lumi.switch.l2acn1": ["Aqara", "Wall Switch H1 (Double Rocker)", "QBKG28LM"],
        # 墙壁开关T1（单火线双键版）
        "lumi.switch.b2lacn01": ["Aqara", "Wall Switch T1 (Double Rocker)", ""],
        # 墙壁开关D1（单火线双键版）
        "lumi.switch.b2lacn02": ["Aqara", "Wall Switch D1 (Double Rocker)", "QBKG21LM"],
        # 墙壁开关E1（单火线双键版）
        "lumi.switch.b2lc04": ["Aqara", "Wall Switch E1 (Double Rocker)", "QBKG21LM"],
        # 智能墙壁开关 J1（单火线双键版）
        "lumi.switch.acn042": ["Aqara", "Wall Switch J1 (Double Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 2},
                }
            }
        ],
    },
    ###三键
    {
        # 墙壁开关H1M（零火线三键版）
        "lumi.switch.acn031": ["Aqara", "Wall Switch H1M (Three Rocker)", ""],
        # 墙壁开关X1（零火线三键版）
        "lumi.switch.acn006": ["Aqara", "Wall Switch X1 (Three Rocker)", ""],
        # 墙壁开关H1（零火线三键版）
        "lumi.switch.n3acn1": ["Aqara", "Wall Switch H1 (Three Rocker)", "QBKG27LM"],
        # 墙壁开关T1（零火线三键版）
        "lumi.switch.b3n01": ["Aqara", "Wall Switch T1 (Three Rocker)", ""],
        # 智能场景面板开关 S1（零火线三键版）
        "lumi.switch.n4acn4": ["Aqara", "screen panel S1 (Three Rocker)", ""],
        # 智能墙壁开关D1（零火线三键版）
        "lumi.switch.n3acn3": ["Aqara", "Wall Switch D1 (Three Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 3},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 智能墙壁开关 E1（零火线三键版）
        "lumi.switch.acn040": ["Aqara", "Wall Switch E1 (Three Rocker)", ""],
        # 智能墙壁开关 J1（零火线三键版）
        "lumi.switch.acn046": ["Aqara", "Wall Switch J1 (Three Rocker)", ""],
        # 妙控开关 V1（四键版）
        "lumi.switch.acn051": ["Aqara", "Wall Switch V1", ""],
        # 繁星旋钮 V1
        "lumi.switch.acn053": ["Aqara", "Wall Switch V1", ""],
        # 妙控开关 S1E
        "lumi.switch.acn032": ["Aqara", "Wall Switch S1E", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 3},
                }
            }
        ],
    },
    {
        # 墙壁开关X1（单火线三键版）
        "lumi.switch.acn003": ["Aqara", "Wall Switch X1 (Three Rocker)", ""],
        # 墙壁开关H1（单火线三键版）
        "lumi.switch.l3acn1": ["Aqara", "Wall Switch H1 (Three Rocker)", "QBKG29LM"],
        # 墙壁开关T1（单火线三键版）
        "lumi.switch.b3l01": ["Aqara", "Wall Switch T1 (Three Rocker)", ""],
        # 智能墙壁开关D1（单火线三键版）
        "lumi.switch.l3acn3": ["Aqara", "Wall Switch D1 (Three Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 3},
                }
            }
        ],
    },
    {
        # 墙壁开关J1（单火线三键版）
        "lumi.switch.acn043": ["Aqara", "Wall Switch J1 (Three Rocker)", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "wall_switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 3},
                }
            }
        ],
    },
    {
        # 集悦妙控屏 S1 Plus
        "lumi.switch.acn034": ["Aqara", "Magic Pad S1 Plus", ""],
        "params": [
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": SensorStateClass.TOTAL_INCREASING,
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    ##########################通断器、插座开关#######################################
    {
        # 单路控制器 T1（单火版）
        "lumi.switch.l0acn1": ["Aqara", "Wall Switch (Single Rocker)", ""],
        # 单路控制器（零火版）
        "lumi.switch.n0acn2": ["Aqara", "Wall Switch (Single Rocker)", ""],
        # 智能插座 (国标)
        "lumi.plug.v1": ["Xiaomi", "Plug", "ZNCZ02LM"],
        # 智能插座 (国标)
        "lumi.plug.aq1": ["Xiaomi", "Plug", ""],
        # 智能插座T1 (国标)
        "lumi.plug.macn01": ["Aqara", "Plug T1", ""],
        # 智能墙壁插座 X1（USB版）
        "lumi.plug.acn003": ["Aqara", "Smart Wall Outlet X1(USB)", ""],
        # 智能墙壁插座 H1（USB版）
        "lumi.plug.sacn03": ["Aqara", "Smart Wall Outlet H1(USB)", "QBCZWG11LM"],
        # 智能墙壁插座 H1
        "lumi.plug.sacn02": ["Aqara", "Smart Wall Outlet H1", "QBCZWG11LM"],
        # 墙壁插座（Zigbee版）
        "lumi.ctrl_86plug.aq1": ["Aqara", "Plug AQ1", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {MK_HASS_NAME: "switch"},
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                        "power": ("0.12.85", "_attr_current_power_w"),
                        "energy": ("0.13.85", "_attr_today_energy_kwh"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    ###双路控制器、继电器
    {
        # 双路控制器
        "lumi.relay.c2acn01": ["Aqara", "Double Way Controller", ""],
        # 双路控制模块 T2
        "lumi.switch.acn047": ["Aqara", "Double Way Controller T2", ""],
        "params": [
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.{}.85", "_attr_is_on"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": 2},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "energy",
                        "device_class": SensorDeviceClass.ENERGY,
                        "state_class": "total_increasing",
                        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    },
                    MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
                }
            },
        ],
    },
    ###############################调光器###########################################
    # 亮度类
    {
        # Aqara 智能恒流驱动器 T1-1
        "lumi.light.cbacn1": ["Aqara", "Constant current driver T1", ""],
        # 轨道格栅灯 H1（6头）
        "lumi.light.acn007": ["Aqara", "H1 LED Light", ""],
        # 轨道格栅灯 H1（12头）
        "lumi.light.acn008": ["Aqara", "H1 LED Light", ""],
        # 轨道泛光灯 H1（30cm）
        "lumi.light.acn009": ["Aqara", "H1 LED Light", ""],
        # 轨道泛光灯 H1（60cm）
        "lumi.light.acn010": ["Aqara", "H1 LED Light", ""],
        # 轨道吊线灯 H1
        "lumi.light.acn011": ["Aqara", "H1 LED Light", ""],
        # 轨道折叠格栅灯 H1（6头）
        "lumi.light.acn012": ["Aqara", "H1 LED Light", ""],
        # 轨道偏光灯 H1（22cm）
        "lumi.light.acn013": ["Aqara", "H1 LED Light", ""],
        "params": [
            {
                "light": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "light",
                        "supported_features": LightEntityFeature.EFFECT,
                        "supported_color_modes": {
                            ColorMode.BRIGHTNESS,
                        },
                        "color_mode": ColorMode.BRIGHTNESS,
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                        "brightness": ("14.1.85", "_attr_brightness"),
                    },
                }
            }
        ],
    },
    # 色温类
    {
        # LED灯泡（可调色温）
        "lumi.light.aqcn02": ["Aqara", "Bulb", "ZNLDP12LM"],
        # 吸顶灯MX960（可调色温）
        "lumi.light.cwopcn01": ["Aqara", "Opple MX960", "XDD11LM"],
        # 吸顶灯MX650（可调色温）
        "lumi.light.cwopcn02": ["Aqara", "Opple MX650", "XDD12LM"],
        # 吸顶灯MX480（可调色温）
        "lumi.light.cwopcn03": ["Aqara", "Opple MX480", "XDD13LM"],
        # Aqara智能调光模块T1（0-10v）
        "lumi.light.cwacn1": ["Aqara", "0-10V Dimmer", "ZNTGMK12LM"],
        # 射灯（可调色温）
        "lumi.light.cwjwcn01": ["Aqara", "Spotlight", ""],
        # 筒灯（可调色温）
        "lumi.light.cwjwcn02": ["Aqara", "Spotlight", ""],
        # Aqara 双色温驱动器 T1 Pro
        "lumi.light.acn004": ["Aqara", "Double Color Temp Driver T1 Pro", ""],
        # 轨道灯 H1 Pro
        "lumi.light.acn006": ["Aqara", "Rail Light H1 Pro", ""],
        # 射灯 T2（15度）
        "lumi.light.acn023": ["Aqara", "Spotlight T2", ""],
        # 射灯 T2（24度）
        "lumi.light.acn024": ["Aqara", "Spotlight T2", ""],
        # 射灯 T2（36度）
        "lumi.light.acn025": ["Aqara", "Spotlight T2", ""],
        # 筒灯 T2（60度）
        "lumi.light.acn026": ["Aqara", "Spotlight T2", ""],
        # 筒射灯 T3
        "lumi.light.acn128": ["Aqara", "Spotlight T3", ""],
        "params": [
            {
                "light": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "light",
                        "supported_features": LightEntityFeature.EFFECT,
                        "supported_color_modes": {
                            ColorMode.COLOR_TEMP,
                        },
                        "color_mode": ColorMode.COLOR_TEMP,
                        "min_color_temp_kelvin": 2703,
                        "max_color_temp_kelvin": 6500,
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                        "brightness": ("14.1.85", "_attr_brightness"),
                        "color_temp_kelvin": ("14.2.85", "_attr_color_temp_kelvin"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            }
        ],
    },
    {
        # Aqara LED灯泡 T1
        "lumi.light.cwac02": ["Aqara", "Bulb T1", "ZNLDP13LM"],
        # LED灯泡 T1（可调色温）
        "lumi.light.acn014": ["Aqara", "Bulb T1", ""],
        # Aqara 吸顶灯 L1-350
        "lumi.light.acn003": ["Aqara", "Light L1-350", ""],
        # Aqara光艺晴空灯 H1
        "lumi.light.acn015": ["Aqara", "Light H1", ""],
        "params": [
            {
                "light": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "light",
                        "supported_features": LightEntityFeature.EFFECT,
                        "supported_color_modes": {
                            ColorMode.COLOR_TEMP,
                        },
                        "color_mode": ColorMode.COLOR_TEMP,
                        "min_color_temp_kelvin": 2703,
                        "max_color_temp_kelvin": 6500,
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                        "brightness": ("1.7.85", "_attr_brightness"),
                        "color_temp_kelvin": ("1.9.85", "_attr_color_temp_kelvin"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            }
        ],
    },
    {
        # 幻彩吸顶灯 T1（40W）
        "lumi.light.acn032": ["Aqara", "Ceiling Light T1", ""],
        "params": [
            {
                "light": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "light",
                        "supported_features": LightEntityFeature.EFFECT,
                        "supported_color_modes": {
                            ColorMode.COLOR_TEMP,
                        },
                        "color_mode": ColorMode.COLOR_TEMP,
                        "min_color_temp_kelvin": 2703,
                        "max_color_temp_kelvin": 6500,
                        "unique_id_extra": "ch1",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                        "brightness": ("1.7.85", "_attr_brightness"),
                        "color_temp_kelvin": ("1.9.85", "_attr_color_temp_kelvin"),
                    },
                }
            },
            {
                "light": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "light",
                        "supported_features": LightEntityFeature.EFFECT,
                        "supported_color_modes": {
                            ColorMode.COLOR_TEMP,
                        },
                        "color_mode": ColorMode.COLOR_TEMP,
                        "min_color_temp_kelvin": 2703,
                        "max_color_temp_kelvin": 6500,
                        "unique_id_extra": "ch2",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.2.85", "_attr_is_on"),
                        "brightness": ("1.8.85", "_attr_brightness"),
                        "color_temp_kelvin": ("1.10.85", "_attr_color_temp_kelvin"),
                    },
                }
            },
        ],
    },
    {
        # 智能灯带驱动器 T1 (60W/120W/240W)
        "lumi.dimmer.acn003": ["Aqara", "LED Strip Dimmer T1", "ZNDDQDQ11LM"],
        "lumi.dimmer.acn004": ["Aqara", "LED Strip Dimmer T1", "ZNDDQDQ12LM"],
        "lumi.dimmer.acn005": ["Aqara", "LED Strip Dimmer T1", "ZNDDQDQ13LM"],
        "params": [
            {
                "light": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "light",
                        "supported_features": LightEntityFeature.EFFECT,
                        "supported_color_modes": {
                            ColorMode.COLOR_TEMP,
                        },
                        "color_mode": ColorMode.COLOR_TEMP,
                        "min_color_temp_kelvin": 2700,
                        "max_color_temp_kelvin": 6500,
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                        "brightness": ("1.7.85", "_attr_brightness"),
                        "color_temp_kelvin": ("1.9.85", "_attr_color_temp_kelvin"),
                    },
                }
            }
        ],
    },
    # RGB类
    {
        # Aqara智能调光模块 T1
        "lumi.light.rgbac1": ["Aqara", "RGBW LED Controller T1", "ZNTGMK11LM"],
        # Aqara智能灯带驱动模块
        "lumi.dimmer.rcbac1": ["Aqara", "RGBW LED Dimmer", "ZNDDMK11LM"],
        "params": [
            {
                "light": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "light",
                        "supported_features": LightEntityFeature.EFFECT,
                        "supported_color_modes": {
                            ColorMode.XY,
                        },
                        "color_mode": ColorMode.XY,
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                        "brightness": ("14.1.85", "_attr_brightness"),
                        "color": ("14.8.85", "_attr_xy_color"),
                        "color_temp_kelvin": ("14.2.85", "_attr_color_temp_kelvin"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            }
        ],
    },
    {
        # 流光溢彩灯带 T1
        "lumi.light.acn132": ["Aqara", "RGB LED Belt T1", ""],
        "params": [
            {
                "light": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "light",
                        "supported_features": LightEntityFeature.EFFECT,
                        "supported_color_modes": {
                            ColorMode.XY,
                        },
                        "color_mode": ColorMode.XY,
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                        "brightness": ("1.7.85", "_attr_brightness"),
                        "color": ("14.8.85", "_attr_xy_color"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            }
        ],
    },
    ##################################窗帘##################################
    {
        # 智能窗帘电机 (Zigbee开合帘版)
        "lumi.curtain.v1": ["Aqara", "Curtain Motor Zigbee", ""],
        # Aqara智能窗帘电机 T1
        "lumi.curtain.acn007": ["Aqara", "Curtain Motor T1", ""],
        # 智能窗帘电机 C2
        "lumi.curtain.hagl07": ["Aqara", "Curtain Motor C2", ""],
        # Aqara智能窗帘电机A1
        "lumi.curtain.hagl08": ["Aqara", "Curtain Motor A1", ""],
        # 智能窗帘电机 B1
        "lumi.curtain.hagl04": ["Aqara", "Curtain Motor B1", ""],
        # Aqara智能窗帘电机 T2
        "lumi.curtain.acn015": ["Aqara", "Curtain Motor T2", ""],
        # 智能管状电机
        "lumi.curtain.aq2": ["Aqara", "Tube Motor", ""],
        # 智能管状电机 T1
        "lumi.curtain.vagl02": ["Aqara", "Tube Motor T1", ""],
        "params": [
            {
                "cover": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "curtain",
                        "device_class": CoverDeviceClass.CURTAIN,
                        "state_class": CoverState,
                        "supported_features": CoverEntityFeature.OPEN
                        | CoverEntityFeature.CLOSE
                        | CoverEntityFeature.STOP
                        | CoverEntityFeature.SET_POSITION,
                    },
                    MK_RESOURCES: {
                        "is_closed": ("14.2.85", "_attr_is_closed"),
                        "current_cover_position": (
                            "1.1.85",
                            "_attr_current_cover_position",
                        ),
                        "running_status": ("14.4.85", "_attr_native_value"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            }
        ],
    },
    {
        # 智能窗帘电机 B1
        "lumi.curtain.hagl04": ["Aqara", "Curtain Motor B1", ""],
        "params": [
            {
                "cover": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "curtain",
                        "device_class": CoverDeviceClass.CURTAIN,
                        "state_class": CoverState,
                        "supported_features": CoverEntityFeature.OPEN
                        | CoverEntityFeature.CLOSE
                        | CoverEntityFeature.STOP
                        | CoverEntityFeature.SET_POSITION,
                    },
                    MK_RESOURCES: {
                        "is_closed": ("14.2.85", "_attr_is_closed"),
                        "current_cover_position": (
                            "1.1.85",
                            "_attr_current_cover_position",
                        ),
                        "running_status": ("14.4.85", "_attr_native_value"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "battery",
                        "device_class": SensorDeviceClass.BATTERY,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfRatio.PERCENTAGE,
                    },
                    MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # Aqara智能窗帘电机 C3
        "lumi.curtain.acn04": ["Aqara", "Curtain Motor C3", ""],
        "params": [
            {
                "cover": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "curtain",
                        "device_class": CoverDeviceClass.CURTAIN,
                        "state_class": CoverState,
                        "supported_features": CoverEntityFeature.OPEN
                        | CoverEntityFeature.CLOSE
                        | CoverEntityFeature.STOP
                        | CoverEntityFeature.SET_POSITION,
                    },
                    MK_RESOURCES: {
                        "is_closed": ("14.2.85", "_attr_is_closed"),
                        "current_cover_position": (
                            "1.1.85",
                            "_attr_current_cover_position",
                        ),
                        "running_status": ("13.4.85", "_attr_native_value"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            }
        ],
    },
    {
        # 智能窗帘伴侣E1
        "lumi.curtain.acn003": ["Aqara", "Curtain Partner E1", ""],
        "params": [
            {
                "cover": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "curtain",
                        "device_class": CoverDeviceClass.CURTAIN,
                        "state_class": CoverState,
                        "supported_features": CoverEntityFeature.OPEN
                        | CoverEntityFeature.CLOSE
                        | CoverEntityFeature.STOP
                        | CoverEntityFeature.SET_POSITION,
                    },
                    MK_RESOURCES: {
                        "is_closed": ("14.8.85", "_attr_is_closed"),
                        "current_cover_position": (
                            "1.1.85",
                            "_attr_current_cover_position",
                        ),
                        "running_status": ("14.4.85", "_attr_native_value"),
                    },
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "battery",
                        "device_class": SensorDeviceClass.BATTERY,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfRatio.PERCENTAGE,
                    },
                    MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 智能卷帘伴侣E1
        "lumi.curtain.acn002": ["Aqara", "Curtain Partner E1", ""],
        "params": [
            {
                "cover": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "curtain",
                        "device_class": CoverDeviceClass.CURTAIN,
                        "state_class": CoverState,
                        "supported_features": CoverEntityFeature.OPEN
                        | CoverEntityFeature.CLOSE
                        | CoverEntityFeature.STOP
                        | CoverEntityFeature.SET_POSITION,
                    },
                    MK_RESOURCES: {
                        "is_closed": ("14.8.85", "_attr_is_closed"),
                        "current_cover_position": (
                            "1.1.85",
                            "_attr_current_cover_position",
                        ),
                        "running_status": ("14.4.85", "_attr_native_value"),
                    },
                }
            },
        ],
    },
    ##################################晾衣机##################################
    {
        # 智能晾衣机H1
        "lumi.airer.acn001": ["Aqara", "Airer H1", ""],
        "params": [
            {
                "cover": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "airer",
                        "device_class": CoverDeviceClass.AWNING,
                        "state_class": CoverState,
                        "supported_features": CoverEntityFeature.OPEN
                        | CoverEntityFeature.CLOSE
                        | CoverEntityFeature.STOP,
                    },
                    MK_RESOURCES: {
                        "is_closed": ("14.1.85", "_attr_is_closed"),
                    },
                }
            },
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "switch",
                        "unique_id_extra": "1",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.21.85", "_attr_is_on"),
                    },
                }
            },
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "switch",
                        "entity_name": "风干",
                        "unique_id_extra": "2",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.66.85", "_attr_is_on"),
                    },
                }
            },
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "switch",
                        "entity_name": "烘干",
                        "unique_id_extra": "3",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.67.85", "_attr_is_on"),
                    },
                }
            },
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "switch",
                        "entity_name": "消毒",
                        "unique_id_extra": "4",
                    },
                    MK_RESOURCES: {
                        "toggle": ("4.22.85", "_attr_is_on"),
                    },
                }
            },
        ],
    },
    {
        # Aqara智能晾衣机 Lite
        "lumi.airer.acn02": ["Aqara", "Airer Lite", ""],
        "params": [
            {
                "cover": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "airer",
                        "device_class": CoverDeviceClass.AWNING,
                        "state_class": CoverState,
                        "supported_features": CoverEntityFeature.OPEN
                        | CoverEntityFeature.CLOSE
                        | CoverEntityFeature.STOP
                        | CoverEntityFeature.SET_POSITION,
                    },
                    MK_RESOURCES: {
                        "is_closed": ("14.1.85", "_attr_is_closed"),
                        "current_cover_position": (
                            "1.1.85",
                            "_attr_current_cover_position",
                        ),
                    },
                }
            },
            {
                "switch": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "switch",
                    },
                    MK_RESOURCES: {
                        "toggle": ("14.2.85", "_attr_is_on"),
                    },
                }
            },
        ],
    },
    ##################################无线开关##################################
    {
        # 无线开关（贴墙式单键版）
        "lumi.remote.b186acn01": ["Aqara", "Single Wall Button", "WXKG03LM"],
        # 无线开关T1
        "lumi.remote.b1acn02": [
            "Aqara",
            "Wireless Remote Switch T1 (Single Rocker)",
            "",
        ],
        # 无线开关
        "lumi.remote.b1acn01": ["Aqara", "Wireless Remote Switch (Single Rocker)", ""],
        # 无线开关
        "lumi.sensor_switch.v1": [
            "Aqara",
            "Wireless Remote Switch (Single Rocker)",
            "",
        ],
        # 无线开关
        "lumi.sensor_switch.v2": [
            "Aqara",
            "Wireless Remote Switch (Single Rocker)",
            "",
        ],
        # 无线开关
        "lumi.sensor_switch.aq2": [
            "Aqara",
            "Wireless Remote Switch (Single Rocker)",
            "",
        ],
        # 无线开关（升级版）
        "lumi.sensor_switch.aq3": [
            "Aqara",
            "Wireless Remote Switch Plus (Single Rocker)",
            "",
        ],
        # 无线开关H1（贴墙式单键版）
        "lumi.remote.b18ac1": [
            "Aqara",
            "Wireless Remote Switch H1 (Single Rocker)",
            "WXKG14LM",
        ],
        # 无线开关E1（贴墙式单键版）
        "lumi.remote.acn003": [
            "Aqara",
            "Wireless Remote Switch E1 (Single Rocker)",
            "",
        ],
        # 无线开关E1（贴墙式单键版）
        "lumi.remote.acn007": [
            "Aqara",
            "Wireless Remote Switch E1 (Single Rocker)",
            "WXKG16LM",
        ],
        # 无线开关D1（贴墙式单键版）
        "lumi.remote.b186acn02": [
            "Aqara",
            "Wireless Remote Switch D1 (Single Rocker)",
            "WXKG06LM",
        ],
        # 无线开关T1（贴墙式单键版）
        "lumi.remote.b186acn03": [
            "Aqara",
            "Wireless Remote Switch T1 (Single Rocker)",
            "",
        ],
        "params": [
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "button",
                        "device_class": EventDeviceClass.BUTTON,
                    },
                    MK_RESOURCES: {"button": ("13.1.85", "_attr_trigger")},
                }
            }
        ],
    },
    ###无线双键
    {
        # 无线场景开关（双键版）
        "lumi.remote.b286acn01": ["Aqara", "Double Wall Button", "WXKG02LM"],
        # 无线开关H1（贴墙式双键版）
        "lumi.remote.b28ac1": [
            "Aqara",
            "Wireless Remote Switch H1 (Double Rocker)",
            "WXKG15LM",
        ],
        # 无线开关E1（贴墙式双键版）
        "lumi.remote.acn004": [
            "Aqara",
            "Wireless Remote Switch E1 (Double Rocker)",
            "WXKG17LM",
        ],
        # 无线开关D1（贴墙式双键版）
        "lumi.remote.b286acn02": [
            "Aqara",
            "Wireless Remote Switch D1 (Double Rocker)",
            "WXKG07LM",
        ],
        # 无线开关T1（贴墙式双键版）
        "lumi.remote.b286acn03": [
            "Aqara",
            "Wireless Remote Switch T1 (Double Rocker)",
            "",
        ],
        "params": [
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "button",
                        "device_class": EventDeviceClass.BUTTON,
                    },
                    MK_RESOURCES: {"button": ("13.{}.85", "_attr_trigger")},
                    MK_MAPPING_PARAMS: {"ch_count": 2},
                }
            }
        ],
    },
    ###无线四键
    {
        # 无线场景开关（四键版）
        "lumi.remote.b486opcn01": ["Aqara", "Wireless Remote Switch (Four Rocker)", ""],
        "params": [
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "button",
                        "device_class": EventDeviceClass.BUTTON,
                    },
                    MK_RESOURCES: {"button": ("13.{}.85", "_attr_trigger")},
                    MK_MAPPING_PARAMS: {"ch_count": 4},
                }
            }
        ],
    },
    ###无线六键
    {
        # 无线开关（六键版）
        "lumi.remote.b686opcn01": ["Aqara", "Wireless Remote Switch (Six Rocker)", ""],
        "params": [
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "button",
                        "device_class": EventDeviceClass.BUTTON,
                    },
                    MK_RESOURCES: {"button": ("13.{}.85", "_attr_trigger")},
                    MK_MAPPING_PARAMS: {"ch_count": 6},
                }
            }
        ],
    },
    ###无线旋钮
    {
        # 智能旋钮开关 H1（无线版）
        "lumi.remote.rkba01": ["Aqara", "Wireless rotary switch H1", ""],
        "params": [
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "button",
                        "device_class": EventDeviceClass.BUTTON,
                    },
                    MK_RESOURCES: {"button": ("13.1.85", "_attr_trigger")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "rotation_angle",
                        "device_class": "",
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": "°",
                    },
                    MK_RESOURCES: {"state": ("0.22.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "press_rotation_angle",
                        "device_class": "",
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": "°",
                    },
                    MK_RESOURCES: {"state": ("0.29.85", "_attr_native_value")},
                }
            },
        ],
    },
    ###############################传感器###########################################
    ###温湿度
    {
        # 小米温湿度传感器
        "lumi.sensor_ht.v1": ["Xiaomi", "TH Sensor", "WSDCGQ01LM"],
        # 温湿度传感器T1
        "lumi.sensor_ht.agl02": ["Aqara", "T1 TH Sensor", ""],
        # 温湿度传感器
        "lumi.weather.v1": ["Aqara", "TH Sensor", "WSDCGQ11LM"],
        "params": [
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "temperature",
                        "device_class": SensorDeviceClass.TEMPERATURE,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    },
                    MK_RESOURCES: {"temperature": ("0.1.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "humidity",
                        "device_class": SensorDeviceClass.HUMIDITY,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfRatio.PERCENTAGE,
                    },
                    MK_RESOURCES: {"humidity": ("0.2.85", "_attr_native_value")},
                }
            },
        ],
    },
    ### 空气质量
    {
        # TVOC空气健康伴侣
        "lumi.airmonitor.acn01": ["Aqara", "TVOC Sensor", ""],
        "params": [
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "temperature",
                        "device_class": SensorDeviceClass.TEMPERATURE,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    },
                    MK_RESOURCES: {"temperature": ("0.1.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "humidity",
                        "device_class": SensorDeviceClass.HUMIDITY,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfRatio.PERCENTAGE,
                    },
                    MK_RESOURCES: {"humidity": ("0.2.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "TVOC",
                        "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfRatio.PARTS_PER_BILLION,
                    },
                    MK_RESOURCES: {
                        "TVOC": (
                            "0.3.85",
                            "_attr_native_value",
                        )
                    },
                }
            },
        ],
    },
    ###光照传感器
    {
        # 光照传感器 T1
        "lumi.sen_ill.agl01": ["Aqara", "Light Sensor T1", ""],
        "params": [
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "illuminance",
                        "device_class": SensorDeviceClass.ILLUMINANCE,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": LIGHT_LUX,
                    },
                    MK_RESOURCES: {"illuminance": ("0.3.85", "_attr_native_value")},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "battery",
                        "device_class": SensorDeviceClass.BATTERY,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfRatio.PERCENTAGE,
                    },
                    MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
                }
            },
        ],
    },
    ###人体传感器
    {
        # 人体传感器
        "lumi.sensor_motion.v1": ["Xiaomi", "Motion Sensor", "RTCGQ01LM"],
        "lumi.sensor_motion.v2": ["Xiaomi", "Motion Sensor", "RTCGQ01LM"],
        # 人体传感器 P1
        "lumi.motion.ac02": ["Aqara", "Motion Sensor P1", ""],
        # 人体传感器 E1
        "lumi.motion.acn001": ["Aqara", "Motion Sensor E1", ""],
        "params": [
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "motion",
                        "device_class": BinarySensorDeviceClass.MOTION,
                    },
                    MK_RESOURCES: {
                        "motion": ("3.1.85", "_attr_native_value"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                    },
                }
            }
        ],
    },
    {
        # 人体传感器 带亮度
        "lumi.sensor_motion.aq2": ["Aqara", "Motion Sensor", "RTCGQ11LM"],
        # 人体传感器 T1
        "lumi.motion.agl02": ["Aqara", "Motion Sensor T1", ""],
        "params": [
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "motion",
                        "device_class": BinarySensorDeviceClass.MOTION,
                    },
                    MK_RESOURCES: {
                        "motion": ("3.1.85", "_attr_native_value"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                        "voltage": ("8.0.2008", "_attr_voltage"),
                    },
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "illuminance",
                        "device_class": SensorDeviceClass.ILLUMINANCE,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": LIGHT_LUX,
                        "entity_name": "Illuminance",
                    },
                    MK_RESOURCES: {"illumination": ("0.3.85", "_attr_native_value")},
                }
            },
        ],
    },
    ###高精度人体传感器
    {
        # 高精度人体传感器
        "lumi.motion.agl04": ["Aqara", "Precision Motion Sensor", "RTCGQ13LM"],
        "params": [
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "motion",
                        "device_class": BinarySensorDeviceClass.MOTION,
                    },
                    MK_RESOURCES: {
                        "motion": ("3.1.85", "_attr_native_value"),
                        "detect_time": ("8.0.2115", "_attr_detect_time"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                        "voltage": ("8.0.2008", "_attr_voltage"),
                    },
                }
            },
        ],
    },
    ###人体存在传感器
    {
        # 人体存在
        "lumi.motion.ac01": ["Aqara", "Presence Sensor FP1", "RTCZCGQ11LM"],
        # AI智能存在传感器 FP1E
        "lumi.sensor_occupy.agl1": ["Aqara", "Presence Sensor FP1E", ""],
        "params": [
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "device_class": BinarySensorDeviceClass.MOTION,
                    },
                    MK_RESOURCES: {
                        "exist": ("3.51.85", "_attr_is_on"),
                    },
                }
            },
            {
                "event": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "event_mapping": FP_MOTION_MAPPING,
                        "entity_name": "移动监测事件",
                    },
                    MK_RESOURCES: {
                        "event": ("13.27.85", "_attr_native_value"),
                    },
                }
            },
        ],
    },
    {
        # 人体场景传感器 FP2
        "lumi.motion.agl001": ["Aqara", "Presence Sensor FP2", ""],
        "params": [
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "device_class": BinarySensorDeviceClass.MOTION,
                        "entity_name": "Area",
                    },
                    MK_RESOURCES: {
                        "exist": ("3.{}.85", "_attr_is_on"),
                    },
                }
            },
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "default",
                        "device_class": BinarySensorDeviceClass.MOTION,
                        "entity_name": "All Area",
                    },
                    MK_RESOURCES: {
                        "exist": ("3.51.85", "_attr_is_on"),
                    },
                    MK_MAPPING_PARAMS: {"ch_count": None},
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "illuminance",
                        "device_class": SensorDeviceClass.ILLUMINANCE,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": LIGHT_LUX,
                        "entity_name": "Illuminance",
                    },
                    MK_RESOURCES: {"illumination": ("0.4.85", "_attr_native_value")},
                    MK_MAPPING_PARAMS: {"ch_count": None},
                }
            },
        ],
    },
    ###门窗传感器
    {
        # 门窗传感器
        "lumi.sensor_magnet.v1": ["Xiaomi", "Door Sensor", "MCCGQ01LM"],
        "lumi.sensor_magnet.v2": ["Xiaomi", "Door Sensor", "MCCGQ01LM"],
        "lumi.sensor_magnet.aq2": ["Aqara", "Door Sensor", "MCCGQ11LM"],
        # 门窗传感器T1
        "lumi.magnet.agl02": ["Aqara", "Door Sensor T1", "MCCGQ12LM"],
        # 门窗传感器E1
        "lumi.magnet.acn001": ["Aqara", "Door Sensor E1", "MCCGQ14LM"],
        # 门窗传感器P1
        "lumi.magnet.ac01": ["Aqara", "Door Sensor P1", "MCCGQ13LM"],
        "params": [
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "contact",
                        "device_class": BinarySensorDeviceClass.DOOR,
                    },
                    MK_RESOURCES: {
                        "status": ("3.1.85", "_attr_native_value"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                        "voltage": ("8.0.2008", "_attr_voltage"),
                    },
                }
            }
        ],
    },
    ###水浸传感器
    {
        # 水浸传感器
        "lumi.sensor_wleak.aq1": ["Aqara", "Water Leak Sensor", "SJCGQ11LM"],
        "lumi.sensor_wleak.v1": ["Aqara", "Water Leak Sensor", ""],
        "lumi.flood.agl02": ["Aqara", "Water Leak Sensor T1", "SJCGQ12LM"],
        "lumi.flood.acn001": ["Aqara", "Water Leak Sensor E1", "SJCGQ13LM"],
        "params": [
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "moisture",
                        "device_class": BinarySensorDeviceClass.MOISTURE,
                    },
                    MK_RESOURCES: {
                        "moisture": ("3.1.85", "_attr_is_on"),
                        "zigbee_lqi": ("8.0.2007", "_attr_zigbee_lqi"),
                        "voltage": ("8.0.2008", "_attr_voltage"),
                    },
                }
            }
        ],
    },
    ###烟雾传感器
    {
        # Xiaomi 烟雾报警器
        "lumi.sensor_smoke.v1": ["Xiaomi", "Smoke Sensor", "JTYJ-GD-01LM/BW"],
        "lumi.sensor_smoke.acn03": ["Xiaomi", "Smoke Sensor", ""],
        "params": [
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "smoke",
                        "device_class": BinarySensorDeviceClass.SMOKE,
                    },
                    MK_RESOURCES: {"smoke": ("13.1.85", "_attr_is_on")},
                }
            },
        ],
    },
    ###天然气传感器
    {
        # 天然气报警器
        "lumi.sensor_natgas.v1": ["Aqara", "Gas Alarm", ""],
        "params": [
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "gas",
                        "device_class": BinarySensorDeviceClass.GAS,
                    },
                    MK_RESOURCES: {"gas": ("13.1.85", "_attr_is_on")},
                }
            },
        ],
    },
    {
        # Aqara天然气报警器
        "lumi.sensor_gas.acn02": ["Aqara", "Gas Sensor", ""],
        "params": [
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "gas",
                        "device_class": SensorDeviceClass.GAS,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": "",
                    },
                    MK_RESOURCES: {"density": ("0.5.85", "_attr_native_value")},
                }
            },
        ],
    },
    ###############################门锁#############################################
    {
        # P100门锁
        "aqara.lock.wbzac1": ["Aqara", "DoorLock P100", ""],
        "params": [
            {
                "binary_sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "contact",
                        "device_class": BinarySensorDeviceClass.DOOR,
                    },
                    MK_RESOURCES: {
                        "status": ("13.12.85", "_attr_native_value"),
                    },
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "contact",
                        "device_class": "",
                        "state_class": "",
                        "unit_of_measurement": "",
                    },
                    MK_RESOURCES: {"status": ("13.2.85", "_attr_native_value")},
                }
            },
        ],
    },
    #################################空调、地暖####################################
    {
        # 空调伴侣 P3
        "lumi.aircondition.acn05": ["Aqara", "AC Partner P3", ""],
        "params": [
            {
                "climate": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "ac_partner_p3",
                        "supported_features": ClimateEntityFeature.TARGET_TEMPERATURE
                        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
                        | ClimateEntityFeature.FAN_MODE
                        | ClimateEntityFeature.PRESET_MODE
                        | ClimateEntityFeature.SWING_MODE
                        | ClimateEntityFeature.TURN_ON
                        | ClimateEntityFeature.TURN_OFF,
                        "max_temp": float(30),
                        "min_temp": float(16),
                        "hvac_modes": [
                            HVACMode.OFF,
                            HVACMode.HEAT,
                            HVACMode.COOL,
                            HVACMode.AUTO,
                            HVACMode.DRY,
                            HVACMode.FAN_ONLY,
                        ],
                        "fan_modes": [
                            FAN_AUTO,
                            FAN_LOW,
                            FAN_MEDIUM,
                            FAN_HIGH,
                        ],
                        "swing_modes": [
                            SWING_OFF,
                            SWING_ON,
                        ],
                        "preset_modes": [PRESET_NONE, PRESET_BOOST],
                        "temperature_unit": UnitOfTemperature.CELSIUS,
                        "target_temperature_step": float(1),
                    },
                    MK_RESOURCES: {
                        "ac_fun_ctl": ("8.0.2116", "_attr_native_value"),
                        "ac_quick_cool": ("4.4.85", "_attr_native_value"),
                        "ac_zip_mode": ("14.32.85", "_attr_native_value"),
                        "ac_on_off": ("3.1.85", "_attr_native_value"),
                    },
                }
            },
            {
                "switch": {
                    MK_INIT_PARAMS: {MK_HASS_NAME: "switch"},
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                    },
                }
            },
            {
                "sensor": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "power",
                        "device_class": SensorDeviceClass.POWER,
                        "state_class": SensorStateClass.MEASUREMENT,
                        "unit_of_measurement": UnitOfPower.WATT,
                    },
                    MK_RESOURCES: {"power": ("0.11.85", "_attr_native_value")},
                }
            },
        ],
    },
    {
        # 空调温控器
        "lumi.ctrl_hvac.es1": ["Aqara", "AC Controller", ""],
        "params": [
            {
                "climate": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "airrtc_tcpecn02",
                        "supported_features": ClimateEntityFeature.TARGET_TEMPERATURE
                        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
                        | ClimateEntityFeature.FAN_MODE
                        | ClimateEntityFeature.SWING_MODE
                        | ClimateEntityFeature.TURN_ON
                        | ClimateEntityFeature.TURN_OFF,
                        "max_temp": float(30),
                        "min_temp": float(16),
                        "hvac_modes": [
                            HVACMode.OFF,
                            HVACMode.HEAT,
                            HVACMode.COOL,
                            HVACMode.AUTO,
                            HVACMode.DRY,
                            HVACMode.FAN_ONLY,
                        ],
                        "fan_modes": [
                            FAN_AUTO,
                            FAN_LOW,
                            FAN_MEDIUM,
                            FAN_HIGH,
                        ],
                        "swing_modes": [
                            SWING_OFF,
                            SWING_ON,
                        ],
                        "temperature_unit": UnitOfTemperature.CELSIUS,
                        "target_temperature_step": float(1),
                    },
                    MK_RESOURCES: {
                        "ac_on_off": ("3.1.85", "_attr_native_value"),
                        "ac_state": ("14.2.85", "_attr_native_value"),
                    },
                }
            },
        ],
    },
    {
        # 空调温控器
        "lumi.airrtc.tcpecn01": ["Aqara", "AC Controller", ""],
        # 空调温控器 S2
        "lumi.airrtc.tcpecn02": ["Aqara", "AC Controller S2", ""],
        # 空调温控器（CO2）
        "lumi.airrtc.tcpco2ecn01": ["Aqara", "AC Controller CO2", ""],
        "params": [
            {
                "climate": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "airrtc_tcpecn02",
                        "supported_features": ClimateEntityFeature.TARGET_TEMPERATURE
                        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
                        | ClimateEntityFeature.FAN_MODE
                        | ClimateEntityFeature.SWING_MODE
                        | ClimateEntityFeature.TURN_ON
                        | ClimateEntityFeature.TURN_OFF,
                        "max_temp": float(30),
                        "min_temp": float(16),
                        "hvac_modes": [
                            HVACMode.OFF,
                            HVACMode.HEAT,
                            HVACMode.COOL,
                            HVACMode.AUTO,
                            HVACMode.DRY,
                            HVACMode.FAN_ONLY,
                        ],
                        "fan_modes": [
                            FAN_AUTO,
                            FAN_LOW,
                            FAN_MEDIUM,
                            FAN_HIGH,
                        ],
                        "swing_modes": [
                            SWING_OFF,
                            SWING_ON,
                        ],
                        "temperature_unit": UnitOfTemperature.CELSIUS,
                        "target_temperature_step": float(1),
                    },
                    MK_RESOURCES: {
                        "ac_on_off": ("3.1.85", "_attr_native_value"),
                        "ac_state": ("14.2.85", "_attr_native_value"),
                        "current_temperature": ("3.2.85", "_attr_current_temperature"),
                    },
                }
            },
        ],
    },
    {
        # 空调伴侣（升级版）
        "lumi.acpartner.v3": ["Aqara", "AC Partner V3", ""],
        "params": [
            {
                "climate": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "airrtc_tcpecn02",
                        "supported_features": ClimateEntityFeature.TARGET_TEMPERATURE
                        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
                        | ClimateEntityFeature.FAN_MODE
                        | ClimateEntityFeature.SWING_MODE
                        | ClimateEntityFeature.TURN_ON
                        | ClimateEntityFeature.TURN_OFF,
                        "max_temp": float(30),
                        "min_temp": float(16),
                        "hvac_modes": [
                            HVACMode.OFF,
                            HVACMode.HEAT,
                            HVACMode.COOL,
                            HVACMode.AUTO,
                            HVACMode.DRY,
                            HVACMode.FAN_ONLY,
                        ],
                        "fan_modes": [
                            FAN_AUTO,
                            FAN_LOW,
                            FAN_MEDIUM,
                            FAN_HIGH,
                        ],
                        "swing_modes": [
                            SWING_OFF,
                            SWING_ON,
                        ],
                        "temperature_unit": UnitOfTemperature.CELSIUS,
                        "target_temperature_step": float(1),
                    },
                    MK_RESOURCES: {
                        "ac_on_off": ("3.1.85", "_attr_native_value"),
                        "ac_state": ("14.10.85", "_attr_native_value"),
                    },
                }
            },
            {
                "switch": {
                    MK_INIT_PARAMS: {MK_HASS_NAME: "switch"},
                    MK_RESOURCES: {
                        "toggle": ("4.1.85", "_attr_is_on"),
                    },
                }
            },
        ],
    },
    {
        # 空调伴侣
        "lumi.acpartner.aq1": ["Aqara", "AC Partner", ""],
        # 空调伴侣
        "lumi.acpartner.es1": ["Aqara", "AC Partner", ""],
        "params": [
            {
                "climate": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "airrtc_tcpecn02",
                        "supported_features": ClimateEntityFeature.TARGET_TEMPERATURE
                        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
                        | ClimateEntityFeature.FAN_MODE
                        | ClimateEntityFeature.SWING_MODE
                        | ClimateEntityFeature.TURN_ON
                        | ClimateEntityFeature.TURN_OFF,
                        "max_temp": float(30),
                        "min_temp": float(16),
                        "hvac_modes": [
                            HVACMode.OFF,
                            HVACMode.HEAT,
                            HVACMode.COOL,
                            HVACMode.AUTO,
                            HVACMode.DRY,
                            HVACMode.FAN_ONLY,
                        ],
                        "fan_modes": [
                            FAN_AUTO,
                            FAN_LOW,
                            FAN_MEDIUM,
                            FAN_HIGH,
                        ],
                        "swing_modes": [
                            SWING_OFF,
                            SWING_ON,
                        ],
                        "temperature_unit": UnitOfTemperature.CELSIUS,
                        "target_temperature_step": float(1),
                    },
                    MK_RESOURCES: {
                        "ac_on_off": ("3.1.85", "_attr_native_value"),
                        "ac_state": ("14.10.85", "_attr_native_value"),
                    },
                }
            },
        ],
    },
    {
        # 温控伴侣 T1（室内机）
        "aqara.airrtc.acn02": ["Aqara", "Thermostat Partner T1", ""],
        "params": [
            {
                "climate": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "airrtc_acn02",
                        "supported_features": ClimateEntityFeature.TARGET_TEMPERATURE
                        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
                        | ClimateEntityFeature.FAN_MODE
                        | ClimateEntityFeature.TURN_ON
                        | ClimateEntityFeature.TURN_OFF,
                        "max_temp": float(30),
                        "min_temp": float(16),
                        "hvac_modes": [
                            HVACMode.OFF,
                            HVACMode.HEAT,
                            HVACMode.COOL,
                            HVACMode.AUTO,
                            HVACMode.DRY,
                            HVACMode.FAN_ONLY,
                        ],
                        "fan_modes": [
                            FAN_AUTO,
                            FAN_LOW,
                            FAN_MEDIUM,
                            FAN_HIGH,
                        ],
                        "temperature_unit": UnitOfTemperature.CELSIUS,
                        "target_temperature_step": float(1),
                    },
                    MK_RESOURCES: {
                        "ac_on_off": ("4.1.85", "_attr_native_value"),
                        "ac_temperature": ("1.1.85", "_attr_native_value"),
                        "ac_mode": ("14.140.85", "_attr_native_value"),
                        "ac_fan_mode": ("14.1.85", "_attr_native_value"),
                        "env_temperature": ("0.1.85", "_attr_native_value"),
                    },
                }
            },
        ],
    },
    {
        # 智能温控器 S3
        "lumi.airrtc.pcacn2": ["Aqara", "Thermostat S3", ""],
        "lumi.airrtc.pcacn2_thermostat": ["Aqara", "Thermostat S3", ""],
        "params": [
            {
                "climate": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "airrtc_pcacn2",
                        "supported_features": ClimateEntityFeature.TARGET_TEMPERATURE
                        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
                        | ClimateEntityFeature.FAN_MODE
                        | ClimateEntityFeature.TURN_ON
                        | ClimateEntityFeature.TURN_OFF,
                        "max_temp": float(30),
                        "min_temp": float(16),
                        "hvac_modes": [
                            HVACMode.OFF,
                            HVACMode.HEAT,
                            HVACMode.COOL,
                            HVACMode.FAN_ONLY,
                        ],
                        "fan_modes": [
                            FAN_AUTO,
                            FAN_LOW,
                            FAN_MEDIUM,
                            FAN_HIGH,
                        ],
                        "temperature_unit": UnitOfTemperature.CELSIUS,
                        "target_temperature_step": 0.5,
                    },
                    MK_RESOURCES: {
                        "ac_on_off": ("4.21.85", "_attr_native_value"),
                        "ac_temperature": ("1.8.85", "_attr_native_value"),
                        "ac_mode": ("14.51.85", "_attr_native_value"),
                        "ac_fan_mode": ("14.35.85", "_attr_native_value"),
                        "env_temperature": ("0.1.85", "_attr_native_value"),
                        "env_humidity": ("0.2.85", "_attr_native_value"),
                    },
                }
            },
        ],
    },
    {
        # 智能阀式温控器 E1
        "lumi.airrtc.agl001": ["Aqara", "Valve Thermostat E1", ""],
        "params": [
            {
                "climate": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "airrtc_agl001",
                        "supported_features": ClimateEntityFeature.TARGET_TEMPERATURE
                        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
                        | ClimateEntityFeature.TURN_ON
                        | ClimateEntityFeature.TURN_OFF,
                        "max_temp": float(30),
                        "min_temp": float(5),
                        "hvac_modes": [
                            HVACMode.OFF,
                            HVACMode.HEAT,
                        ],
                        "temperature_unit": UnitOfTemperature.CELSIUS,
                        "target_temperature_step": 0.5,
                    },
                    MK_RESOURCES: {
                        "ac_on_off": ("4.21.85", "_attr_native_value"),
                        "ac_temperature": ("1.8.85", "_attr_native_value"),
                        "ac_mode": ("14.51.85", "_attr_native_value"),
                        "env_temperature": ("0.1.85", "_attr_native_value"),
                    },
                }
            },
        ],
    },
    {
        # VRF空调控制器
        "lumi.airrtc.vrfegl01": ["Aqara", "VRF AC Controller", ""],
        "params": [
            {
                "climate": {
                    MK_INIT_PARAMS: {
                        MK_HASS_NAME: "airrtc_vrfegl01",
                        "supported_features": ClimateEntityFeature.TARGET_TEMPERATURE
                        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
                        | ClimateEntityFeature.FAN_MODE
                        | ClimateEntityFeature.SWING_MODE
                        | ClimateEntityFeature.TURN_ON
                        | ClimateEntityFeature.TURN_OFF,
                        "max_temp": float(30),
                        "min_temp": float(16),
                        "hvac_modes": [
                            HVACMode.OFF,
                            HVACMode.HEAT,
                            HVACMode.COOL,
                            HVACMode.AUTO,
                            HVACMode.DRY,
                            HVACMode.FAN_ONLY,
                        ],
                        "fan_modes": [
                            FAN_AUTO,
                            FAN_LOW,
                            FAN_MEDIUM,
                            FAN_HIGH,
                        ],
                        "swing_modes": [
                            SWING_OFF,
                            SWING_ON,
                        ],
                        "temperature_unit": UnitOfTemperature.CELSIUS,
                        "target_temperature_step": float(1),
                    },
                    MK_RESOURCES: {
                        "ac_state": ("14.{}.85", "_attr_native_value"),
                    },
                }
            },
        ],
    },
]
