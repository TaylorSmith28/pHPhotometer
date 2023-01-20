"""
The file for the MainMenu class
"""
from photometer.ui_states.ui_state import UIState
from photometer.ui_states.settings import Settings

# from photometer.ui_states.settings import Sample
# from photometer.ui_states.user_values.read_values import ReadValues


class MainMenu(UIState):
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
            1 -> Settings
            2 -> ReadValues

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if key == "1":
            self._set_next_state(Settings(self.photometer))
        # NEEDS IMPLEMENTING
        # elif key == "2":
        #    self._set_next_state(ReadValues(self.photometer))
        # elif key == "3":
        #    self._set_next_state(Sample(self.photometer))

    def loop(self):
        """
        The function to loop through until a keypad press
        """
        self.photometer.lcd.clear()
        self.photometer.lcd.message = "1. Settings\n2. ReadValues"
