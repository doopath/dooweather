"""
    Kivy app prototype.
"""

from kivymd.app import MDApp
from kivy.core.window import Window
from modules.container import Container


class MainApp(MDApp):
    def build(self):
        Window.softinput_mode = 'pan'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return Container()


def main():
    MainApp().run()


(lambda: main() if __name__ == "__main__" else None)()
