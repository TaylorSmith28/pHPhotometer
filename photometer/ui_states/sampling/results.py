"""
The file for the Results class
"""

from photometer.ui_states.ui_state import UIState
from photometer.ui_states import main_menu


class Results(UIState):
    """
    This is a class for the Results state of the photometer

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
        if key is not None:
            self._set_next_state(main_menu.MainMenu(self.photometer))

    def loop(self):
        """
        The function to loop through until a keypad press
        """
        self.photometer.lcd.clear()
        if self.substate == 1:
            self.photometer.lcd.message = (
                "R"
                + self.photometer.r2
                + "G"
                + self.photometer.g2
                + "B"
                + self.photometer.b2
                + "\npH: "
                + self.photometer.ph
            )
