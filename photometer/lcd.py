import time
import digitalio

# Commands
_LCD_CLEARDISPLAY = 0x01
_LCD_RETURNHOME = 0x02
_LCD_ENTRYMODESET = 0x04
_LCD_DISPLAYCONTROL = 0x08
_LCD_CURSORSHIFT = 0x10
_LCD_FUNCTIONSET = 0x20
_LCD_SETCGRAMADDR = 0x40
_LCD_SETDDRAMADDR = 0x80

# Entry flags
_LCD_ENTRYLEFT = 0x02
_LCD_ENTRYSHIFTDECREMENT = 0x00

# Control flags
_LCD_DISPLAYON = 0x04
_LCD_CURSORON = 0x02
_LCD_CURSOROFF = 0x00
_LCD_BLINKON = 0x01
_LCD_BLINKOFF = 0x00

# Move flags
_LCD_DISPLAYMOVE = 0x08
_LCD_MOVERIGHT = 0x04
_LCD_MOVELEFT = 0x00

# Function set flags
_LCD_4BITMODE = 0x00
_LCD_2LINE = 0x08
_LCD_1LINE = 0x00
_LCD_5X8DOTS = 0x00

# Offset for up to 4 rows.
_LCD_ROW_OFFSETS = (0x00, 0x40, 0x14, 0x54)


def _set_bit(byte_value: int, position: int, val: bool) -> int:
    # Given the specified byte_value set the bit at position to the provided
    # boolean value val and return the modified byte.
    ret = None
    if val:
        ret = byte_value | (1 << position)
    else:
        ret = byte_value & ~(1 << position)
    return ret


def _map(
    xval: float, in_min: float, in_max: float, out_min: float, out_max: float
) -> float:
    # Affine transfer/map with constrained output.
    outrange = float(out_max - out_min)
    inrange = float(in_max - in_min)
    ret = (xval - in_min) * (outrange / inrange) + out_min
    if out_max > out_min:
        ret = max(min(ret, out_max), out_min)
    else:
        ret = max(min(ret, out_min), out_max)
    return ret


