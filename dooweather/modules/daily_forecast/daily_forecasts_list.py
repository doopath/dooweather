"""
    Module that provides a class to create a list of daily forecasts.
"""
from .daily_forecast_card import Card
from kivymd.uix.card import MDCard


class DailyForecastsList:
    @staticmethod
    def create_daily_forecast(forecast_info: str) -> MDCard:
        return Card(forecast_info)

    @staticmethod
    def create_daily_forecasts_list(forecasts: list[str]) -> list[Card]:
        return [DailyForecastsList.create_daily_forecast(forecast) for forecast in forecasts]
