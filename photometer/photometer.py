"""
The file for the Photometer class
"""
import digitalio
import board
from photometer.ui_states.main_menu import MainMenu
from photometer.lcd import Character_LCD


class Photometer:
    """
    The Photometer class is the model for the state machine in order to move through the different sampling states

    Attributes:
        state (UIState object): is used to represent the current state in the state machine
        next_state (UIState object): is used to move to the next state in the state machine
        keypad (Keypad object): is used to identify what keypad value was entered
    """

    def __init__(self):
        """
        The constructor for the Photometer class
        """

        # Initialize LCD
        self.lcd_rs = digitalio.DigitalInOut(board.GP2)
        self.lcd_en = digitalio.DigitalInOut(board.GP3)
        self.lcd_d7 = digitalio.DigitalInOut(board.GP19)
        self.lcd_d6 = digitalio.DigitalInOut(board.GP18)
        self.lcd_d5 = digitalio.DigitalInOut(board.GP17)
        self.lcd_d4 = digitalio.DigitalInOut(board.GP16)

        self.lcd_columns = 16
        self.lcd_rows = 2

        self.lcd = Character_LCD(
            self.lcd_rs,
            self.lcd_en,
            self.lcd_d4,
            self.lcd_d5,
            self.lcd_d6,
            self.lcd_d7,
            self.lcd_columns,
            self.lcd_rows,
        )

        # Initialize Keypad

        # Initialize State
        self.state = MainMenu(self)
        self.next_state = None
        self.temperature = None
        self.salinity = None

    def loop(self):
        """
        The function used to loop through in each state
        """
        self._handle_ui()

    def set_next_state(self, new_state, update):
        """
        The function used to set the next state the state machine will enter
        """
        self.next_state = new_state
        if update:
            self._update_state()

    def _update_state(self):
        """
        The function used to move to the next state
        """
        if self.next_state:
            self.state = self.next_state
            self.next_state = None
            self.state.start()

    def _handle_ui(self):
        """
        The function used to receive the keypad input and process the appropriate response
        """
        #key = self.keypad.get_key() Needs implementing
        #self.state.handle_key(key) Needs implementing
        self._update_state()
        self.state.loop()
