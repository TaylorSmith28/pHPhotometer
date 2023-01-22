"""
The file to test the Settings class
"""
from unittest.mock import ANY
from unittest import mock
from photometer.ui_states.settings import Settings
from photometer.photometer import Photometer


@mock.patch.object(Settings, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test Setting's handle_key function for each keypad input
    """
    settings = Settings(Photometer())

    settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Salinity"

    settings.handle_key("2")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Temperature"


def test_loop():
    """
    The function to test Settings's loop function's lcd calls
    """
    settings = Settings(Photometer())

    settings.loop()
    assert settings.photometer.lcd.message == "1. Salinity\n2. Temperature"


@mock.patch.object(Settings, "_set_next_state")
def test_settings(set_next_state_mock):
    """
    The function to test the entire use case of the Settings class
    """
    settings = Settings(Photometer())

    settings.loop()
    assert settings.photometer.lcd.message == "1. Salinity\n2. Temperature"

    settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Salinity"

    settings.handle_key("2")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Temperature"
