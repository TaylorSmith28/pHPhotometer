"""
The file to test the Correction1 class
"""
from unittest.mock import ANY
from unittest import mock
from photometer.ui_states.user_values.correction1 import Correction1
from photometer.photometer import Photometer
from photometer.ui_states.settings import Settings


@mock.patch.object(Correction1, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test Correction1's handle_key function for each keypad input
    """
    correction1 = Correction1(Photometer(), Settings(Photometer()))
    assert correction1.string == ""

    correction1.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Correction2"
    assert correction1.photometer.c1 == ""

    correction1.handle_key("B")
    assert correction1.string == ""

    correction1.string = "3.14"

    correction1.handle_key("B")
    assert correction1.string == "3.1"

    correction1.handle_key("C")
    assert correction1.string == ""

    correction1.handle_key("D")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"

    correction1.handle_key("*")
    assert correction1.string == "."

    correction1.handle_key("3")
    assert correction1.string == ".3"


def test_loop():
    """
    The function to test Correction1's loop function's lcd calls
    """
    correction1 = Correction1(Photometer(), Settings(Photometer()))

    correction1.loop()
    assert correction1.photometer.lcd.message == "corr=c1*abs+c2\nc1:" + correction1.string


@mock.patch.object(Correction1, "_set_next_state")
def test_correction1(set_next_state_mock):
    """
    The function to test a use case of the Correction1 class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    correction1 = Correction1(Photometer(), Settings(Photometer()))

    correction1.loop()
    assert correction1.photometer.lcd.message == "corr=c1*abs+c2\nc1:" + correction1.string

    correction1.handle_key("3")
    assert correction1.string == "3"

    correction1.loop()
    assert correction1.photometer.lcd.message == "corr=c1*abs+c2\nc1:" + correction1.string

    correction1.handle_key("*")
    assert correction1.string == "3."

    correction1.loop()
    assert correction1.photometer.lcd.message == "corr=c1*abs+c2\nc1:" + correction1.string

    correction1.handle_key("*")
    assert correction1.string == "3."

    correction1.loop()
    assert correction1.photometer.lcd.message == "corr=c1*abs+c2\nc1:" + correction1.string

    correction1.handle_key("1")
    assert correction1.string == "3.1"

    correction1.handle_key("A")
    assert correction1.photometer.c1 == "3.1"
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Correction2"
