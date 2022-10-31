"""
    Module that provides a class to create a list of daily forecasts.
"""
from .daily_forecast_card import Card
from ..colorscheme import Colorscheme
from kivymd.uix.card import MDCard


class DailyForecastsList:
    @staticmethod
    def create_daily_forecast(forecast_info: str, colorscheme: Colorscheme) -> MDCard:
        return Card(forecast_info, colorscheme)

    @staticmethod
    def create_daily_forecasts_list(forecasts: list[str], colorscheme: Colorscheme) -> list[Card]:
        return [DailyForecastsList.create_daily_forecast(f, colorscheme) for f in forecasts]
