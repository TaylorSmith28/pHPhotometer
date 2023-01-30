"""
The file for the Photometer class
"""
from photometer.ui_states.main_menu import MainMenu
from photometer import constants

# Which imports to use for testing
if constants.IS_TEST:
    from photometer.devices import board_mock as board_class
    from photometer.devices.lcd_mock import Character_LCD
    from photometer.devices.keypad_mock import Keypad
else:
    import board as board_class  # type: ignore
    from photometer.devices.lcd import Character_LCD  # type: ignore
    from photometer.devices.keypad import Keypad  # type: ignore


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
        self.lcd_columns = 16
        self.lcd_rows = 2

        self.lcd = Character_LCD(
            rs=board_class.GP2,
            en=board_class.GP3,
            d4=board_class.GP16,
            d5=board_class.GP17,
            d6=board_class.GP18,
            d7=board_class.GP19,
            columns=self.lcd_columns,
            lines=self.lcd_rows,
        )

        # Initialize Keypad
        self.key = "A"
        self.keypad = Keypad(
            r0=board_class.GP6,
            r1=board_class.GP7,
            r2=board_class.GP8,
            r3=board_class.GP9,
            c0=board_class.GP10,
            c1=board_class.GP11,
            c2=board_class.GP12,
            c3=board_class.GP13,
        )

        # Initialize State
        self.state = MainMenu(self)
        self.next_state = None
        self.temperature = "0"
        self.salinity = "0"
        self.c1 = "0"
        self.c2 = "0"
        self.r1 = "0"
        self.r2 = "0"
        self.g1 = "0"
        self.g2 = "0"
        self.b1 = "0"
        self.b2 = "0"
        self.ph = "0"

    def loop(self):
        """
        The function used to loop through in each state
        """
        self._handle_ui()

    def set_next_state(self, new_state, update=True):
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
        # This is implemented this way to prevent button bouncing
        # This should eventually be moved to its own function
        if self.key != self.keypad.keypad_poll():
            self.key = self.keypad.keypad_poll()  # pylint: disable = E1128
            self.state.handle_key(self.key)
            self._update_state()
            self.state.loop()
