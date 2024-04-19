from modules.OpenWeatherAPI import OpenWeatherAPI

from modules.staticFunctions import *
import json
from collections import Counter

from default import *
from config import *


class ForecastWeather(OpenWeatherAPI):

    def __init__(self, api_key=API_KEY,
                 city_name=CITY_NAME,
                 state_code=STATE_CODE,
                 country_code=COUNTRY_CODE,
                 city_id=CITY_ID,
                 lat=LAT,
                 lon=LON,
                 units=UNITS,
                 language=LANGUAGE,
                 category="forecast") -> None:
        super().__init__(api_key, city_name, state_code, country_code, city_id, lat, lon, units, language, category)
        getJSON(self.url, FORECAST_WEATHER_JSON)
        self.getInfo(FORECAST_WEATHER_JSON)
        self.getTodayForecast()
        self.getNextDaysForecast()

    def getInfo(self, file=FORECAST_WEATHER_JSON):
        """
        Information from https://openweathermap.org/forecast5
        """

        with open(FORECAST_WEATHER_JSON, "r") as file:
            data = json.load(file)

            self.all_info = ifAvailable(data, "list")       # Get all 40 forecasted data (every 3 hours)
            
            city = ifAvailable(data, "city")
            self.city_id = ifAvailable(city, "id")          # City ID
            self.city_name = ifAvailable(city, "name")      # City name
            self.city_coord = ifAvailable(city, "coord")    # Geo location, latitude & longitude
            self.city_coutry = ifAvailable(city, "country") # Country code (GB, JP etc.)
            self.city_population = ifAvailable(city, "population") # City population
            self.timezone = ifAvailable(city, "timezone")   # Shift in seconds from UTC
            self.sunrise = ifAvailable(city, "sunrise")     # Sunrise time, Unix, UTC
            self.sunset = ifAvailable(city, "sunset")       # Sunset time, Unix, UTC

            # Sort data into days from today, and run self.allocateDays(allList)
            self.plus0Day = []  # Today
            self.plus1Day = []  # Tomorrow
            self.plus2Day = []  # + 2 days
            self.plus3Day = []  # + 3 days
            self.plus4Day = []  # + 4 days
            self.plus5Day = []  # + 5 days

            # separate items with info, and arrange them according to their days with self.day.append with getDate == currentDay
            self.allocateDays(self.all_info)

            self.unit_symbol = SYMBOLS[self.units] if self.units in SYMBOLS else SYMBOLS["standard"]
            

    def allocateDays(self, allLists: list):

        # Get days in Unix format (converted to timestamp)
        self.dt_now = datetime.datetime.now()
        day_plus0 = (self.dt_now + datetime.timedelta(days=0)).timestamp()
        day_plus1 = (self.dt_now + datetime.timedelta(days=1)).timestamp()
        day_plus2 = (self.dt_now + datetime.timedelta(days=2)).timestamp()
        day_plus3 = (self.dt_now + datetime.timedelta(days=3)).timestamp()
        day_plus4 = (self.dt_now + datetime.timedelta(days=4)).timestamp()
        day_plus5 = (self.dt_now + datetime.timedelta(days=5)).timestamp()

        # Sort items into their respective days
        for item in allLists:
            day = ifAvailable(item, "dt")

            if day != None:
                # Adjust time error
                item["dt"] -= self.timezone 
                day -= self.timezone

                if getDate(day_plus0) == getDate(day):
                    self.plus0Day.append(item)
                elif getDate(day_plus1) == getDate(day):
                    self.plus1Day.append(item)
                elif getDate(day_plus2) == getDate(day):
                    self.plus2Day.append(item)
                elif getDate(day_plus3) == getDate(day):
                    self.plus3Day.append(item)
                elif getDate(day_plus4) == getDate(day):
                    self.plus4Day.append(item)
                elif getDate(day_plus5) == getDate(day):
                    self.plus5Day.append(item)

                
    
    def getTodayForecast(self):

        sunrise_info = {
            "type": "sunrise", 
            "dt": self.sunrise
        }

        sunset_info = {
            "type": "sunset", 
            "dt": self.sunset
        }

        temp_sunrise = (datetime.datetime.fromtimestamp(self.sunrise) + datetime.timedelta(days=1)).timestamp()
        temp_sunrise_info = {
            "type": "sunrise", 
            "dt": temp_sunrise
        }

        """Append Sunrise if valid"""
        if self.sunrise != None: 
            if self.dt_now.timestamp() > self.sunrise: # Sunrise has passed
                pass
            elif self.dt_now.timestamp() <= self.sunrise and self.sunrise <= self.plus0Day[0]["dt"]: # Sunrise is the next coming forecast
                self.plus0Day.insert(0, sunrise_info)
            else:
                for i in range(len(self.plus0Day)): # Else, find an appropriate placement for the info
                    if self.plus0Day[i]["dt"] < self.sunrise and self.sunrise <= self.plus0Day[i+1]["dt"]:
                        self.plus0Day.insert(i, sunrise_info)
                        break
        

        """Append Sunset if valid"""
        if self.sunset != None: 
            if self.dt_now.timestamp() > self.sunset: # Sunrise has passed
                pass
            elif self.dt_now.timestamp() <= self.sunset and self.sunset <= self.plus0Day[0]["dt"]: # Sunrise is the next coming forecast
                self.plus0Day.insert(0, sunset_info)
            elif self.sunset > self.plus0Day[-1]["dt"]: # Sunrise is after last item on the forecast
                self.plus0Day.append(sunset_info)
            else:
                for i in range(len(self.plus0Day)): # Else, find an appropriate placement for the info
                    if self.plus0Day[i]["dt"] < self.sunset and self.sunset <= self.plus0Day[i+1]["dt"]:
                        self.plus0Day.insert(i+1, sunset_info)
                        break

                

        """Get Today Forecast"""
        len_ = 6
        if len(self.plus0Day) >= len_:
            self.todayForecast = self.plus0Day[:len_]
        else: 
            self.todayForecast = self.plus0Day + self.plus1Day[:len_ - len(self.plus0Day)]

        # Add temporary sunrise when appropriate
        for i in range(len_-1):
            if self.todayForecast[i]["dt"] < temp_sunrise and temp_sunrise <= self.todayForecast[i+1]["dt"]:
                self.todayForecast.insert(i+1, temp_sunrise_info)
                self.todayForecast.pop()
                break






    def getNextDaysForecast(self):
        """Get forecast of next few days"""

        # Get information
        day1 = self.getDayInfo(self.plus1Day)
        day2 = self.getDayInfo(self.plus2Day)
        day3 = self.getDayInfo(self.plus3Day)
        day4 = self.getDayInfo(self.plus4Day)
        day5 = self.getDayInfo(self.plus5Day)

        # Summarise info
        day1 = self.summariseForecastInfo(day1)
        day2 = self.summariseForecastInfo(day2)
        day3 = self.summariseForecastInfo(day3)
        day4 = self.summariseForecastInfo(day4)
        day5 = self.summariseForecastInfo(day5)
        
        self.nextDaysForecast = [day1, day2, day3, day4, day5]

    @staticmethod
    def getDayInfo(day) -> dict:
        """To be used for + 1-5 days"""

        dayInfo = {
            "dt": [],
            "temp": [],
            "temp_min": [],
            "temp_max": [],
            "humidity": [],
            "weather_id": [],
            "weather_main": [],
            "weather_desc": [],
            "weather_icon": [],
            "cloudiness": [],
            "wind_speed": [],
            "wind_deg": [],
            "wind_gust": [],
            "visibility": [],
            "precipitation": [],
            "rain_3h": [],
            "snow_3h": [],
        }

        for hourly in day:
            if "sunrise" not in day:
                dayInfo["dt"].append(ifAvailable(hourly, "dt"))

                main = ifAvailable(hourly, "main")
                dayInfo["temp"].append(ifAvailable(main, "temp"))
                # dayInfo["temp_min"].append(ifAvailable(main, "temp_min"))
                # dayInfo["temp_max"].append(ifAvailable(main, "temp_max"))
                dayInfo["humidity"].append(ifAvailable(main, "humidity"))

                weather = ifAvailable(hourly, "weather")
                dayInfo["weather_id"].append(ifAvailable(weather[0], "id"))
                dayInfo["weather_main"].append(ifAvailable(weather[0], "main"))
                dayInfo["weather_desc"].append(ifAvailable(weather[0], "description"))
                dayInfo["weather_icon"].append(ifAvailable(weather[0], "icon"))

                clouds = ifAvailable(hourly, "clouds")
                dayInfo["cloudiness"].append(ifAvailable(clouds, "all"))

                wind = ifAvailable(hourly, "wind")
                dayInfo["wind_speed"].append(ifAvailable(wind, "speed"))
                dayInfo["wind_deg"].append(ifAvailable(wind, "deg"))
                dayInfo["wind_gust"].append(ifAvailable(wind, "gust"))

                dayInfo["visibility"].append(ifAvailable(hourly, "visibility"))

                dayInfo["precipitation"].append(ifAvailable(hourly, "pop"))

                rain = ifAvailable(hourly, "rain")
                dayInfo["rain_3h"].append(ifAvailable(rain, "3h"))

                snow = ifAvailable(hourly, "snow")
                dayInfo["snow_3h"].append(ifAvailable(snow, "3h"))

        for key, values in dayInfo.items():
            dayInfo[key] = list(filter(lambda x: x is not None, values))

        return dayInfo
    
    @staticmethod
    def summariseForecastInfo(data) -> dict:

        for key, values in data.items():
            if key in ["dt", "temp_min", "temp_max"]: # To ignore these keys
                pass
            elif values == []: # If nothing in value, return none
                data[key] = None
            elif key == "temp": # Get min & max temp
                data["temp_min"] = min(values)
                data["temp_max"] = max(values)
            else: # Find max or most frequent values
                if key == "weather_id" or isinstance(values[0], str):
                    data[key] = Counter(values).most_common()[0][0]
                elif isinstance(values[0], int):
                    data[key] = max(values)
                elif isinstance(values[0], float):
                    data[key] = max(values)
        return data



