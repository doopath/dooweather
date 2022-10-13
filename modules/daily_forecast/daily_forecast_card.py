from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class Card(MDCard):
    def __init__(self, text: str, *args, **kwargs):
        self.radius = dp(15),
        self.padding = Window.height / 40
        self.size_hint = (1, None)

        super().__init__(*args, **kwargs)

        label = MDLabel(
            padding=[Window.height / 40, Window.height / 40],
            text=f'\n{text}',
            line_height=1.4,
            size_hint=(1, 1)
        )
        label.font_size = '18sp'
        label.size = label.texture_size

        self.add_widget(label)
        self.height = label.height + Window.height / 3.0
