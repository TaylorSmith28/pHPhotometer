"""
The file for the MainMenu class
"""
from photometer.ui_states.ui_state import UIState
from photometer.ui_states.settings import Settings
from photometer.ui_states.user_values.read_values import ReadValues
from photometer.ui_states.sampling.add_sample import AddSample


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
        The function to respond to a keypad input

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if key == "A":
            if self.substate == 1:
                self._set_next_state(AddSample(self.photometer, self))
            if self.substate == 2:
                self._set_next_state(Settings(self.photometer, self))
            if self.substate == 3:
                self._set_next_state(ReadValues(self.photometer, self))
        elif key == "B":
            if self.substate > 1:
                self.substate -= 1
        elif key == "C":
            if self.substate < 3:
                self.substate += 1

    def loop(self):
        """
        The function to loop through until a keypad press
        """
        self.photometer.lcd.clear()
        if self.substate == 1:
            self.photometer.lcd.message = " Main Menu\n>Sample"
        if self.substate == 2:
            self.photometer.lcd.message = ">Settings\n Read Values"
        if self.substate == 3:
            self.photometer.lcd.message = " Settings\n>Read Values"
