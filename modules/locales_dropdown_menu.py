"""
    Dropdown menu for selecting a locale.
"""
from typing import Any, Callable
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from modules import constants


class LocalesDropdownMenu(MDDropdownMenu):
    def __init__(self, update_locale: Callable, **kwargs):
        super().__init__(**kwargs)

        self._update_locale = update_locale
        self.items = []
        self.position = 'center'
        self.width_mult = 4
        self.max_height = Window.size[1] / 3 // 50 * 50

    def _create_item(self, locale: str) -> Any:
        return {
            'text': locale,
            'viewclass': 'OneLineListItem',
            'on_release': lambda: self._on_release(locale)
        }

    def _set_items(self) -> None:
        for locale in constants.LOCALES.keys():
            self.items.append(self._create_item(locale))

    def _on_release(self, locale: str) -> None:
        self._update_locale(locale)
        self.dismiss()

    def open(self) -> None:
        self._set_items()
        super().open()
