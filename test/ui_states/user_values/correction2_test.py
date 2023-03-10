"""
The file to test the Correction2 class
"""
from unittest.mock import ANY
from unittest import mock
from photometer.ui_states.user_values.correction2 import Correction2
from photometer.photometer import Photometer
from photometer.ui_states.settings import Settings


@mock.patch.object(Correction2, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test Correction2's handle_key function for each keypad input
    """
    correction2 = Correction2(Photometer(), Settings(Photometer()))
    assert correction2.string == ""

    correction2.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"
    assert correction2.photometer.c2 == ""

    correction2.handle_key("B")
    assert correction2.string == ""

    correction2.string = "3.24"

    correction2.handle_key("B")
    assert correction2.string == "3.2"

    correction2.handle_key("C")
    assert correction2.string == ""

    correction2.handle_key("D")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"

    correction2.handle_key("*")
    assert correction2.string == "."

    correction2.handle_key("3")
    assert correction2.string == ".3"


def test_loop():
    """
    The function to test Correction2's loop function's lcd calls
    """
    correction2 = Correction2(Photometer(), Settings(Photometer()))

    correction2.loop()
    assert (
        correction2.photometer.lcd.message == "corr=c1*abs+c2\nc2:" + correction2.string
    )


@mock.patch.object(Correction2, "_set_next_state")
def test_correction2(set_next_state_mock):
    """
    The function to test a use case of the Correction2 class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "2"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    correction2 = Correction2(Photometer(), Settings(Photometer()))

    correction2.loop()
    assert (
        correction2.photometer.lcd.message == "corr=c1*abs+c2\nc2:" + correction2.string
    )

    correction2.handle_key("3")
    assert correction2.string == "3"

    correction2.loop()
    assert (
        correction2.photometer.lcd.message == "corr=c1*abs+c2\nc2:" + correction2.string
    )

    correction2.handle_key("*")
    assert correction2.string == "3."

    correction2.loop()
    assert (
        correction2.photometer.lcd.message == "corr=c1*abs+c2\nc2:" + correction2.string
    )

    correction2.handle_key("*")
    assert correction2.string == "3."

    correction2.loop()
    assert (
        correction2.photometer.lcd.message == "corr=c1*abs+c2\nc2:" + correction2.string
    )

    correction2.handle_key("1")
    assert correction2.string == "3.1"

    correction2.handle_key("A")
    assert correction2.photometer.c2 == "3.1"
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"
