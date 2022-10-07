from modules.forecast import Forecast
from kivymd.uix.gridlayout import MDGridLayout
from modules.input_dropdown_menu import InputDropdownMenu
import python_weather
import asyncio
import threading
from modules.cache import Cache


class Container(MDGridLayout):
    def __init__(self, cache: Cache, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._forecast: Forecast | None = None
        self._cache = cache

        self.dropdown_menu = InputDropdownMenu(self._set_location_set_weather, self._cache)
        self.dropdown_menu.caller = self.choose_city_button

    def _set_weather(self) -> None:
        async def inner():
            async with python_weather.Client(format=python_weather.IMPERIAL) as client:
                user_input = self.input_field.text
                user_input = user_input if user_input != '' else '0'
                weather = await client.get(user_input)
                forecast = Forecast(weather, user_input, self._cache)
                self._forecast = forecast
                self._update_weather()

        asyncio.run(inner())

    def _set_location_set_weather(self, city: str) -> None:
        self.input_field.text = city
        self.set_weather()

    def _update_weather(self) -> None:
        self.weather_info_label.text = self._forecast.beautified()

    def show_dropdown_menu(self, *_) -> None:
        self.dropdown_menu.open()

    def set_weather(self) -> None:
        """
        Uses as an event handler.
        Is not intended for using by other modules.
        """
        self.weather_info_label.text = "Loading..."
        threading.Thread(target=self._set_weather).start()

    def temperature_switch(self) -> None:
        """
        Uses as an event handler.
        Is not intended for using by other modules.
        """
        if self._forecast:
            self._forecast.switch_temperature_mode()
            self._update_weather()
