from .constants import COLORSCHEMES


class Colorscheme:
    def __init__(self, mode: str = 'Dark'):
        self.BUTTON_TEXT_FG = None
        self.FORECAST_TEXT_FG = None
        self.TEXT_INPUT_TEXT_COLOR = None
        self.FORECAST_CARD_BG = None

        self._mode = mode
        self._set_scheme()

    def _set_scheme(self) -> None:
        [setattr(self, k, v) for k, v in COLORSCHEMES[self._mode].items()]
