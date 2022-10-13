"""
    Weather app written in python.
"""
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout

from modules.cache import Cache
from modules.container import Container
from modules.constants import LOCALES
from modules import constants


def set_window_size():
    if platform == 'android' or platform == 'ios':
        return
    else:
        Window.size = (550, 900)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logo = None
        self._cache = Cache()

    def build(self) -> Widget:
        self._set_locale()
        set_window_size()

        Window.softinput_mode = 'pan'
        container: MDGridLayout = Container(self._cache)

        self.logo = 'weather_icon.png'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return container

    def on_stop(self) -> None:
        self._cache.save_session()

    def on_pause(self) -> None:
        self._cache.save_session()

    def _set_locale(self) -> None:
        try:
            locale_key = self._cache.get_value('LOCALE')
            constants.LOCALE = LOCALES[locale_key]
        except KeyError: pass


def main():
    MainApp().run()


(lambda: main() if __name__ == "__main__" else None)()

