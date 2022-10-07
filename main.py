"""
    Kivy app prototype.
"""
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.utils import platform

from modules.cache import Cache
from modules.container import Container


def set_window_size():
    match platform:
        case 'android' | 'ios':
            return
        case _:
            Window.size = (600, 800)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cache = Cache()

    def build(self) -> Widget:
        set_window_size()
        Window.softinput_mode = 'pan'

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return Container(self._cache)

    def on_stop(self) -> None:
        self._cache.save_session()

    def on_pause(self) -> None:
        self._cache.save_session()


def main():
    MainApp().run()


(lambda: main() if __name__ == "__main__" else None)()
