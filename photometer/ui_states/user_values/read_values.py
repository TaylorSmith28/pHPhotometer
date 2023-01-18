"""
The file for the ReadValues class
"""
from photometer.lcd import Character_LCD
from photometer.ui_states.ui_state import UIState

class ReadValues(UIState):
    def handle_key(self, key):
        self._set_next_state(self.previous_state)
    def loop(self):
        Character_LCD.message("Sal: "+self.photometer.salinity, 1)
        Character_LCD.message("Temp: "+self.photometer.salinity,2)