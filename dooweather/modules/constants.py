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
        'LOWEST_TEMPERATURE': 'Min temperature',
        'HIGHEST_TEMPERATURE': 'Max temperature',
        'FEELS_LIKE': 'Feels like',
        'HUMIDITY': 'Humidity',
        'WIND_SPEED': 'Wind speed',
        'WIND_DIRECTION': 'Wind direction',
        'PRESSURE': 'Pressure',

        'INVALID_LOCATION': 'Invalid location',
        'LOADING_MESSAGE': 'Loading',
        'FORECAST_NOW': 'Forecast (now)',
        'ENTERED_NO_CITY': "You didn't enter a city yet!",
        'ENTER_CITY': 'Enter your city',
        'SELECT_BUTTON': 'Select',
        'GET_WEATHER_BUTTON': 'Get forecast',
        'LOCALE_BUTTON': 'Locale',
        'REMOVE_ALL': 'Remove all',
        'NO_CONNECTION_MESSAGE': 'No internet connection',
        'THEME_BUTTON_TEXT': 'THEME',
    },
    'RU': {  # Russian
        'DATE': 'Дата',
        'CITY': 'Город',
        'TEMPERATURE': 'Температура',
        'LOWEST_TEMPERATURE': 'Мин. температура',
        'HIGHEST_TEMPERATURE': 'Макс. температура',
        'FEELS_LIKE': 'Ощущается как',
        'HUMIDITY': 'Влажность',
        'WIND_SPEED': 'Скорость ветра',
        'WIND_DIRECTION': 'Направление ветра',
        'PRESSURE': 'Давление',

        'INVALID_LOCATION': 'Неверное местоположение',
        'LOADING_MESSAGE': 'Загрузка',
        'FORECAST_NOW': 'Прогноз на сегодня',
        'ENTERED_NO_CITY': "Вы еще не ввели город!",
        'ENTER_CITY': 'Введите свой город',
        'SELECT_BUTTON': 'Выбрать',
        'GET_WEATHER_BUTTON': 'Получить прогноз',
        'LOCALE_BUTTON': 'Язык',
        'REMOVE_ALL': 'Удалить все',
        'NO_CONNECTION_MESSAGE': 'Отсутствует интернет-соединение',
        'THEME_BUTTON_TEXT': 'Тема',
    }
}
LOCALE = LOCALES[DEFAULT_LOCALE]
COLORSCHEMES = {
    'Dark': {
        'BUTTON_TEXT_FG': (.92, .92, .92, 1),
        'FORECAST_TEXT_FG': (.92, .92, .92, 1),
        'TEXT_INPUT_TEXT_COLOR': (.92, .92, .92, 1),
        'FORECAST_CARD_BG': (.15, .15, .15, 1),
    },
    'Light': {
        'BUTTON_TEXT_FG': (.15, .15, .15, 1),
        'FORECAST_TEXT_FG': (.15, .15, .15, 1),
        'TEXT_INPUT_TEXT_COLOR': (.15, .15, .15, 1),
        'FORECAST_CARD_BG': (.92, .92, .92, 1),
    }
}
