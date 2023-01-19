"""
The file for the Settings class
"""
from photometer.ui_states.ui_state import UIState
from photometer.ui_states.user_values.salinity import Salinity
from photometer.ui_states.user_values.temperature import Temperature


class Settings(UIState):
    """
    This is a class for the MainMenu state of the photometer

    Attributes:
        photometer (Photometer object): the photometer is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """
    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            1 -> Salinity
            2 -> Temperature

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if key == 1:
            self._set_next_state(Salinity(self.photometer))
        elif key == 2:
            self._set_next_state(Temperature(self.photometer))

    def loop(self):
        """
        The function to loop through until a keypad press
        """
        self.photometer.lcd.clear()
        self.photometer.lcd.message = "1. Salinity\n2. Temperature"
