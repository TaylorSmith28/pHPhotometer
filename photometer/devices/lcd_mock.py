class Character_LCD:
    def __init__(
        self,
        rs,
        en,
        d4,
        d5,
        d6,
        d7,
        columns,
        lines,
    ):

        pass

    def home(self):
        pass

    def clear(self):
        pass

    @property
    def cursor(self):
        pass

    @cursor.setter
    def cursor(self, show: bool):
        pass

    def cursor_position(self, column: int, row: int):
        pass

    @property
    def blink(self):
        pass

    @blink.setter
    def blink(self, blink: bool):
        pass

    @property
    def display(self):
        pass

    @display.setter
    def display(self, enable: bool):
        pass

    @property
    def message(self):
        pass

    @message.setter
    def message(self, message: str):
        pass

    def _write8(self, value: int, char_mode: bool = False):
        pass

    def _pulse_enable(self):
        pass
