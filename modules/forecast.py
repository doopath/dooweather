from python_weather.client import Weather
from modules.exceptions import (InvalidTemperatureFormatException)
from modules.cache import Cache


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


class Forecast:
    def __init__(self, forecast: Weather, city: str, cache: Cache):
        self._is_valid = False
        self._cache = cache
        self._check_if_valid(forecast)

        self.city = city
        self.temperature = forecast.current.temperature
        self.humidity = forecast.current.humidity
        self.wind_speed = forecast.current.wind_speed
        self.wind_direction = forecast.current.wind_direction
        self.pressure = forecast.current.pressure
        self.feels_like = forecast.current.feels_like

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

    def _convert_switched_temperature(self) -> None:
        if self._temperature_mode == 'F':
            self.temperature = fahrenheit_to_celsius(self.temperature)
            self.feels_like = fahrenheit_to_celsius(self.feels_like)
        elif self._temperature_mode == 'C':
            self.temperature = celsius_to_fahrenheit(self.temperature)
            self.feels_like = celsius_to_fahrenheit(self.feels_like)
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

    def beautified(self) -> str:
        """
        Returns
        -------
        Formatted temperature info.
        """
        if not self._is_valid:
            return "Invalid location!"

        cities: list = self._cache.get_value('CITIES')

        if self.city not in cities:
            cities.append(self.city)
            self._cache.set_value('CITIES', cities)

        return f"City: {self.city}\n" +\
            f"Temperature: {self.temperature}{self._temperature_mode}" +\
            f" (Feels like {self.feels_like}{self._temperature_mode})\n" +\
            f"Humidity: {self.humidity}%\n" +\
            f"Wind Speed: {self.wind_speed} km/h\n" +\
            f"Wind Direction: {self.wind_direction}\n" +\
            f"Pressure: {self.pressure}"

    def switch_temperature_mode(self) -> None:
        self._convert_switched_temperature()
        self._switch_temperature_mode()
