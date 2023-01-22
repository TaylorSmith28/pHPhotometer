"""
The file to test the Salinity class
"""
from unittest.mock import ANY
from unittest import mock
from photometer.ui_states.user_values.salinity import Salinity
from photometer.photometer import Photometer
from photometer.ui_states.settings import Settings


@mock.patch.object(Salinity, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test Salinity's handle_key function for each keypad input
    """
    salinity = Salinity(Photometer(), Settings(Photometer()))
    assert salinity.string == ""

    salinity.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"
    assert salinity.photometer.salinity == ""

    salinity.handle_key("B")
    assert salinity.string == ""

    salinity.string = "3.14"

    salinity.handle_key("B")
    assert salinity.string == "3.1"

    salinity.handle_key("C")
    assert salinity.string == ""

    salinity.handle_key("D")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"

    salinity.handle_key("*")
    assert salinity.string == "."

    salinity.handle_key("3")
    assert salinity.string == ".3"


def test_loop():
    """
    The function to test Salinity's loop function's lcd calls
    """
    salinity = Salinity(Photometer(), Settings(Photometer()))

    salinity.loop()
    assert salinity.photometer.lcd.message == "*=. B=BS C=Clr\n" + salinity.string


@mock.patch.object(Salinity, "_set_next_state")
def test_salinity(set_next_state_mock):
    """
    The function to test a use case of the Salinity class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    salinity = Salinity(Photometer(), Settings(Photometer()))

    salinity.loop()
    assert salinity.photometer.lcd.message == "*=. B=BS C=Clr\n" + salinity.string

    salinity.handle_key("3")
    assert salinity.string == "3"

    salinity.loop()
    assert salinity.photometer.lcd.message == "*=. B=BS C=Clr\n" + salinity.string

    salinity.handle_key("*")
    assert salinity.string == "3."

    salinity.loop()
    assert salinity.photometer.lcd.message == "*=. B=BS C=Clr\n" + salinity.string

    salinity.handle_key("*")
    assert salinity.string == "3."

    salinity.loop()
    assert salinity.photometer.lcd.message == "*=. B=BS C=Clr\n" + salinity.string

    salinity.handle_key("1")
    assert salinity.string == "3.1"

    salinity.loop()
    assert salinity.photometer.lcd.message == "*=. B=BS C=Clr\n" + salinity.string

    salinity.handle_key("B")
    assert salinity.string == "3."

    salinity.loop()
    assert salinity.photometer.lcd.message == "*=. B=BS C=Clr\n" + salinity.string

    salinity.handle_key("B")
    assert salinity.string == "3"

    salinity.loop()
    assert salinity.photometer.lcd.message == "*=. B=BS C=Clr\n" + salinity.string

    salinity.handle_key("C")
    assert salinity.string == ""

    salinity.loop()
    assert salinity.photometer.lcd.message == "*=. B=BS C=Clr\n" + salinity.string

    salinity.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"
