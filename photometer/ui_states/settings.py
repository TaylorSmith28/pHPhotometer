"""
The file for the Settings class
"""
from photometer.ui_states.ui_state import UIState
from photometer.ui_states.user_values.salinity import Salinity
from photometer.ui_states.user_values.temperature import Temperature


class Settings(UIState):
    def handle_key(self, key):
        if key == 1:
            self._set_next_state(Salinity(self.photometer))
        elif key == 2:
            self._set_next_state(Temperature(self.photometer))

    def loop(self):
        self.photometer.lcd.message = "1. Salinity\n2. Temperature"
