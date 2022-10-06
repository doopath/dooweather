from modules.forecast import Forecast
from kivymd.uix.gridlayout import MDGridLayout
import python_weather
import asyncio
import threading
from modules.cache import Cache


class Container(MDGridLayout):
    def __init__(self, cache: Cache, *args, **kwargs):
        self._forecast: Forecast = None
        self._cache = cache
        super().__init__(*args, **kwargs)

    def set_weather(self):
        self.weather_info_label.text = "Loading..."
        threading.Thread(target=self._set_weather).start()

    def temperature_switch(self):
        self._forecast.switch_temperature_mode()
        self._update_weather()

    def _set_weather(self):
        async def inner():
            async with python_weather.Client(format=python_weather.IMPERIAL) as client:
                user_input = self.input_field.text
                user_input = user_input if user_input != '' else '0'
                weather = await client.get(user_input)
                forecast = Forecast(weather, self._cache)
                self._forecast = forecast
                self._update_weather()

        asyncio.run(inner())

    def _update_weather(self):
        self.weather_info_label.text = self._forecast.beautified()
