"""
The file for the ReadValues class
"""
from photometer.ui_states.ui_state import UIState


class ReadValues(UIState):
    """
    This is a class for the ReadValues state of the photometer

    Attributes:
        photometer (Photometer object): the photometer is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            ANY -> MainMenu

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if key == "A":
            self._set_next_state(self.previous_state)
        elif key == "B":
            if self.substate == 2:
                self.substate = 1
        elif key == "C":
            if self.substate == 1:
                self.substate = 2
        elif key == "D":
            self._set_next_state(self.previous_state)

    def loop(self):
        """
        The function to loop through until a keypad press
        """
        self.photometer.lcd.clear()
        if self.substate == 1:
            self.photometer.lcd.message = (
                "Sal: "
                + self.photometer.salinity
                + "\nTemp: "
                + self.photometer.temperature
            )
        elif self.substate == 2:
            self.photometer.lcd.message = (
                "C1: " + self.photometer.c1 + "\nC2: " + self.photometer.c2
            )
