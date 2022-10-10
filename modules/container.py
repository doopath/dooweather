import python_weather
import asyncio
import threading

from kivy.core.window import Window

from modules.daily_forecasts_list import DailyForecastsList
from modules.forecast import Forecast
from kivymd.uix.gridlayout import MDGridLayout
from modules.input_dropdown_menu import InputDropdownMenu
from modules.cache import Cache


class Container(MDGridLayout):
    def __init__(self, cache: Cache, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spacing = Window.height / 20

        self._forecast: Forecast | None = None
        self._cache = cache
        self._feature_forecasts = []

        self.dropdown_menu = InputDropdownMenu(self._set_location_set_weather, self._cache)
        self.dropdown_menu.caller = self.choose_city_button

        self.forecast_content.height = sum([i.height + 50 for i in self.forecast_content.children]) \
                                       + Window.height / 3

    def _set_weather(self) -> None:
        async def inner():
            async with python_weather.Client(format=python_weather.IMPERIAL) as client:
                user_input = self.input_field.text
                user_input = user_input if user_input != '' else '0'
                weather = await client.get(user_input)
                forecast = Forecast(weather, user_input, self._cache)
                self._forecast = forecast
                self._update_current_forecast()

        asyncio.run(inner())

    def _set_location_set_weather(self, city: str) -> None:
        self.input_field.text = city
        self.set_weather()

    def _update_current_forecast(self) -> None:
        self.weather_info_label.text = self._forecast.beautified_current

    def _clean_feature_forecasts(self) -> None:
        for forecast in self._feature_forecasts:
            self.forecast_content.remove_widget(forecast)
            self.forecast_content.height -= (forecast.height + self.forecast_content.spacing[0])

        self._feature_forecasts = []

    def _update_feature_forecasts(self) -> None:
        self._clean_feature_forecasts()
        index = len(self.forecast_content.children) - 1

        for forecast in self._forecast.beautified_feature:
            card = DailyForecastsList.create_daily_forecast(forecast)
            self._feature_forecasts.append(card)
            self.forecast_content.add_widget(card, index)
            self.forecast_content.height += card.height + self.forecast_content.spacing[1]

    def show_dropdown_menu(self, *_) -> None:
        self.dropdown_menu.open()

    def set_weather(self) -> None:
        """
        Uses as an event handler.
        Is not intended for using by other modules.
        """
        self.weather_info_label.text = "Loading..."
        thread = threading.Thread(target=self._set_weather)
        thread.start()
        thread.join()
        self._update_feature_forecasts()

    def temperature_switch(self) -> None:
        """
        Uses as an event handler.
        Is not intended for using by other modules.
        """
        if self._forecast:
            self._forecast.switch_temperature_mode()
            self._update_current_forecast()
            self._update_feature_forecasts()
