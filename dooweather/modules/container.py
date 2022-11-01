from aiohttp.client_exceptions import ClientConnectionError
import python_weather
import asyncio

from kivy.core.window import Window

from .colorscheme import Colorscheme
from .forecast import Forecast
from .dropdown_menu.cities_dropdown_menu import CitiesDropdownMenu
from .dropdown_menu.locales_dropdown_menu import LocalesDropdownMenu
from .dropdown_menu.themes_dropdown_menu import ThemesDropdownMenu
from .cache import Cache
from . import constants
from .daily_forecast.daily_forecasts_list import DailyForecastsList

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.button import MDRoundFlatButton


class Container(MDGridLayout):
    def __init__(self, cache: Cache, colorscheme: Colorscheme, *args, **kwargs):
        self.locale = constants.LOCALE
        self.window = Window
        self.colorscheme = colorscheme

        self.forecast_content: MDStackLayout
        self.input_field: MDLabel
        self.weather_info_label: MDLabel
        self.switch_locale_button: MDRoundFlatButton
        self.switch_theme_button: MDRoundFlatButton
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

    def _set_theme(self, theme: str) -> None:
        try:
            new_theme = constants.COLORSCHEMES[theme]
            self.colorscheme = new_theme
            self._cache.set_value('THEME', theme)
        except KeyError:
            pass

    def _update_future_forecasts(self) -> None:
        self._clean_future_forecasts()
        index = len(self.forecast_content.children) - 1

        for forecast in self._forecast.beautified_future():
            card = DailyForecastsList.create_daily_forecast(forecast, self.colorscheme)
            self._future_forecasts.append(card)
            self.forecast_content.add_widget(card, index)
            self.forecast_content.height += card.height + self.forecast_content.spacing[1]

    def set_weather(self) -> None:
        """
        Uses as an event handler.
        Is not intended for using by other modules.
        """
        self.weather_info_label.text = "Loading..."

        async def inner():
            try:
                await self._set_weather()
                self._update_future_forecasts()
            except ClientConnectionError:
                self.weather_info_label.text = self.locale['NO_CONNECTION_MESSAGE']

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
        dropdown_menu = LocalesDropdownMenu(update=self._set_locale)
        dropdown_menu.caller = self.switch_locale_button
        dropdown_menu.open()

    def theme_switch(self) -> None:
        """
        Uses as an event handler.
        Is not intended for using by other modules.
        """
        dropdown_menu = ThemesDropdownMenu(update=self._set_theme)
        dropdown_menu.caller = self.switch_theme_button
        dropdown_menu.open()

    def city_select(self, *_) -> None:
        dropdown_menu = CitiesDropdownMenu(
            update=self._set_location_set_weather,
            cache=self._cache)
        dropdown_menu.caller = self.choose_city_button
        dropdown_menu.open()

