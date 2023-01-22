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

    def clear(self):
        pass

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message: str):
        self._message = message
