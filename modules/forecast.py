from python_weather.client import Weather
from exceptions import (InvalidTemperatureFormatException)


def fahrenheit_to_celsius(deg: int) -> int:
    return round((deg - 32) * 5 / 9)


def celsius_to_fahrenheit(deg: int) -> int:
    return round(deg * 9 / 5 + 32)


class Forecast():
    def __init__(self, forecast: Weather):
        self._is_valid = False
        self._check_if_valid(forecast)
        self._temperature_mode = 'F'  # or 'C'

        self.temperature = forecast.current.temperature
        self.humidity = forecast.current.humidity
        self.wind_speed = forecast.current.wind_speed
        self.wind_direction = forecast.current.wind_direction
        self.pressure = forecast.current.pressure
        self.feels_like = forecast.current.feels_like

    def _check_if_valid(self, forecast: Weather):
        self._is_valid = bool(forecast.location)

    def _convert_switched_temperature(self):
        if self._temperature_mode == 'F':
            self.temperature = fahrenheit_to_celsius(self.temperature)
            self.feels_like = fahrenheit_to_celsius(self.feels_like)
        elif self._temperature_mode == 'C':
            self.temperature = celsius_to_fahrenheit(self.temperature)
            self.feels_like = celsius_to_fahrenheit(self.feels_like)
        else:
            raise InvalidTemperatureFormatException(
                "Temperature format can be only 'C' or 'F'!")

    def beautified(self) -> str:
        if not self._is_valid:
            return "Invalid location!"

        return f"Temperature: {self.temperature}{self._temperature_mode}" +\
            f" (Feels like {self.feels_like}{self._temperature_mode})\n" +\
            f"Humidity: {self.humidity}%\n" +\
            f"Wind Speed: {self.wind_speed} km/h\n" +\
            f"Wind Direction: {self.wind_direction}\n" +\
            f"Pressure: {self.pressure}"

    def switch_temperature_mode(self):
        self._convert_switched_temperature()
        if self._temperature_mode == 'F':
            self._temperature_mode = 'C'
        elif self._temperature_mode == 'C':
            self._temperature_mode = 'F'
        else:
            raise InvalidTemperatureFormatException(
                "Temperature format can be only 'C' or 'F'!")
