"""Constants for the Aqara Bridge component."""

DOMAIN = "aqara_bridge"

# Config flow fields
CONF_FIELD_ACCOUNT = "field_account"
CONF_FIELD_COUNTRY_CODE = "field_country_code"
CONF_FIELD_AUTH_CODE = "field_auth_code"
CONF_FIELD_SELECTED_DEVICES = "field_selected_devices"
CONF_FIELD_REFRESH_TOKEN = "field_refresh_token"
CONF_FIELD_APP_ID = "field_app_id"
CONF_FIELD_APP_KEY = "field_app_key"
CONF_FIELD_KEY_ID = "field_key_id"
CONF_OCCUPANCY_TIMEOUT = "occupancy_timeout"

# Cloud
SERVER_COUNTRY_CODES = ["CN", "USA", "KR", "RU", "GER"]
SERVER_COUNTRY_CODES_DEFAULT = "CN"
DEFAULT_CLOUD_APP_ID = ""
DEFAULT_CLOUD_APP_KEY = ""
DEFAULT_CLOUD_KEY_ID = ""

# CONFIG ENTRY
CONF_ENTRY_APP_ID = "app_id"
CONF_ENTRY_APP_KEY = "app_key"
CONF_ENTRY_KEY_ID = "key_id"
CONF_ENTRY_AUTH_ACCOUNT = "account"
CONF_ENTRY_AUTH_ACCOUNT_TYPE = "account_type"
CONF_ENTRY_AUTH_COUNTRY_CODE = "country_code"
CONF_ENTRY_AUTH_EXPIRES_IN = "expires_in"
CONF_ENTRY_AUTH_EXPIRES_TIME = "expires_datetime"
CONF_ENTRY_AUTH_ACCESS_TOKEN = "access_token"
CONF_ENTRY_AUTH_REFRESH_TOKEN = "refresh_token"
CONF_ENTRY_AUTH_OPENID = "open_id"
# CONFIG ENTRY OPTIONS，未设置时接入所有支持的设备
CONF_ENTRY_DEVICES = "devices"

# HASS DATA
HASS_DATA_AUTH_ENTRY_ID = "auth_entry_id"
HASS_DATA_AIOTCLOUD = "aiotcloud"
HASS_DATA_AIOT_MANAGER = "aiot_manager"

ATTR_FIRMWARE_VERSION = "firmware_version"
ATTR_ZIGBEE_LQI = "zigbee_lqi"
ATTR_VOLTAGE = "voltage"


PROP_TO_ATTR_BASE = {
    "firmware_version": ATTR_FIRMWARE_VERSION,
    "zigbee_lqi": ATTR_ZIGBEE_LQI,
    "voltage": ATTR_VOLTAGE,
}

# Air Quality Monitor
ATTR_CO2E = "carbon_dioxide_equivalent"
ATTR_TVOC = "total_volatile_organic_compounds"
ATTR_HUMIDITY = "humidity"

# Switch Sensor
# https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/converters/fromZigbee.js#L4738
BUTTON = {
    "1": "single",
    "2": "double",
    "3": "triple",
    "4": "quadruple",
    "16": "hold",
    "17": "release",
    "18": "shake",
    "20": "reversing_rotate",
    "21": "hold_rotate",
    "22": "clockwise",
    "23": "counterclockwise",
    "24": "hold_clockwise",
    "25": "hold_counterclockwise",
    "26": "rotate",
    "27": "hold_rotate",
    "128": "many",
}

BUTTON_BOTH = {
    "4": "single",
    "5": "double",
    "6": "triple",
    "16": "hold",
    "17": "release",
}

VIBRATION = {
    "1": "vibration",
    "2": "tilt",
    "3": "drop",
}

CUBE = {
    "0": "flip90",
    "1": "flip180",
    "2": "move",
    "3": "knock",
    "4": "quadruple",
    "16": "rotate",
    "20": "shock",
    "28": "hold",
    "move": "move",
    "flip90": "flip90",
    "flip180": "flip180",
    "rotate": "rotate",
    "alert": "alert",
    "shake_air": "shock",
    "tap_twice": "knock",
}

# 智能摄像机G3（网关版）
GESTURE_MAPPING = {
    "2": "二",
    "4": "四",
    "5": "五",
    "6": "八",
    "10": "好(OK)",
    "101": "二(双手)",
    "102": "四(双手)",
    "103": "五(双手)",
    "104": "八(双手)",
    "105": "好(OK)(双手)",
}

PET_MAPPING = {"1": "猫", "2": "狗", "3": "猫狗"}
HUMAN_MAPPING = {"0": "无人", "1": "有人"}
MOVING_MAPPING = {"0": "未侦测到移动", "1": "侦测到移动"}
SOUND_MAPPING = {"0": "无异常声音", "1": "有异常声音"}
DOORBELL_MAPPING = {"1": "ring"}

# 卡农开关
KN_BUTTON_MAPPING = {"1": "single", "2": "double", "3": "hold"}

KN_BUTTON_3_MAPPING = {"1": "single", "2": "double", "16": "hold"}

KN_SLIDE_MAPPING = {
    "0": "空闲",
    "1": "单击",
    "2": "双击",
    "3": "三击",
    "4": "滑动",
    "16": "长按按下",
    "17": "长按释放",
    "20": "旋转中",
    "21": "按住旋转中",
    "22": "顺时针旋转停止",
    "23": "逆时针旋转停止",
    "24": "按住顺时针旋转停止",
    "25": "按住逆时针旋转停止",
    "26": "旋转开始",
    "27": "按住旋转开始",
}

# 人体存在传感器
FP_MOTION_MAPPING = {
    "0": "进入",
    "1": "离开",
    "2": "左进",
    "3": "右出",
    "4": "右进",
    "5": "左出",
    "6": "接近",
    "7": "远离",
}
