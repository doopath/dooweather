import python_weather
import asyncio

from kivy.core.window import Window

from .daily_forecast.daily_forecasts_list import DailyForecastsList
from .forecast import Forecast
from .cities_dropdown_menu import CitiesDropdownMenu
from .cache import Cache
from . import constants
from .locales_dropdown_menu import LocalesDropdownMenu

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.button import MDRoundFlatButton


class Container(MDGridLayout):
    def __init__(self, cache: Cache, *args, **kwargs):
        self.locale = constants.LOCALE
        self.window = Window

        self.forecast_content: MDStackLayout
        self.input_field: MDLabel
        self.weather_info_label: MDLabel
        self.switch_locale_button: MDRoundFlatButton
        self.choose_city_button: MDRoundFlatButton

        super().__init__(*args, **kwargs)

        self.spacing = Window.height / 20

        self._forecast: Forecast
        self._cache = cache
        self._future_forecasts = []

        self.forecast_content.height = sum([i.height + Window.height \
            / 20 for i in self.forecast_content.children]) \
            + Window.height / 2.4

    async def _set_weather(self) -> None:
        async def inner():
            async with python_weather.Client(format=python_weather.IMPERIAL) as client:
                user_input = self.input_field.text
                user_input = user_input if user_input != '' else '0'
                weather = await client.get(user_input)
                forecast = Forecast(weather, user_input, self._cache)
                self._forecast = forecast
                self._update_current_forecast()

        await inner()

    def _set_location_set_weather(self, city: str) -> None:
        self.input_field.text = city
        self.set_weather()

    def _update_current_forecast(self) -> None:
        self.weather_info_label.text = self._forecast.beautified_current

    def _clean_future_forecasts(self) -> None:
        for forecast in self._future_forecasts:
            self.forecast_content.remove_widget(forecast)
            self.forecast_content.height -= (forecast.height + self.forecast_content.spacing[0])

        self._future_forecasts = []

    def _set_locale(self, locale: str) -> None:
        try:
            new_locale = constants.LOCALES[locale]
            constants.LOCALE, self.locale = new_locale, new_locale
            self._cache.set_value('LOCALE', locale)
        except KeyError:
            pass

    def _update_future_forecasts(self) -> None:
        self._clean_future_forecasts()
        index = len(self.forecast_content.children) - 1

        for forecast in self._forecast.beautified_future():
            card = DailyForecastsList.create_daily_forecast(forecast)
            self._future_forecasts.append(card)
            self.forecast_content.add_widget(card, index)
            self.forecast_content.height += card.height + self.forecast_content.spacing[1]

    def show_dropdown_menu(self, *_) -> None:
        dropdown_menu = CitiesDropdownMenu(
            self._set_location_set_weather, self._cache)
        dropdown_menu.caller = self.choose_city_button
        dropdown_menu.open()

    def set_weather(self) -> None:
        """
        Uses as an event handler.
        Is not intended for using by other modules.
        """
        self.weather_info_label.text = "Loading..."

        async def inner():
            await self._set_weather()
            self._update_future_forecasts()

        asyncio.run(inner())

    def temperature_switch(self) -> None:
        """
        Uses as an event handler.
        Is not intended for using by other modules.
        """
        try:
            self._forecast.switch_temperature_mode()
            self._update_current_forecast()
            self._update_future_forecasts()
        except AttributeError: ...


    def locale_switch(self) -> None:
        """
        Uses as an event handler.
        Is not intended for using by other modules.
        """
        dropdown_menu = LocalesDropdownMenu(self._set_locale)
        dropdown_menu.caller = self.switch_locale_button
        dropdown_menu.open()