# pylint: disable-msg=too-many-instance-attributes
class Character_LCD:
    """Base class for character LCD.

    :param ~digitalio.DigitalInOut rs: The reset data line
    :param ~digitalio.DigitalInOut en: The enable data line
    :param ~digitalio.DigitalInOut d4: The data line 4
    :param ~digitalio.DigitalInOut d5: The data line 5
    :param ~digitalio.DigitalInOut d6: The data line 6
    :param ~digitalio.DigitalInOut d7: The data line 7
    :param int columns: The columns on the charLCD
    :param int lines: The lines on the charLCD

    """

    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1

    # pylint: disable-msg=too-many-arguments
    def __init__(
        # pylint: disable=invalid-name
        self,
        rs: digitalio.DigitalInOut,
        en: digitalio.DigitalInOut,
        d4: digitalio.DigitalInOut,
        d5: digitalio.DigitalInOut,
        d6: digitalio.DigitalInOut,
        d7: digitalio.DigitalInOut,
        columns: int,
        lines: int,
        # pylint: enable=invalid-name
    ) -> None:

        self.columns = columns
        self.lines = lines
        #  save pin numbers
        self.reset = rs
        self.enable = en
        self.dl4 = d4
        self.dl5 = d5
        self.dl6 = d6
        self.dl7 = d7

        # set all pins as outputs
        for pin in (rs, en, d4, d5, d6, d7):
            pin.direction = digitalio.Direction.OUTPUT

        # Initialise the display
        self._write8(0x33)
        self._write8(0x32)
        # Initialise display control
        self.displaycontrol = _LCD_DISPLAYON | _LCD_CURSOROFF | _LCD_BLINKOFF
        # Initialise display function
        self.displayfunction = _LCD_4BITMODE | _LCD_1LINE | _LCD_2LINE | _LCD_5X8DOTS
        # Initialise display mode
        self.displaymode = _LCD_ENTRYLEFT | _LCD_ENTRYSHIFTDECREMENT
        # Write to displaycontrol
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)
        # Write to displayfunction
        self._write8(_LCD_FUNCTIONSET | self.displayfunction)
        # Set entry mode
        self._write8(_LCD_ENTRYMODESET | self.displaymode)
        self.clear()
        self._message = None
        self._enable = None
        self._direction = None
        # track row and column used in cursor_position
        # initialize to 0,0
        self.row = 0
        self.column = 0
        self._column_align = False

    # pylint: enable-msg=too-many-arguments

    def home(self) -> None:
        """Moves the cursor "home" to position (0, 0)."""
        self._write8(_LCD_RETURNHOME)
        time.sleep(0.003)

    def clear(self) -> None:
        """Clears everything displayed on the LCD.

        The following example displays, "Hello, world!", then clears the LCD.

        .. code-block:: python

            import time
            import board
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.message = "Hello, world!"
            time.sleep(5)
            lcd.clear()
        """
        self._write8(_LCD_CLEARDISPLAY)
        time.sleep(0.003)

    @property
    def column_align(self) -> bool:
        """If True, message text after '\\n' starts directly below start of first
        character in message. If False, text after '\\n' starts at column zero.
        """
        return self._column_align

    @column_align.setter
    def column_align(self, enable: bool):
        if isinstance(enable, bool):
            self._column_align = enable
        else:
            raise ValueError("The column_align value must be either True or False")

    @property
    def cursor(self) -> bool:
        """True if cursor is visible. False to stop displaying the cursor.

        The following example shows the cursor after a displayed message:

        .. code-block:: python

            import time
            import board
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.cursor = True
            lcd.message = "Cursor! "
            time.sleep(5)

        """
        return self.displaycontrol & _LCD_CURSORON == _LCD_CURSORON

    @cursor.setter
    def cursor(self, show: bool) -> None:
        if show:
            self.displaycontrol |= _LCD_CURSORON
        else:
            self.displaycontrol &= ~_LCD_CURSORON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor_position(self, column: int, row: int) -> None:
        """Move the cursor to position ``column``, ``row`` for the next
        message only. Displaying a message resets the cursor position to (0, 0).

            :param int column: column location
            :param int row: row location
        """
        # Clamp row to the last row of the display
        if row >= self.lines:
            row = self.lines - 1
        # Clamp to last column of display
        if column >= self.columns:
            column = self.columns - 1
        # Set location
        self._write8(_LCD_SETDDRAMADDR | (column + _LCD_ROW_OFFSETS[row]))
        # Update self.row and self.column to match setter
        self.row = row
        self.column = column

    @property
    def blink(self) -> bool:
        """
        Blink the cursor. True to blink the cursor. False to stop blinking.

        The following example shows a message followed by a blinking cursor for five seconds.

        .. code-block:: python

            import time
            import board
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.blink = True
            lcd.message = "Blinky cursor!"
            time.sleep(5)
            lcd.blink = False
        """
        return self.displaycontrol & _LCD_BLINKON == _LCD_BLINKON

    @blink.setter
    def blink(self, blink: bool) -> None:
        if blink:
            self.displaycontrol |= _LCD_BLINKON
        else:
            self.displaycontrol &= ~_LCD_BLINKON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    @property
    def display(self) -> bool:
        """
        Enable or disable the display. True to enable the display. False to disable the display.

        The following example displays, "Hello, world!" on the LCD and then turns the display off.

        .. code-block:: python

            import time
            import board
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.message = "Hello, world!"
            time.sleep(5)
            lcd.display = False
        """
        return self.displaycontrol & _LCD_DISPLAYON == _LCD_DISPLAYON

    @display.setter
    def display(self, enable: bool) -> None:
        if enable:
            self.displaycontrol |= _LCD_DISPLAYON
        else:
            self.displaycontrol &= ~_LCD_DISPLAYON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    @property
    def message(self):
        """Display a string of text on the character LCD.
        Start position is (0,0) if cursor_position is not set.
        If cursor_position is set, message starts at the set
        position from the left for left to right text and from
        the right for right to left text. Resets cursor column
        and row to (0,0) after displaying the message.

        The following example displays, "Hello, world!" on the LCD.

        .. code-block:: python

            import time
            import board
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.message = "Hello, world!"
            time.sleep(5)
        """
        return self._message

    @message.setter
    def message(self, message: str):
        self._message = message
        # Set line to match self.row from cursor_position()
        line = self.row
        # Track times through iteration, to act on the initial character of the message
        initial_character = 0
        # iterate through each character
        for character in message:
            # If this is the first character in the string:
            if initial_character == 0:
                # Start at (0, 0) unless direction is set right to left, in which case start
                # on the opposite side of the display if cursor_position not set or (0,0)
                # If cursor_position is set then starts at the specified location for
                # LEFT_TO_RIGHT. If RIGHT_TO_LEFT cursor_position is determined from right.
                # allows for cursor_position to work in RIGHT_TO_LEFT mode
                if self.displaymode & _LCD_ENTRYLEFT > 0:
                    col = self.column
                else:
                    col = self.columns - 1 - self.column
                self.cursor_position(col, line)
                initial_character += 1
            # If character is \n, go to next line
            if character == "\n":
                line += 1
                # Start the second line at (0, 1) unless direction is set right to left in
                # which case start on the opposite side of the display if cursor_position
                # is (0,0) or not set. Start second line at same column as first line when
                # cursor_position is set
                if self.displaymode & _LCD_ENTRYLEFT > 0:
                    col = self.column * self._column_align
                else:
                    if self._column_align:
                        col = self.column
                    else:
                        col = self.columns - 1
                self.cursor_position(col, line)
            # Write string to display
            else:
                self._write8(ord(character), True)
        # reset column and row to (0,0) after message is displayed
        self.column, self.row = 0, 0

    def move_left(self) -> None:
        """Moves displayed text left one column.

        The following example scrolls a message to the left off the screen.

        .. code-block:: python

            import time
            import board
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            scroll_message = "<-- Scroll"
            lcd.message = scroll_message
            time.sleep(2)
            for i in range(len(scroll_message)):
                lcd.move_left()
                time.sleep(0.5)
        """
        self._write8(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVELEFT)

    def move_right(self) -> None:
        """Moves displayed text right one column.

        The following example scrolls a message to the right off the screen.

        .. code-block:: python

            import time
            import board
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            scroll_message = "Scroll -->"
            lcd.message = scroll_message
            time.sleep(2)
            for i in range(len(scroll_message) + 16):
                lcd.move_right()
                time.sleep(0.5)
        """
        self._write8(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVERIGHT)

    @property
    def text_direction(self):
        """The direction the text is displayed. To display the text left to right beginning on the
        left side of the LCD, set ``text_direction = LEFT_TO_RIGHT``. To display the text right
        to left beginning on the right size of the LCD, set ``text_direction = RIGHT_TO_LEFT``.
        Text defaults to displaying from left to right.

        The following example displays "Hello, world!" from right to left.

        .. code-block:: python

            import time
            import board
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.text_direction = lcd.RIGHT_TO_LEFT
            lcd.message = "Hello, world!"
            time.sleep(5)
        """
        return self._direction

    @text_direction.setter
    def text_direction(self, direction: int) -> None:
        self._direction = direction
        if direction == self.LEFT_TO_RIGHT:
            self._left_to_right()
        elif direction == self.RIGHT_TO_LEFT:
            self._right_to_left()

    def _left_to_right(self) -> None:
        # Displays text from left to right on the LCD.
        self.displaymode |= _LCD_ENTRYLEFT
        self._write8(_LCD_ENTRYMODESET | self.displaymode)

    def _right_to_left(self) -> None:
        # Displays text from right to left on the LCD.
        self.displaymode &= ~_LCD_ENTRYLEFT
        self._write8(_LCD_ENTRYMODESET | self.displaymode)

    def create_char(self, location: int, pattern) -> None:
        """
        Fill one of the first 8 CGRAM locations with custom characters.
        The location parameter should be between 0 and 7 and pattern should
        provide an array of 8 bytes containing the pattern. E.g. you can easily
        design your custom character at http://www.quinapalus.com/hd44780udg.html
        To show your custom character use, for example, ``lcd.message = "\x01"``

        :param int location: Integer in range(8) to store the created character.
        :param Sequence[int] pattern: len(8) describes created character.

        """
        # only position 0..7 are allowed
        location &= 0x7
        self._write8(_LCD_SETCGRAMADDR | (location << 3))
        for i in range(8):
            self._write8(pattern[i], char_mode=True)

    def _write8(self, value: int, char_mode: bool = False) -> None:
        # Sends 8b ``value`` in ``char_mode``.
        # :param value: int
        # :param char_mode: character/data mode selector. False (default) for
        # data only, True for character bits.
        #  one ms delay to prevent writing too quickly.
        time.sleep(0.001)
        #  set character/data bit. (charmode = False)
        self.reset.value = char_mode
        # WRITE upper 4 bits
        self.dl4.value = ((value >> 4) & 1) > 0
        self.dl5.value = ((value >> 5) & 1) > 0
        self.dl6.value = ((value >> 6) & 1) > 0
        self.dl7.value = ((value >> 7) & 1) > 0
        #  send command
        self._pulse_enable()
        # WRITE lower 4 bits
        self.dl4.value = (value & 1) > 0
        self.dl5.value = ((value >> 1) & 1) > 0
        self.dl6.value = ((value >> 2) & 1) > 0
        self.dl7.value = ((value >> 3) & 1) > 0
        self._pulse_enable()

    def _pulse_enable(self) -> None:
        # Pulses (lo->hi->lo) to send commands.
        self.enable.value = False
        # 1microsec pause
        time.sleep(0.0000001)
        self.enable.value = True
        time.sleep(0.0000001)
        self.enable.value = False
        time.sleep(0.0000001)
