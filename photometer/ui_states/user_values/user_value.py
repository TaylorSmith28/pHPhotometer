"""
The file for the UserValue superclass
"""

from photometer.ui_states.ui_state import UIState


class UserValue(UIState):
    """
    This is a superclass for the UserValue state's temperature and salinity

    Attributes:
        photometer (Photometer object): the photometer is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

    def __init__(self, photometer, previous_state):
        """
        The constructor for the UserValue state

        Parameters:
            photometer (Photometer object): the photometer is used to move through the state machine
            previous_state (UIState object): the previous_state is used to return the last visited state
        """
        super().__init__(photometer, previous_state)
        self.string = ""

    def save_value(self):
        """
        The function to save photometer values

        This must be implemented for each user_value state
        """
        raise Exception(self.name() + " requires a save_value function")

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            A -> Save value and return to previous state
            B -> Backspace on the entered user value
            C -> Clear currently entered user value
            D -> Return to previous state without saving a new value
            * -> Enters a decimal point to be appended to new user value
                - Only if there is not already a decimal point
            [0-9] -> Enter a number to be appended to new user value

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if key == "A":
            self._set_next_state(self.previous_state)
            self.save_value()
        if key == "B":
            self.string = self.string[:-1]
        elif key == "C":
            self.string = ""
        elif key == "D":
            self._set_next_state(self.previous_state)
        elif key == "*":
            if "." not in self.string:
                self.string = self.string + "."
        elif str(key).isdigit():
            self.string = self.string + str(key)

    def loop(self):
        """
        The function to loop through until a keypad press
        """
        self.photometer.lcd.clear()
        self.photometer.lcd.message = "*=. B=BS C=Clr\n" + self.string
