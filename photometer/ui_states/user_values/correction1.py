"""
The file for the Correction1 class
"""
from photometer.ui_states.user_values.user_value import UserValue
from photometer.ui_states.user_values.correction2 import Correction2


class Correction1(UserValue):
    """
    This is a class for the Correction1 state of the photometer

    Attributes:
        photometer (Photometer object): the photometer is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        string (string): the string is used to hold the user input
    """

    def handle_key(self, key):
        if key == "A":
            self.save_value()
            self._set_next_state(Correction2(self.photometer, self))
        else:
            super().handle_key(key)

    def save_value(self):
        """
        The function to save the first correction factor
        """
        self.photometer.c1 = self.string

    def loop(self):
        """
        The function to loop through until a keypad press
        """
        self.photometer.lcd.clear()
        self.photometer.lcd.message = "corr=c1*abs+c2\nc1:" + self.string
