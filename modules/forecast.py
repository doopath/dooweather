import python_weather.forecast
from python_weather.client import Weather
from modules.exceptions import (InvalidTemperatureFormatException)
from typing import AsyncGenerator
from modules.cache import Cache
from modules import constants


def fahrenheit_to_celsius(deg: int) -> int:
    """
    Covert Fahrenheit to celsius.

    Parameters
    ----------
    deg - celsius degrees as int.

    Returns
    -------
    Fahrenheit degrees int.
    """
    return round((deg - 32) * 5 / 9)


def celsius_to_fahrenheit(deg: int) -> int:
    """
    Covert Celsius to fahrenheit.

    Parameters
    ----------
    deg - fahrenheit degrees as int.

    Returns
    -------
    Celsius degrees int.
    """
    return round(deg * 9 / 5 + 32)


class CurrentForecast:
    def __init__(self, forecast: python_weather.forecast.CurrentForecast):
        self.temperature = forecast.temperature
        self.humidity = forecast.humidity
        self.feels_like = forecast.feels_like
        self.wind_speed = forecast.wind_speed
        self.wind_direction = forecast.wind_direction
        self.pressure = forecast.pressure


class DailyForecast:
    def __init__(self, forecast: python_weather.forecast.DailyForecast):
        self.temperature = forecast.temperature
        self.highest_temperature = forecast.highest_temperature
        self.lowest_temperature = forecast.lowest_temperature
        self.date = forecast.date


class Forecast:
    def __init__(self, forecast: Weather, city: str, cache: Cache):
        self._is_valid = False
        self._cache = cache
        self._check_if_valid(forecast)
        self.city = city
        self._current_forecast = CurrentForecast(forecast.current)
        self._future_forecasts = [DailyForecast(f) for f in forecast.forecasts]

        # TEMP_MODE is 'F' or 'C'
        try:
            self._temperature_mode = self._cache.get_value('TEMP_MODE')
        except KeyError:
            self._temperature_mode = 'F'
            self._cache.set_value('TEMP_MODE', 'F')

        if forecast.format != self._temperature_mode:
            self._switch_temperature_mode()
            self._convert_switched_temperature()
            self._switch_temperature_mode()

    def _check_if_valid(self, forecast: Weather) -> None:
        self._is_valid = bool(forecast.location)

    def _convert_forecasts_temperature_to_celsius(self) -> None:
        self._current_forecast.temperature = fahrenheit_to_celsius(self._current_forecast.temperature)
        self._current_forecast.feels_like = fahrenheit_to_celsius(self._current_forecast.feels_like)

        for forecast in self._future_forecasts:
            forecast.temperature = fahrenheit_to_celsius(forecast.temperature)
            forecast.lowest_temperature = fahrenheit_to_celsius(forecast.lowest_temperature)
            forecast.highest_temperature = fahrenheit_to_celsius(forecast.highest_temperature)

    def _convert_forecasts_temperature_to_fahrenheit(self) -> None:
        self._current_forecast.temperature = celsius_to_fahrenheit(self._current_forecast.temperature)
        self._current_forecast.feels_like = celsius_to_fahrenheit(self._current_forecast.feels_like)

        for forecast in self._future_forecasts:
            forecast.temperature = celsius_to_fahrenheit(forecast.temperature)
            forecast.lowest_temperature = celsius_to_fahrenheit(forecast.lowest_temperature)
            forecast.highest_temperature = celsius_to_fahrenheit(forecast.highest_temperature)

    def _convert_switched_temperature(self) -> None:
        if self._temperature_mode == 'F':
            self._convert_forecasts_temperature_to_celsius()
        elif self._temperature_mode == 'C':
            self._convert_forecasts_temperature_to_fahrenheit()
        else:
            raise InvalidTemperatureFormatException(
                "Temperature format can be only 'C' or 'F'!")

    def _switch_temperature_mode(self) -> None:
        if self._temperature_mode == 'F':
            self._temperature_mode = 'C'
            self._cache.set_value('TEMP_MODE', 'C')
        elif self._temperature_mode == 'C':
            self._temperature_mode = 'F'
            self._cache.set_value('TEMP_MODE', 'F')
        else:
            raise InvalidTemperatureFormatException(
                "Temperature format can be only 'C' or 'F'!")

    def _beautify_daily_forecast(self, forecast: DailyForecast) -> str:
        return f"{constants.LOCALE['CITY']}: {self.city}\n" + \
               f"{constants.LOCALE['DATE']}: {forecast.date}\n" + \
               f"{constants.LOCALE['TEMPERATURE']}: {forecast.temperature}{self._temperature_mode}\n" + \
               f"{constants.LOCALE['LOWEST_TEMPERATURE']}: {forecast.lowest_temperature}{self._temperature_mode}\n" + \
               f"{constants.LOCALE['HIGHEST_TEMPERATURE']}: {forecast.highest_temperature}{self._temperature_mode}\n"

    def _beautify_main_forecast(self, forecast: CurrentForecast) -> str:
        return f"{constants.LOCALE['CITY']}: {self.city}\n" + \
               f"{constants.LOCALE['TEMPERATURE']}: {forecast.temperature}{self._temperature_mode}" + \
               f" ({constants.LOCALE['FEELS_LIKE']} {forecast.feels_like}{self._temperature_mode})\n" + \
               f"{constants.LOCALE['HUMIDITY']}: {forecast.humidity}%\n" + \
               f"{constants.LOCALE['WIND_SPEED']}: {forecast.wind_speed} km/h\n" + \
               f"{constants.LOCALE['WIND_DIRECTION']}: {forecast.wind_direction}\n" + \
               f"{constants.LOCALE['PRESSURE']}: {forecast.pressure}"

    @property
    def beautified_current(self) -> str:
        """
        Formatted current forecast info.
        """
        if not self._is_valid:
            return constants.LOCALE['INVALID_LOCATION']

        try:
            cities: list = self._cache.get_value('CITIES')
        except KeyError:
            cities = []

        if self.city not in cities:
            cities.append(self.city)
            self._cache.set_value('CITIES', cities)

        return self._beautify_main_forecast(self._current_forecast)

    @property
    async def beautified_future(self) -> AsyncGenerator:
        """
        Formatted feature forecast info.
        """
        for forecast in self._future_forecasts:
            yield self._beautify_daily_forecast(forecast)

    def switch_temperature_mode(self) -> None:
        self._convert_switched_temperature()
        self._switch_temperature_mode()

