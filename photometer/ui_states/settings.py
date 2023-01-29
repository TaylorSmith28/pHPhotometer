"""
The file for the Settings class
"""
from photometer.ui_states.ui_state import UIState
from photometer.ui_states.user_values.salinity import Salinity
from photometer.ui_states.user_values.temperature import Temperature
from photometer.ui_states.user_values.correction1 import Correction1
from photometer.ui_states import main_menu


class Settings(UIState):
    """
    This is a class for the Settings state of the photometer

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
                self._set_next_state(Salinity(self.photometer, self))
            if self.substate == 2:
                self._set_next_state(Temperature(self.photometer, self))
            if self.substate == 3:
                self._set_next_state(Correction1(self.photometer, self))
        elif key == "B":
            if self.substate > 1:
                self.substate -= 1
        elif key == "C":
            if self.substate < 3:
                self.substate += 1
        elif key == "D":
            self._set_next_state(main_menu.MainMenu(self.photometer))

    def loop(self):
        """
        The function to loop through until a keypad press
        """
        self.photometer.lcd.clear()
        if self.substate == 1:
            self.photometer.lcd.message = " Settings\n>Salinity"
        if self.substate == 2:
            self.photometer.lcd.message = ">Temperature\n Correction"
        if self.substate == 3:
            self.photometer.lcd.message = " Temperature\n>Correction"
