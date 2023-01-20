import time
import digitalio

_LCD_CLEARDISPLAY = 0x01
_LCD_RETURNHOME = 0x02
_LCD_ENTRYMODESET = 0x04
_LCD_DISPLAYCONTROL = 0x08
_LCD_FUNCTIONSET = 0x20
_LCD_SETDDRAMADDR = 0x80

_LCD_ENTRYLEFT = 0x02
_LCD_ENTRYSHIFTDECREMENT = 0x00

_LCD_DISPLAYON = 0x04
_LCD_CURSORON = 0x02
_LCD_CURSOROFF = 0x00
_LCD_BLINKON = 0x01
_LCD_BLINKOFF = 0x00

_LCD_4BITMODE = 0x00
_LCD_2LINE = 0x08
_LCD_1LINE = 0x00
_LCD_5X8DOTS = 0x00

_LCD_ROW_OFFSETS = (0x00, 0x40, 0x14, 0x54)


class Character_LCD:
    def __init__(
        self,
        rs,
        en,
        d4,
        d5,
        d6,
        d7,
        columns,
        lines,
    ):

        self.reset = digitalio.DigitalInOut(rs)
        self.enable = digitalio.DigitalInOut(en)
        self.dl7 = digitalio.DigitalInOut(d7)
        self.dl6 = digitalio.DigitalInOut(d6)
        self.dl5 = digitalio.DigitalInOut(d5)
        self.dl4 = digitalio.DigitalInOut(d4)

        self.columns = columns
        self.lines = lines

        for pin in (rs, en, d4, d5, d6, d7):
            pin.direction = digitalio.Direction.OUTPUT

        self._write8(0x33)
        self._write8(0x32)
        self.displaycontrol = _LCD_DISPLAYON | _LCD_CURSOROFF | _LCD_BLINKOFF
        self.displayfunction = _LCD_4BITMODE | _LCD_1LINE | _LCD_2LINE | _LCD_5X8DOTS
        self.displaymode = _LCD_ENTRYLEFT | _LCD_ENTRYSHIFTDECREMENT
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)
        self._write8(_LCD_FUNCTIONSET | self.displayfunction)
        self._write8(_LCD_ENTRYMODESET | self.displaymode)
        self.clear()
        self._message = None
        self._enable = None
        self._direction = None
        self.row = 0
        self.column = 0
        self._column_align = False

    def home(self):
        """Moves the cursor "home" to position (0, 0)."""
        self._write8(_LCD_RETURNHOME)
        time.sleep(0.003)

    def clear(self):
        self._write8(_LCD_CLEARDISPLAY)
        time.sleep(0.003)

    @property
    def cursor(self):
        return self.displaycontrol & _LCD_CURSORON == _LCD_CURSORON

    @cursor.setter
    def cursor(self, show: bool):
        if show:
            self.displaycontrol |= _LCD_CURSORON
        else:
            self.displaycontrol &= ~_LCD_CURSORON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor_position(self, column: int, row: int):
        if row >= self.lines:
            row = self.lines - 1
        if column >= self.columns:
            column = self.columns - 1
        self._write8(_LCD_SETDDRAMADDR | (column + _LCD_ROW_OFFSETS[row]))
        self.row = row
        self.column = column

    @property
    def blink(self):
        return self.displaycontrol & _LCD_BLINKON == _LCD_BLINKON

    @blink.setter
    def blink(self, blink: bool):
        if blink:
            self.displaycontrol |= _LCD_BLINKON
        else:
            self.displaycontrol &= ~_LCD_BLINKON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    @property
    def display(self):
        return self.displaycontrol & _LCD_DISPLAYON == _LCD_DISPLAYON

    @display.setter
    def display(self, enable: bool):
        if enable:
            self.displaycontrol |= _LCD_DISPLAYON
        else:
            self.displaycontrol &= ~_LCD_DISPLAYON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message: str):
        self._message = message
        line = self.row
        initial_character = 0
        for character in message:
            if initial_character == 0:
                if self.displaymode & _LCD_ENTRYLEFT > 0:
                    col = self.column
                else:
                    col = self.columns - 1 - self.column
                self.cursor_position(col, line)
                initial_character += 1
            if character == "\n":
                line += 1
                if self.displaymode & _LCD_ENTRYLEFT > 0:
                    col = self.column * self._column_align
                else:
                    if self._column_align:
                        col = self.column
                    else:
                        col = self.columns - 1
                self.cursor_position(col, line)
            else:
                self._write8(ord(character), True)
        self.column, self.row = 0, 0

    def _write8(self, value: int, char_mode: bool = False):
        time.sleep(0.001)
        self.reset.value = char_mode
        self.dl4.value = ((value >> 4) & 1) > 0
        self.dl5.value = ((value >> 5) & 1) > 0
        self.dl6.value = ((value >> 6) & 1) > 0
        self.dl7.value = ((value >> 7) & 1) > 0
        self._pulse_enable()
        self.dl4.value = (value & 1) > 0
        self.dl5.value = ((value >> 1) & 1) > 0
        self.dl6.value = ((value >> 2) & 1) > 0
        self.dl7.value = ((value >> 3) & 1) > 0
        self._pulse_enable()

    def _pulse_enable(self):
        self.enable.value = False
        time.sleep(0.0000001)
        self.enable.value = True
        time.sleep(0.0000001)
        self.enable.value = False
        time.sleep(0.0000001)
