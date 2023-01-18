"""
The file for the MainMenu class
"""
from photometer.lcd import Character_LCD
from photometer.ui_states.ui_state import UIState
from photometer.ui_states.settings import Settings
from photometer.ui_states.settings import Sample
from photometer.ui_states.user_values.read_values import ReadValues

class MainMenu(UIState):
    def handle_key(self, key):
        if key == 1:
            self._set_next_state(Settings(self.photometer))
        elif key == 2:
            self._set_next_state(ReadValues(self.photometer))
        # Not implemented yet
        #elif key == 3:
        #    self._set_next_state(Sample(self.photometer))

    def loop(self):
        """
        The function to loop through until a keypad press
        """
        Character_LCD.message("1. Settings", 1)
        Character_LCD.message("2. ReadValues", 2)


