from modules.staticFunctions import *
from default import *
from config import *

class OpenWeatherAPI():

    def __init__(self, 
                 api_key=API_KEY,
                 city_name=CITY_NAME,
                 state_code=STATE_CODE,
                 country_code=COUNTRY_CODE,
                 city_id=CITY_ID,
                 lat=LAT,
                 lon=LON,
                 units=UNITS,
                 language=LANGUAGE,
                 category=CATEGORY) -> None:
        self.api_key = api_key
        self.units = units
        self.url = self.getURL(city_name, state_code, country_code, city_id, lat, lon, units, language, category)

    def getURL(self, city_name, state_code, country_code, city_id, lat, lon, units, language, category):
        
        url = f"https://api.openweathermap.org/data/2.5"

        # Get type of url
        if category == "current":
            url += f"/weather"
        elif category == "forecast":
            url += f"/forecast"

        # Details of city
        q = ",".join(str(item) for item in [
                    city_name, state_code, country_code] if item is not None)
        if lat != None and lon != None:
            url += f"?lat={lat}&lon={lon}"
        elif city_id != None:
            url += f"?id={city_id}"
        elif q:
            url += f"?q={q}"

        # Add API Key
        url += f"&appid={self.api_key}"

        # Additional Parameters
        if units != None:
            url += f"&units={units}"
        if language != None:
            url += f"&lang={language}"

        return url
    