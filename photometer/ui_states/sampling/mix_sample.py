"""
The file for the MixSample class
"""

from photometer.ui_states.ui_state import UIState
from photometer.ui_states.sampling.sample import Sample


class MixSample(UIState):
    """
    This is a class for the MixSample state of the photometer

    Attributes:
        photometer (Photometer object): the photometer is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            ANY -> Sample

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if key is not None:
            self._set_next_state(Sample(self.photometer))

    def loop(self):
        """
        The function to loop through until a keypad press
        """
        self.photometer.lcd.clear()
        self.photometer.lcd.message = "Mix Dye\nPress Any Key"
