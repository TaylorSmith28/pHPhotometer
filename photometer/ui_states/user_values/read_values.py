"""
The file for the ReadValues class
"""
from photometer.ui_states.ui_state import UIState


class ReadValues(UIState):
    def handle_key(self, key):
        self._set_next_state(self.previous_state)

    def loop(self):
        self.photometer.lcd.message = (
            "Sal: " + self.photometer.salinity + "\nTemp: " + self.photometer.salinity
        )
