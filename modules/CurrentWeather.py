
from modules.OpenWeatherAPI import OpenWeatherAPI
from default import *
from config import *
from modules.staticFunctions import *
import json


class CurrentWeather(OpenWeatherAPI):
    
    def __init__(self, api_key=API_KEY,
                 city_name=CITY_NAME,
                 state_code=STATE_CODE,
                 country_code=COUNTRY_CODE,
                 city_id=CITY_ID,
                 lat=LAT,
                 lon=LON,
                 units=UNITS,
                 language=LANGUAGE,
                 category="current") -> None:
        super().__init__(api_key, city_name, state_code, country_code, city_id, lat, lon, units, language, category)
        getJSON(self.url, CURRENT_WEATHER_JSON)
        self.getCurrentInfo(CURRENT_WEATHER_JSON)

    def getCurrentInfo(self, file=CURRENT_WEATHER_JSON):
        """
        Information from https://openweathermap.org/current
        """

        with open(CURRENT_WEATHER_JSON, "r") as file:
            data = json.load(file)

            # Coordinates
            coord = ifAvailable(data, "coord")
            self.lon = ifAvailable(coord, "lon")     # Longitude of the location
            self.lat = ifAvailable(coord, "lat")     # Latitude of the location

            # Weather
            weather = ifAvailable(data, "weather")
            self.weather_id = ifAvailable(weather[0], "id")             # Weather condition id
            self.weather_main = ifAvailable(weather[0], "main")         # Group of weather parameters (Rain, Snow, Clouds etc.)
            self.weather_desc = ifAvailable(weather[0], "description")  # Weather condition within the group.
            self.weather_icon = ifAvailable(weather[0], "icon")         # Weather icon id

            # Main weather info
            main = ifAvailable(data, "main")
            self.temp = ifAvailable(main, "temp")               # Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
            self.feels_like = ifAvailable(main, "feels_like")   # Temperature. This temperature parameter accounts for the human perception of weather. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
            self.pressure = ifAvailable(main, "pressure")       # Atmospheric pressure on the sea level, hPa
            self.humidity = ifAvailable(main, "humidity")       # Humidity, %
            self.temp_min = ifAvailable(main, "temp_min")       # Minimum temperature at the moment. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
            self.temp_max = ifAvailable(main, "temp_max")       # Maximum temperature at the moment. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
            self.sea_level = ifAvailable(main, "sea_level")     # Atmospheric pressure on the sea level, hPa
            self.grnd_level = ifAvailable(main, "grnd_level")   # Atmospheric pressure on the ground level, hPa

            # Visibiliy
            self.visibility = ifAvailable(data, "visibility") # Visibility, meter. The maximum value of the visibility is 10 km

            # Wind
            wind = ifAvailable(data, "wind")
            self.wind_speed = ifAvailable(wind, "speed")    # Wind speed. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour
            self.wind_deg = ifAvailable(wind, "deg")        # Wind direction, degrees (meteorological)
            self.wind_gust = ifAvailable(wind, "gust")      # Wind gust. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour
            self.wind_dir = self.getWindDir(self.wind_deg)

            # Clouds
            clouds = ifAvailable(data, "clouds")
            self.cloudiness = ifAvailable(clouds, "all")     # Cloudiness, %

            # Rain
            rain = ifAvailable(data, "rain")
            self.rain_1h = ifAvailable(rain, "1h") # Rain volume for the last 1 hour, mm.
            self.rain_3h = ifAvailable(rain, "3h") # Rain volume for the last 3 hours, mm.

            # Snow
            snow = ifAvailable(data, "snow")
            self.snow_1h = ifAvailable(snow, "1h") # Snow volume for the last 1 hour, mm.
            self.snow_3h = ifAvailable(snow, "3h") # Snow volume for the last 3 hours, mm.

            # Time of data extraction
            self.dt = ifAvailable(data, "dt")      # Time of data calculation, unix, UTC

            # System, timezone, ID and city name
            sys = ifAvailable(data, "sys")              
            self.country = ifAvailable(sys, "country")      # Country code (GB, JP etc.)
            self.sunrise = ifAvailable(sys, "sunrise")      # Sunrise time, unix, UTC
            self.sunset = ifAvailable(sys, "sunset")        # Sunset time, unix, UTC
            self.timezone = ifAvailable(data, "timezone")   # Shift in seconds from UTC
            self.city_id = ifAvailable(data, "id")               # City ID
            self.city_name = ifAvailable(data, "name")           # City name

            self.unit_symbol = SYMBOLS[self.units] if self.units in SYMBOLS else SYMBOLS["standard"]

    
    @staticmethod
    def getWindDir(wind_deg: int):
        """Get wind direction"""
        if wind_deg is not None:
            if 22.5 < wind_deg and wind_deg <= 67.5:
                return "NE"
            elif 67.5 < wind_deg and wind_deg <= 112.5:
                return "E"
            elif 112.5 < wind_deg and wind_deg <= 157.5:
                return "SE"
            elif 157.5 < wind_deg and wind_deg <= 202.5:
                return "S"
            elif 202.5 < wind_deg and wind_deg <= 247.5:
                return "SW"
            elif 247.5 < wind_deg and wind_deg <= 292.5:
                return "W"
            elif 292.5 < wind_deg and wind_deg <= 337.5:
                return "NW"
            else:
                # wind_deg < 22.5 or wind_deg > 337.5
                return "N" 
        else:
            return None
