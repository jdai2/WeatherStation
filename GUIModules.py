import tkinter as tk
import datetime
from PIL import Image, ImageTk
import os

from modules.CurrentWeather import CurrentWeather
from modules.ForecastWeather import ForecastWeather, FWGetTodayForecast, FWGetNextDaysForecast
from modules.staticFunctions import *
from default import *
from config import *

class GUIModules:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("WeatherStation Display")
        self.root.geometry("1024x600")  # size of display

        self.GUIdatetime()
        self.GUIWeatherDisplay()


        self.root.mainloop()

    ### Datetime
    def GUIdatetime(self):
        self.dt_frame = tk.Frame(self.root)
        self.dt_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor='nw')

        self.date_label = tk.Label(self.dt_frame, font=(FONT_TYPE, FONT_DATE))
        self.date_label.pack()

        self.time_label = tk.Label(self.dt_frame, font=(FONT_TYPE, FONT_TIME))
        self.time_label.pack(anchor="w")

        self.update_datetime()

    def update_datetime(self):
        """Update datetime every second"""
        now = datetime.datetime.now()
        self.date_label.config(text=now.strftime('%d %B %Y, %A'))
        self.time_label.config(text=now.strftime('%H:%M'))

        # Schedule the update_time function to run after 1000 milliseconds (1 second)
        self.root.after(SECOND, self.update_datetime)


    ### Weather Display
    def GUIWeatherDisplay(self):
        self.weatherDisplay = tk.Frame(self.root)
        self.weatherDisplay.pack(side=tk.TOP, padx=10, pady=10, anchor='ne')

        self.GUIgetCurrentWeather()
        self.GUIgetForecast()
        
    ### For Current Weather
    def GUIgetCurrentWeather(self):
        """Current Weather Frame"""
        self.cw_frame = tk.Frame(self.weatherDisplay)
        self.cw_frame.pack(side=tk.TOP, padx=0, pady=2, anchor='n')

        # Frame: Introduction & City
        self.cwText_frame1 = tk.Frame(self.cw_frame)
        self.cwText_frame1.pack(side=tk.TOP, anchor='n')
        self.cwText0a = tk.Label(self.cw_frame, font=(FONT_TYPE, FONT_CURRENT_TITLE))
        self.cwText0a.pack(anchor="w")

        # Frame: Information
        self.cw_midFrame = tk.Frame(self.cw_frame)
        self.cw_midFrame.pack(side=tk.TOP, anchor='n')
        self.GUIgetCWWeather()
        self.GUIgetCWTemp()
        self.GUIgetCWOtherInfo()

        # Frame: Generated Time
        self.cwText_frame2 = tk.Frame(self.cw_frame)
        self.cwText_frame2.pack(side=tk.TOP)
        self.cwText0b = tk.Label(self.cw_frame, font=(FONT_TYPE, FONT_LAST_GENERATED))
        self.cwText0b.pack(anchor="e")

        self.update_CurrentWeather()
    
    def GUIgetCWTemp(self):
        self.cwTemp_frame = tk.Frame(self.cw_midFrame)
        self.cwTemp_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor='w')

        # Labels
        self.cwTempMain = tk.Label(self.cwTemp_frame, font=(FONT_TYPE + " bold", FONT_TEMP_NOW))
        self.cwWeatherDesc = tk.Label(self.cwTemp_frame, font=(FONT_TYPE, FONT_SUB_INFO))
        self.cwTempLnH = tk.Label(self.cwTemp_frame, font=(FONT_TYPE, FONT_SUB_INFO))
        
        # Label packer
        for item in [self.cwTempMain,
                     self.cwWeatherDesc,
                     self.cwTempLnH]:
            item.pack(anchor="sw")

    def GUIgetCWWeather(self):
        self.cwWeather_frame = tk.Frame(self.cw_midFrame)
        self.cwWeather_frame.pack(side=tk.LEFT, anchor='w')

        # Labels
        self.cwWeatherIcon = tk.Label(self.cwWeather_frame)

        # Label packer
        for item in [self.cwWeatherIcon]:
            item.pack()

    def GUIgetCWOtherInfo(self): 
        self.cwOther_frame = tk.Frame(self.cw_midFrame)
        self.cwOther_frame.pack(side=tk.LEFT, padx=5, anchor='w')

        # Labels
        self.cwHumidity = tk.Label(self.cwOther_frame, font=(FONT_TYPE, FONT_OTHER_INFO)) 
        self.cwTempFeelsLike = tk.Label(self.cwOther_frame, font=(FONT_TYPE, FONT_OTHER_INFO)) 
        self.cwWind = tk.Label(self.cwOther_frame, font=(FONT_TYPE, FONT_OTHER_INFO))
        self.cwCloudiness = tk.Label(self.cwOther_frame,font=(FONT_TYPE, FONT_OTHER_INFO))
        # self.cwVisibility = tk.Label(self.cwOther_frame, font=(FONT_TYPE, FONT_OTHER_INFO)) 
        self.cwRain1h = tk.Label(self.cwOther_frame, font=(FONT_TYPE, FONT_OTHER_INFO)) 
        self.cwSnow1h = tk.Label(self.cwOther_frame, font=(FONT_TYPE, FONT_OTHER_INFO))
        
        # Packer
        for item in [self.cwHumidity, 
                     self.cwTempFeelsLike,
                     self.cwWind,
                     self.cwCloudiness,
                    #  self.cwVisibility,
                     ]:
            item.pack(anchor="w")
        
    def update_CurrentWeather(self):
        """Update Current Weather every hour"""
        self.currentData = CurrentWeather()
        now = datetime.datetime.now().timestamp()

        temp_symbol = self.currentData.unit_symbol['temp']
        speed_symbol = self.currentData.unit_symbol['speed']

        # Main Frame
        self.cwText0a.config(text=f"In {self.currentData.city_name},")
        self.cwText0b.config(text=f"last updated {'today' if getDate(self.currentData.dt) == getDate(now) else f'on {getDate(self.currentData.dt)}'} at {getTime(self.currentData.dt)}")

        # Midframe: Temperature
        self.cwTempMain.config(text=f"{self.currentData.temp:.1f}{temp_symbol}")
        self.cwWeatherDesc.config(text=f"{self.currentData.weather_desc.capitalize()}")
        self.cwTempLnH.config(text=f"L: {round(self.currentData.temp_min)}{temp_symbol} H: {round(self.currentData.temp_max)}{temp_symbol}")

        # Midframe: Weather & Icon
        path = os.path.join("icons", f"{self.currentData.weather_icon}.png")
        img = Image.open(path).resize(FORECAST_MAIN_SIZE)
        image = ImageTk.PhotoImage(img)
        self.cwWeatherIcon.config(image=image)
        self.cwWeatherIcon.image = image

        # Midframe: Other Info
        self.cwHumidity.config(text=f"{'Humidity:'} {self.currentData.humidity} %")
        self.cwTempFeelsLike.config(text=f"Feels like: {round(self.currentData.feels_like)}{temp_symbol}")
        self.cwWind.config(text=f"{'Wind:'} {self.currentData.wind_speed} {speed_symbol} {self.currentData.wind_dir}")
        self.cwCloudiness.config(text=f"{'Cloudiness:'} {self.currentData.cloudiness} %")
        # self.cwVisibility.config(text=f"{'Visibility:'} {(self.currentData.visibility/1000):.1f} km")
        self.cwRain1h.config(text=f"{'Rain:'} {self.currentData.rain_1h} mm")
        self.cwSnow1h.config(text=f"{'Snow:'} {self.currentData.snow_1h} mm")


        # Custom packer
        # If there is value for rain
        if self.currentData.rain_1h is not None:
            self.cwRain1h.pack(anchor="w")
        
        # If there is value for snow
        if self.currentData.snow_1h is not None:
            self.cwSnow1h.pack(anchor="w")

        self.root.after(HOUR, self.update_CurrentWeather)

    ### For Forecast
    def GUIgetForecast(self):
        self.forecastData = ForecastWeather()

        # Get frames
        self.GUIgetHourlyForecast()
        self.GUIgetNextDaysForecast()

        # Update every 3 hours
        self.update_HourlyForecast()
        self.update_NextDaysForecast()

    ### - Get hourly forecast
    def GUIgetHourlyForecast(self):
        self.hf_mainFrame = tk.Frame(self.weatherDisplay)
        self.hf_mainFrame.pack(side=tk.TOP, padx=5, pady=5, anchor='w')

        self.hfText_frame = tk.Frame(self.hf_mainFrame)
        self.hfText_frame.pack(side=tk.TOP, anchor='w')
        self.hfText_label1 = tk.Label(self.hf_mainFrame,
                            text=f"Today's Forecast", 
                            font=(FONT_TYPE, FONT_OTHER_INFO))
        self.hfText_label1.pack(anchor="w")

        self.GUIgetHourlyFrame1()
        self.GUIgetHourlyFrame2()
        self.GUIgetHourlyFrame3()
        self.GUIgetHourlyFrame4()
        self.GUIgetHourlyFrame5()

    def GUIgetHourlyFrame1(self):
        self.hf_frame1 = tk.Frame(self.hf_mainFrame)
        self.hf_frame1.pack(side=tk.LEFT, padx=FORECAST_FRAME_PADX)

        # Labels
        self.hf_image1 = tk.Label(self.hf_frame1)
        self.hf_text1a = tk.Label(self.hf_frame1, font=(FONT_TYPE, FONT_FORECAST))
        self.hf_text1b = tk.Label(self.hf_frame1, font=(FONT_TYPE, FONT_FORECAST))
        self.hf_text1c = tk.Label(self.hf_frame1, font=(FONT_TYPE, FONT_FORECAST))

        # Packer
        for item in [self.hf_image1, 
                     self.hf_text1a,
                     self.hf_text1b,
                     self.hf_text1c]:
            item.pack()

    def GUIgetHourlyFrame2(self):
        self.hf_frame2 = tk.Frame(self.hf_mainFrame)
        self.hf_frame2.pack(side=tk.LEFT, padx=FORECAST_FRAME_PADX)

        # Labels
        self.hf_image2 = tk.Label(self.hf_frame2)
        self.hf_text2a = tk.Label(self.hf_frame2, font=(FONT_TYPE, FONT_FORECAST))
        self.hf_text2b = tk.Label(self.hf_frame2, font=(FONT_TYPE, FONT_FORECAST))
        self.hf_text2c = tk.Label(self.hf_frame2, font=(FONT_TYPE, FONT_FORECAST))

        # Packer
        for item in [self.hf_image2, 
                     self.hf_text2a,
                     self.hf_text2b,
                     self.hf_text2c]:
            item.pack()

    def GUIgetHourlyFrame3(self):
        self.hf_frame3 = tk.Frame(self.hf_mainFrame)
        self.hf_frame3.pack(side=tk.LEFT, padx=FORECAST_FRAME_PADX)

        # Labels
        self.hf_image3 = tk.Label(self.hf_frame3)
        self.hf_text3a = tk.Label(self.hf_frame3, font=(FONT_TYPE, FONT_FORECAST))
        self.hf_text3b = tk.Label(self.hf_frame3, font=(FONT_TYPE, FONT_FORECAST))
        self.hf_text3c = tk.Label(self.hf_frame3, font=(FONT_TYPE, FONT_FORECAST))

        # Packer
        for item in [self.hf_image3, 
                     self.hf_text3a,
                     self.hf_text3b,
                     self.hf_text3c]:
            item.pack()

    def GUIgetHourlyFrame4(self):
        self.hf_frame4 = tk.Frame(self.hf_mainFrame)
        self.hf_frame4.pack(side=tk.LEFT, padx=FORECAST_FRAME_PADX)

        # Labels
        self.hf_image4 = tk.Label(self.hf_frame4)
        self.hf_text4a = tk.Label(self.hf_frame4, font=(FONT_TYPE, FONT_FORECAST))
        self.hf_text4b = tk.Label(self.hf_frame4, font=(FONT_TYPE, FONT_FORECAST))
        self.hf_text4c = tk.Label(self.hf_frame4, font=(FONT_TYPE, FONT_FORECAST))

        # Packer
        for item in [self.hf_image4, 
                     self.hf_text4a,
                     self.hf_text4b,
                     self.hf_text4c]:
            item.pack()

    def GUIgetHourlyFrame5(self):
        self.hf_frame5 = tk.Frame(self.hf_mainFrame)
        self.hf_frame5.pack(side=tk.LEFT, padx=FORECAST_FRAME_PADX)

        # Labels
        self.hf_image5 = tk.Label(self.hf_frame5)
        self.hf_text5a = tk.Label(self.hf_frame5, font=(FONT_TYPE, FONT_FORECAST))
        self.hf_text5b = tk.Label(self.hf_frame5, font=(FONT_TYPE, FONT_FORECAST))
        self.hf_text5c = tk.Label(self.hf_frame5, font=(FONT_TYPE, FONT_FORECAST))

        # Packer
        for item in [self.hf_image5, 
                     self.hf_text5a,
                     self.hf_text5b,
                     self.hf_text5c]:
            item.pack()

    def update_HourlyForecast(self):
        self.update_HourlyForecast_Frame1()
        self.update_HourlyForecast_Frame2()
        self.update_HourlyForecast_Frame3()
        self.update_HourlyForecast_Frame4()
        self.update_HourlyForecast_Frame5()

        self.root.after(3 * HOUR, self.update_HourlyForecast)

    def update_HourlyForecast_Frame1(self):
        temp_symbol = self.forecastData.unit_symbol["temp"]

        data = FWGetTodayForecast(self.forecastData.todayForecast[0])
        image = self.getImage(data)

        self.hf_image1.config(image=image)
        self.hf_image1.image = image
        self.hf_text1a.config(text=f"    {getTime(data.dt)}    ")
        
        # If data has temperature and precipitation
        if data.type is None:
            self.hf_text1b.config(text=f"{data.temp:.1f}{temp_symbol}")
            # If there is precipitation
            if data.precipitation != 0:
                self.hf_text1c.config(text=f"{data.precipitation*100:.0f}% ppt")
            else:
                self.hf_text1c.config(text=f"")
        else:
            self.hf_text1b.config(text=f"{data.type.capitalize()}")
            self.hf_text1c.config(text=f"")

    def update_HourlyForecast_Frame2(self):
        temp_symbol = self.forecastData.unit_symbol["temp"]

        data = FWGetTodayForecast(self.forecastData.todayForecast[1])
        image = self.getImage(data)

        self.hf_image2.config(image=image)
        self.hf_image2.image = image
        self.hf_text2a.config(text=f"    {getTime(data.dt)}    ")
        
        # If data has temperature and precipitation
        if data.type is None:
            self.hf_text2b.config(text=f"{data.temp:.1f}{temp_symbol}")
            # If there is precipitation
            if data.precipitation != 0:
                self.hf_text2c.config(text=f"{data.precipitation*100:.0f}% ppt")
            else:
                self.hf_text2c.config(text=f"")
        else:
            self.hf_text2b.config(text=f"{data.type.capitalize()}")
            self.hf_text2c.config(text=f"")

    def update_HourlyForecast_Frame3(self):
        temp_symbol = self.forecastData.unit_symbol["temp"]

        data = FWGetTodayForecast(self.forecastData.todayForecast[2])
        image = self.getImage(data)

        self.hf_image3.config(image=image)
        self.hf_image3.image = image
        self.hf_text3a.config(text=f"    {getTime(data.dt)}    ")
        
        # If data has temperature and precipitation
        if data.type is None:
            self.hf_text3b.config(text=f"{data.temp:.1f}{temp_symbol}")
            # If there is precipitation
            if data.precipitation != 0:
                self.hf_text3c.config(text=f"{data.precipitation*100:.0f}% ppt")
            else:
                self.hf_text3c.config(text=f"")
        else:
            self.hf_text3b.config(text=f"{data.type.capitalize()}")
            self.hf_text3c.config(text=f"")

    def update_HourlyForecast_Frame4(self):
        temp_symbol = self.forecastData.unit_symbol["temp"]

        data = FWGetTodayForecast(self.forecastData.todayForecast[3])
        image = self.getImage(data)

        self.hf_image4.config(image=image)
        self.hf_image4.image = image
        self.hf_text4a.config(text=f"    {getTime(data.dt)}    ")
        
        # If data has temperature and precipitation
        if data.type is None:
            self.hf_text4b.config(text=f"{data.temp:.1f}{temp_symbol}")
            # If there is precipitation
            if data.precipitation != 0:
                self.hf_text4c.config(text=f"{data.precipitation*100:.0f}% ppt")
            else:
                self.hf_text4c.config(text=f"")
        else:
            self.hf_text4b.config(text=f"{data.type.capitalize()}")
            self.hf_text4c.config(text=f"")

    def update_HourlyForecast_Frame5(self):
        temp_symbol = self.forecastData.unit_symbol["temp"]

        data = FWGetTodayForecast(self.forecastData.todayForecast[4])
        image = self.getImage(data)

        self.hf_image5.config(image=image)
        self.hf_image5.image = image
        self.hf_text5a.config(text=f"    {getTime(data.dt)}    ")
        
        # If data has temperature and precipitation
        if data.type is None:
            self.hf_text5b.config(text=f"{data.temp:.1f}{temp_symbol}")
            # If there is precipitation
            if data.precipitation != 0:
                self.hf_text5c.config(text=f"{data.precipitation*100:.0f}% ppt")
            else:
                self.hf_text5c.config(text=f"")
        else:
            self.hf_text5b.config(text=f"{data.type.capitalize()}")
            self.hf_text5c.config(text=f"")

    ### - Get next day forecast
    def GUIgetNextDaysForecast(self):
        self.ndf_mainFrame = tk.Frame(self.weatherDisplay)
        self.ndf_mainFrame.pack(side=tk.TOP, padx=5, pady=5, anchor='w')

        self.ndfText_frame = tk.Frame(self.ndf_mainFrame)
        self.ndfText_frame.pack(side=tk.TOP, anchor='w')
        self.ndfText_label1 = tk.Label(self.ndf_mainFrame,
                            text=f"{len(self.forecastData.nextDaysForecast)}-Day Forecast", 
                            font=(FONT_TYPE, FONT_OTHER_INFO))
        self.ndfText_label1.pack(anchor="w")

        self.GUIgetNextDayFrame1()
        self.GUIgetNextDayFrame2()
        self.GUIgetNextDayFrame3()
        self.GUIgetNextDayFrame4()
        self.GUIgetNextDayFrame5()

    def GUIgetNextDayFrame1(self):
        self.ndf_frame1 = tk.Frame(self.ndf_mainFrame)
        self.ndf_frame1.pack(side=tk.LEFT, padx=FORECAST_FRAME_PADX)

        # Labels
        self.ndf_image1 = tk.Label(self.ndf_frame1)
        self.ndf_text1a = tk.Label(self.ndf_frame1, font=(FONT_TYPE, FONT_FORECAST))
        self.ndf_text1b = tk.Label(self.ndf_frame1, font=(FONT_TYPE, FONT_FORECAST))
        self.ndf_text1c = tk.Label(self.ndf_frame1, font=(FONT_TYPE, FONT_FORECAST))

        # Packer
        for item in [self.ndf_image1, 
                     self.ndf_text1a,
                     self.ndf_text1b,
                     self.ndf_text1c,]:
            item.pack()

    def GUIgetNextDayFrame2(self):
        self.ndf_frame2 = tk.Frame(self.ndf_mainFrame)
        self.ndf_frame2.pack(side=tk.LEFT, padx=FORECAST_FRAME_PADX)

        # Labels
        self.ndf_image2 = tk.Label(self.ndf_frame2)
        self.ndf_text2a = tk.Label(self.ndf_frame2, font=(FONT_TYPE, FONT_FORECAST))
        self.ndf_text2b = tk.Label(self.ndf_frame2, font=(FONT_TYPE, FONT_FORECAST))
        self.ndf_text2c = tk.Label(self.ndf_frame2, font=(FONT_TYPE, FONT_FORECAST))

        # Packer
        for item in [self.ndf_image2, 
                     self.ndf_text2a,
                     self.ndf_text2b,
                     self.ndf_text2c,]:
            item.pack()

    def GUIgetNextDayFrame3(self):
        self.ndf_frame3 = tk.Frame(self.ndf_mainFrame)
        self.ndf_frame3.pack(side=tk.LEFT, padx=FORECAST_FRAME_PADX)

        # Labels
        self.ndf_image3 = tk.Label(self.ndf_frame3)
        self.ndf_text3a = tk.Label(self.ndf_frame3, font=(FONT_TYPE, FONT_FORECAST))
        self.ndf_text3b = tk.Label(self.ndf_frame3, font=(FONT_TYPE, FONT_FORECAST))
        self.ndf_text3c = tk.Label(self.ndf_frame3, font=(FONT_TYPE, FONT_FORECAST))

        # Packer
        for item in [self.ndf_image3, 
                     self.ndf_text3a,
                     self.ndf_text3b,
                     self.ndf_text3c,]:
            item.pack()

    def GUIgetNextDayFrame4(self):
        self.ndf_frame4 = tk.Frame(self.ndf_mainFrame)
        self.ndf_frame4.pack(side=tk.LEFT, padx=FORECAST_FRAME_PADX)

        # Labels
        self.ndf_image4 = tk.Label(self.ndf_frame4)
        self.ndf_text4a = tk.Label(self.ndf_frame4, font=(FONT_TYPE, FONT_FORECAST))
        self.ndf_text4b = tk.Label(self.ndf_frame4, font=(FONT_TYPE, FONT_FORECAST))
        self.ndf_text4c = tk.Label(self.ndf_frame4, font=(FONT_TYPE, FONT_FORECAST))

        # Packer
        for item in [self.ndf_image4, 
                     self.ndf_text4a,
                     self.ndf_text4b,
                     self.ndf_text4c,]:
            item.pack()

    def GUIgetNextDayFrame5(self):
        self.ndf_frame5 = tk.Frame(self.ndf_mainFrame)
        self.ndf_frame5.pack(side=tk.LEFT, padx=FORECAST_FRAME_PADX)

        # Labels
        self.ndf_image5 = tk.Label(self.ndf_frame5)
        self.ndf_text5a = tk.Label(self.ndf_frame5, font=(FONT_TYPE, FONT_FORECAST))
        self.ndf_text5b = tk.Label(self.ndf_frame5, font=(FONT_TYPE, FONT_FORECAST))
        self.ndf_text5c = tk.Label(self.ndf_frame5, font=(FONT_TYPE, FONT_FORECAST))

        # Packer
        for item in [self.ndf_image5, 
                     self.ndf_text5a,
                     self.ndf_text5b,
                     self.ndf_text5c,]:
            item.pack()

    def update_NextDaysForecast(self):
        self.update_NextDaysFrame1()
        self.update_NextDaysFrame2()
        self.update_NextDaysFrame3()
        self.update_NextDaysFrame4()
        self.update_NextDaysFrame5()

        self.root.after(3 * HOUR, self.update_HourlyForecast)

    def update_NextDaysFrame1(self):
        temp_symbol = self.forecastData.unit_symbol["temp"]

        data = FWGetNextDaysForecast(self.forecastData.nextDaysForecast[0])

        image = self.getImage(data)
        self.ndf_image1.config(image=image)
        self.ndf_image1.image = image

        self.ndf_text1a.config(text=f" Tomorrow ")
        self.ndf_text1b.config(text=f"{round(data.temp_min)}{temp_symbol} / {round(data.temp_max)}{temp_symbol}")

        # If there is precipitation
        if data.precipitation != 0:
            self.ndf_text1c.config(text=f"{data.precipitation*100:.0f}% ppt")
        else:
            self.ndf_text1c.config(text=f"")

    def update_NextDaysFrame2(self):
        temp_symbol = self.forecastData.unit_symbol["temp"]

        data = FWGetNextDaysForecast(self.forecastData.nextDaysForecast[1])

        image = self.getImage(data)
        self.ndf_image2.config(image=image)
        self.ndf_image2.image = image

        self.ndf_text2a.config(text=f"     {getDay(data.dt[0]):.3s}     ")
        self.ndf_text2b.config(text=f"{round(data.temp_min)}{temp_symbol} / {round(data.temp_max)}{temp_symbol}")

        # If there is precipitation
        if data.precipitation != 0:
            self.ndf_text2c.config(text=f"{data.precipitation*100:.0f}% ppt")
        else:
            self.ndf_text2c.config(text=f"")

    def update_NextDaysFrame3(self):
            temp_symbol = self.forecastData.unit_symbol["temp"]

            data = FWGetNextDaysForecast(self.forecastData.nextDaysForecast[2])

            image = self.getImage(data)
            self.ndf_image3.config(image=image)
            self.ndf_image3.image = image

            self.ndf_text3a.config(text=f"     {getDay(data.dt[0]):.3s}     ")
            self.ndf_text3b.config(text=f"{round(data.temp_min)}{temp_symbol} / {round(data.temp_max)}{temp_symbol}")

            # If there is precipitation
            if data.precipitation != 0:
                self.ndf_text3c.config(text=f"{data.precipitation*100:.0f}% ppt")
            else:
                self.ndf_text3c.config(text=f"")

    def update_NextDaysFrame4(self):
        temp_symbol = self.forecastData.unit_symbol["temp"]

        data = FWGetNextDaysForecast(self.forecastData.nextDaysForecast[3])

        image = self.getImage(data)
        self.ndf_image4.config(image=image)
        self.ndf_image4.image = image

        self.ndf_text4a.config(text=f"     {getDay(data.dt[0]):.3s}     ")
        self.ndf_text4b.config(text=f"{round(data.temp_min)}{temp_symbol} / {round(data.temp_max)}{temp_symbol}")

        # If there is precipitation
        if data.precipitation != 0:
            self.ndf_text4c.config(text=f"{data.precipitation*100:.0f}% ppt")
        else:
            self.ndf_text4c.config(text=f"")
    
    def update_NextDaysFrame5(self):
        temp_symbol = self.forecastData.unit_symbol["temp"]

        try:
            data = FWGetNextDaysForecast(self.forecastData.nextDaysForecast[4])
        except Exception:
            self.ndf_image5.config()
            self.ndf_text5a.config(text=f"")
            self.ndf_text5b.config(text=f"")
            self.ndf_text5c.config(text=f"")
        else:
            image = self.getImage(data)
            self.ndf_image5.config(image=image)
            self.ndf_image5.image = image

            self.ndf_text5a.config(text=f"     {getDay(data.dt[0]):.3s}     ")
            self.ndf_text5b.config(text=f"{round(data.temp_min)}{temp_symbol} / {round(data.temp_max)}{temp_symbol}")

            # If there is precipitation
            if data.precipitation != 0:
                self.ndf_text5c.config(text=f"{data.precipitation*100:.0f}% ppt")
            else:
                self.ndf_text5c.config(text=f"")


    @staticmethod
    def getImage(data):
        if data.type is None: # Normal
            icon = data.weather_icon
        elif "sunset" == data.type: # Sunset
            icon = "sunset"
        else:   # Sunrise
            icon = "sunrise"
        
        icon_path = os.path.join("icons", f"{icon}.png")
        img = Image.open(icon_path).resize(FORECAST_SMALL_SIZE)
        image = ImageTk.PhotoImage(img)

        return image



if __name__ == "__main__":
    GUIModules()