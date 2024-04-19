# This is the default settings used. Please do not modify unless you want to customise the GUI.

CITY_NAME = "New York"
STATE_CODE = None
COUNTRY_CODE = None
CITY_ID = None
LAT = None
LON = None
UNITS = None
LANGUAGE = None
CATEGORY = "current"



CURRENT_WEATHER_JSON = "CurrentWeather.json"
FORECAST_WEATHER_JSON = "ForecastedWeather.json"

SYMBOLS = {
    "standard": {
        "temp": "K",
        "speed": "m/s"
    },
    "metric": {
        "temp": "\u00b0C",
        "speed": "m/s"
    },
    "imperial": {
        "temp": "\u00b0F",
        "speed": "mph"
    }
}

SECOND = 1000
MINUTE = SECOND * 60
HOUR = MINUTE * 60

FONT_TYPE = "Arial"

FONT_DATE = 30
FONT_TIME = 50
FONT_SMALL_TIME = 25

FONT_CURRENT_TITLE = 32
FONT_LAST_GENERATED = 14
FONT_TEMP_NOW = 36
FONT_SUB_INFO = 24
FONT_OTHER_INFO = 18
FONT_FORECAST = 16


FORECAST_MAIN_SIZE = (80, 80)
FORECAST_SMALL_SIZE = (50, 50)
FORECAST_FRAME_PADX = 3