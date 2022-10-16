"""
    Weather app written in python.
"""
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout

try:
    """
    Imports for runnting the app on Android.
    There the app is located in /smth/org.doopath/app
    and the buildozer tool gathers all the files from the
    dooweather directory to the app directory. So you need
    to import the modules from the app directory.
    """
    from modules import cache
    from modules.container import Container
    from modules.constants import LOCALES
    from modules import constants
except ModuleNotFoundError:
    """
    For whl build.
    In Linux common installation with pip the app will be
    located in $HOME/.local/lib/pythonX.X/site-packages/dooweather
    and PYTHONPATH will contain the $HOME/.local/lib/pythonX.X/site-packages
    directory so you need to set module (dooweather) name.
    """
    from dooweather.modules import cache
    from dooweather.modules.container import Container
    from dooweather.modules.constants import LOCALES
    from dooweather.modules import constants


def set_window_size() -> None:
    if platform == 'android' or platform == 'ios':
        return
    else:
        Window.size = (800, 900)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logo = None
        self._cache = cache.Cache()

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


def main() -> None:
    MainApp().run()


if __name__ == "__main__":
    main()

