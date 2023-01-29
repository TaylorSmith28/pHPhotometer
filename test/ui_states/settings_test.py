"""
The file to test the Settings class
"""
from unittest.mock import ANY
from unittest import mock
from photometer.ui_states.settings import Settings
from photometer.ui_states.settings import Settings
from photometer.photometer import Photometer


@mock.patch.object(Settings, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test Settings's handle_key function for each keypad input
    """
    settings = Settings(Photometer(), Settings(Photometer))

    settings.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Salinity"

    settings.substate = 2
    settings.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Temperature"

    settings.substate = 3
    settings.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Correction1"

    settings.substate = 3
    settings.handle_key("B")
    assert settings.substate == 2

    settings.substate = 1
    settings.handle_key("C")
    assert settings.substate == 2


def test_loop():
    """
    The function to test Settings's loop function's lcd calls
    """
    settings = Settings(Photometer(), Settings(Photometer))

    settings.loop()
    assert settings.photometer.lcd.message == " Settings\n>Salinity"

    settings.substate = 2
    settings.loop()
    assert settings.photometer.lcd.message == ">Temperature\n Correction"

    settings.substate = 3
    settings.loop()
    assert settings.photometer.lcd.message == " Temperature\n>Correction"


@mock.patch.object(Settings, "_set_next_state")
def test_settings(set_next_state_mock):
    """
    The function to test the entire use case of the Settings class
    """
    settings = Settings(Photometer(), Settings(Photometer))

    settings.loop()
    assert settings.photometer.lcd.message == " Settings\n>Salinity"

    settings.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Salinity"

    settings.handle_key("C")
    assert settings.substate == 2

    settings.loop()
    assert settings.photometer.lcd.message == ">Temperature\n Correction"

    settings.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Temperature"

    settings.handle_key("C")
    assert settings.substate == 3

    settings.loop()
    assert settings.photometer.lcd.message == " Temperature\n>Correction"

    settings.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Correction1"

    settings.handle_key("C")
    assert settings.substate == 3

    settings.loop()
    assert settings.photometer.lcd.message == " Temperature\n>Correction"

    settings.handle_key("B")
    assert settings.substate == 2

    settings.loop()
    assert settings.photometer.lcd.message == ">Temperature\n Correction"

    settings.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Temperature"

    settings.handle_key("B")
    assert settings.substate == 1

    settings.loop()
    assert settings.photometer.lcd.message == " Settings\n>Salinity"

    settings.handle_key("A")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Salinity"
