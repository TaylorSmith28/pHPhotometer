"""
The file to test the Temperature class
"""
from unittest.mock import ANY
from unittest import mock
from photometer.ui_states.user_values.temperature import Temperature
from photometer.photometer import Photometer
from photometer.ui_states.settings import Settings


@mock.patch.object(Temperature, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test Temperature's handle_key function for each keypad input
    """
    temperature = Temperature(Photometer(), Settings(Photometer()))
    assert temperature.string == ""

    temperature.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"
    assert temperature.photometer.temperature == ""

    temperature.handle_key("B")
    assert temperature.string == ""

    temperature.string = "3.14"

    temperature.handle_key("B")
    assert temperature.string == "3.1"

    temperature.handle_key("C")
    assert temperature.string == ""

    temperature.handle_key("D")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"

    temperature.handle_key("*")
    assert temperature.string == "."

    temperature.handle_key("3")
    assert temperature.string ==".3"

def test_loop():
    """
    The function to test Temperature's loop function's lcd calls
    """
    temperature = Temperature(Photometer(), Settings(Photometer()))

    temperature.loop()
    assert temperature.photometer.lcd.message == "*=. B=BS C=Clr\n" + temperature.string


@mock.patch.object(Temperature, "_set_next_state")
def test_temperature(set_next_state_mock):
    """
    The function to test a use case of the Temperature class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    temperature = Temperature(Photometer(), Settings(Photometer()))

    temperature.loop()
    assert temperature.photometer.lcd.message == "*=. B=BS C=Clr\n" + temperature.string
    

    temperature.handle_key("3")
    assert temperature.string == "3"

    temperature.loop()
    assert temperature.photometer.lcd.message == "*=. B=BS C=Clr\n" + temperature.string

    temperature.handle_key("*")
    assert temperature.string == "3."

    temperature.loop()
    assert temperature.photometer.lcd.message == "*=. B=BS C=Clr\n" + temperature.string

    temperature.handle_key("*")
    assert temperature.string == "3."

    temperature.loop()
    assert temperature.photometer.lcd.message == "*=. B=BS C=Clr\n" + temperature.string

    temperature.handle_key("1")
    assert temperature.string == "3.1"

    temperature.loop()
    assert temperature.photometer.lcd.message == "*=. B=BS C=Clr\n" + temperature.string

    temperature.handle_key("B")
    assert temperature.string == "3."

    temperature.loop()
    assert temperature.photometer.lcd.message == "*=. B=BS C=Clr\n" + temperature.string

    temperature.handle_key("B")
    assert temperature.string == "3"

    temperature.loop()
    assert temperature.photometer.lcd.message == "*=. B=BS C=Clr\n" + temperature.string

    temperature.handle_key("C")
    assert temperature.string == ""

    temperature.loop()
    assert temperature.photometer.lcd.message == "*=. B=BS C=Clr\n" + temperature.string

    temperature.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"