"""
    Kivy app prototype.
"""
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.core.window import Window

from modules.cache import Cache
from modules.container import Container


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cache = Cache()

    def build(self) -> Widget:
        Window.softinput_mode = 'pan'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return Container(self._cache)

    def on_stop(self) -> None:
        self._cache.save_session()


def main():
    MainApp().run()


(lambda: main() if __name__ == "__main__" else None)()