class FWGetTodayForecast:

    def __init__(self, data) -> None:
        self.getInfo(data)

    def getInfo(self, data):
        self.type = ifAvailable(data, "type") # Get type of data: Sunrise, Sunset or None

        self.dt = ifAvailable(data, "dt")       # Time of data forecasted, unix, UTC

        if self.type is None:
            main = ifAvailable(data, "main")
            self.temp = ifAvailable(main, "temp")               # Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
            self.feels_like = ifAvailable(main, "feels_like")   # This temperature parameter accounts for the human perception of weather. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
            self.temp_min = ifAvailable(main, "temp_min")       # Minimum temperature at the moment of calculation. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
            self.temp_max = ifAvailable(main, "temp_max")       # Maximum temperature at the moment of calculation. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
            self.pressure = ifAvailable(main, "pressure")       # Atmospheric pressure on the sea level by default, hPa
            self.sea_level = ifAvailable(main, "sea_level")     # Atmospheric pressure on the sea level, hPa
            self.grnd_level = ifAvailable(main, "grnd_level")   # Atmospheric pressure on the ground level, hPa
            self.humidity = ifAvailable(main, "humidity")       # Humidity, %
            self.temp_kf = ifAvailable(main, "temp_kf")         # Internal parameter

            weather = ifAvailable(data, "weather")
            self.weather_id = ifAvailable(weather[0], "id")             # Weather condition id
            self.weather_main = ifAvailable(weather[0], "main")         # Group of weather parameters (Rain, Snow, Clouds etc.)
            self.weather_desc = ifAvailable(weather[0], "description")  # Weather condition within the group. 
            self.weather_icon = ifAvailable(weather[0], "icon")         # Weather icon id

            clouds = ifAvailable(data, "clouds")
            self.cloudiness = ifAvailable(clouds, "all")        # Cloudiness, %

            wind = ifAvailable(data, "wind")
            self.wind_speed = ifAvailable(wind, "speed")    # Wind speed. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour
            self.wind_deg = ifAvailable(wind, "deg")        # Wind direction, degrees (meteorological)
            self.wind_gust = ifAvailable(wind, "gust")      # Wind gust. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour

            self.visibility = ifAvailable(data, "visibility")   # Average visibility, metres. The maximum value of the visibility is 10km

            self.precipitation = ifAvailable(data, "pop")   # Probability of precipitation. The values of the parameter vary between 0 and 1, where 0 is equal to 0%, 1 is equal to 100%

            rain = ifAvailable(data, "rain")
            self.rain_3h = ifAvailable(rain, "3h")      # Rain volume for last 3 hours, mm. Please note that only mm as units of measurement are available for this parameter

            snow = ifAvailable(data, "snow")
            self.snow_3h = ifAvailable(snow, "3h")      # Snow volume for last 3 hours. Please note that only mm as units of measurement are available for this parameter



class FWGetNextDaysForecast():

    def __init__(self, data) -> None:
        self.getInfo(data)

    def getInfo(self, data):

        self.dt = ifAvailable(data, "dt")
        self.temp = ifAvailable(data, "temp")
        self.temp_min = ifAvailable(data, "temp_min")
        self.temp_max = ifAvailable(data, "temp_max")
        self.weather_id = ifAvailable(data, "weather_id")
        self.weather_main = ifAvailable(data, "weather_main")
        self.weather_desc = ifAvailable(data, "weather_desc")
        self.weather_icon = ifAvailable(data, "weather_icon")
        self.wind_speed = ifAvailable(data, "wind_speed")
        self.wind_deg = ifAvailable(data, "wind_deg")
        self.wind_gust = ifAvailable(data, "wind_gust")
        self.visibility = ifAvailable(data, "visibility")
        self.precipitation = ifAvailable(data, "precipitation")
        self.rain_3h = ifAvailable(data, "rain_3h")
        self.snow_3h = ifAvailable(data, "snow_3h")
        self.type = None

            

            

