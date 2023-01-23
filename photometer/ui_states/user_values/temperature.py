"""
The file for the Temperature class
"""
from photometer.ui_states.user_values.user_value import UserValue


class Temperature(UserValue):
    """
    This is a class for the Temperature state of the photometer

    Attributes:
        photometer (Photometer object): the photometer is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        string (string): the string is used to hold the user input
    """

    def save_value(self):
        """
        The function to save the temperature
        """
        self.photometer.temperature = self.string
