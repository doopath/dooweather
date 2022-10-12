"""
    Available constants.
"""
import sys


APP_DIR = sys.path[0]
DEFAULT_LOCALE = 'EN'
LOCALES = {
    'EN': {  # English
        'DATE': 'Date',
        'CITY': 'City',
        'TEMPERATURE': 'Temperature',
        'LOWEST_TEMPERATURE': 'Lowest temperature',
        'HIGHEST_TEMPERATURE': 'Highest temperature',
        'FEELS_LIKE': 'Feels like',
        'HUMIDITY': 'Humidity',
        'WIND_SPEED': 'Wind speed',
        'WIND_DIRECTION': 'Wind direction',
        'PRESSURE': 'Pressure',

        'INVALID_LOCATION': 'Invalid location',
        'FORECAST_NOW': 'Forecast (now)',
        'ENTERED_NO_CITY': "You didn't enter a city yet!",
        'ENTER_CITY': 'Enter your city',
        'SELECT_BUTTON': 'Select',
        'GET_WEATHER_BUTTON': 'Get forecast',
        'LOCALE_BUTTON': 'Locale',
        'REMOVE_ALL': 'Remove all',
    },
    'RU': {  # Russian
        'DATE': 'Дата',
        'CITY': 'Город',
        'TEMPERATURE': 'Температура',
        'LOWEST_TEMPERATURE': 'Наименьшая температура',
        'HIGHEST_TEMPERATURE': 'Наивысшая температура',
        'FEELS_LIKE': 'Ощущается как',
        'HUMIDITY': 'Влажность',
        'WIND_SPEED': 'Скорость ветра',
        'WIND_DIRECTION': 'Направление ветра',
        'PRESSURE': 'Давление',

        'INVALID_LOCATION': 'Неверное местоположение',
        'FORECAST_NOW': 'Прогноз на сегодня',
        'ENTERED_NO_CITY': "Вы еще не ввели город!",
        'ENTER_CITY': 'Введите свой город',
        'SELECT_BUTTON': 'Выбрать',
        'GET_WEATHER_BUTTON': 'Получить прогноз',
        'LOCALE_BUTTON': 'Язык',
        'REMOVE_ALL': 'Удалить все',
    }
}
LOCALE = LOCALES[DEFAULT_LOCALE]
