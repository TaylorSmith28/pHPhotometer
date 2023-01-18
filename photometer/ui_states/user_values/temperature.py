"""
The file for the Salinity class
"""
from photometer.ui_states.ui_state import UIState
from photometer.lcd import Character_LCD

class Temperature(UIState):
    def __init__(self, photometer, previous_state=None):
        super().__init__(photometer, previous_state)
        self.string = ""

    def save_value(self, value):
        self.photometer.temperature = self.string

    def handle_key(self, key):
        if key == "A":
            self.save_value(self.string)
            self._set_next_state(self.previous_state)
        elif key == "B":
            self.string = self.string[:-1]
        elif key == "C":
            self.string = ""
        elif key == "*":
            if "." not in self.string:
                self.string = self.string +"."
        elif key.isnumeric():
            self.string = self.string +str(key)

    def loop(self):
        Character_LCD.message("*=. B=BS C=Clr", line=1)
        Character_LCD.message(self.string, line=2)