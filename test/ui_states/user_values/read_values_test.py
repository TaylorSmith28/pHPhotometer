"""
The file to test the ReadValues class
"""
from unittest.mock import ANY
from unittest import mock
from photometer.ui_states.user_values.read_values import ReadValues
from photometer.photometer import Photometer
from photometer.ui_states.main_menu import MainMenu


@mock.patch.object(ReadValues, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test ReadValues's handle_key function for each keypad input
    """
    read_values = ReadValues(Photometer(), MainMenu(Photometer()))

    read_values.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"

    read_values.substate = 2
    read_values.handle_key("B")
    assert read_values.substate == 1

    read_values.substate = 1
    read_values.handle_key("C")
    assert read_values.substate == 2

    read_values.handle_key("D")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


def test_loop():
    """
    The function to test ReadValues's loop function's lcd calls
    """
    read_values = ReadValues(Photometer(), MainMenu(Photometer()))

    read_values.loop()
    assert (
        read_values.photometer.lcd.message
        == "Sal: "
        + read_values.photometer.salinity
        + "\nTemp: "
        + read_values.photometer.salinity
    )

    read_values.substate = 2
    read_values.loop()
    assert (
        read_values.photometer.lcd.message
        == "C1: " + read_values.photometer.c1 + "\nC2: " + read_values.photometer.c2
    )


@mock.patch.object(ReadValues, "_set_next_state")
def test_read_values(set_next_state_mock):
    """
    The function to test the entire use case of the ReadValues class
    """
    read_values = ReadValues(Photometer(), MainMenu(Photometer()))

    read_values.loop()
    assert (
        read_values.photometer.lcd.message
        == "Sal: "
        + read_values.photometer.salinity
        + "\nTemp: "
        + read_values.photometer.salinity
    )

    read_values.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"

    read_values.handle_key("C")
    assert read_values.substate == 2

    read_values.loop()
    assert (
        read_values.photometer.lcd.message
        == "C1: " + read_values.photometer.c1 + "\nC2: " + read_values.photometer.c2
    )

    read_values.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"

    read_values.handle_key("D")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"

    read_values.handle_key("B")
    assert read_values.substate == 1

    read_values.substate = 2
    read_values.loop()
    assert (
        read_values.photometer.lcd.message
        == "C1: " + read_values.photometer.c1 + "\nC2: " + read_values.photometer.c2
    )

    read_values.handle_key("D")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"
