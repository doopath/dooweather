"""
    Dropdown menu for selecting a colorscheme.
"""
from typing import Any, Callable
from kivy.core.window import Window
from kivymd.material_resources import dp
from kivymd.uix.menu import MDDropdownMenu


class BaseDropdownMenu(MDDropdownMenu):
    def __init__(self, update: Callable, *args, **kwargs):
        super().__init__(**kwargs)

        self._update = update
        self.items = []
        self.position = 'center'
        self.width_mult = dp(4)

    def _create_item(self, item_text: str) -> Any:
        return {
            'text': item_text,
            'viewclass': 'OneLineListItem',
            'on_release': lambda: self._on_release(item_text)
        }

    def _set_items(self) -> None: ...

    def _set_max_height(self) -> None:
        if (items_scale := len(self.items)) > 4:
            items_scale = 4

        self.max_height = dp(round(Window.size[1] / 16) * items_scale)

    def _on_release(self, update_item: str) -> None:
        self._update(update_item)
        self.dismiss()

    def open(self) -> None:
        self._set_items()
        self._set_max_height()
        super().open()
