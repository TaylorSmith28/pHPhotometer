"""
The file to test the MainMenu class
"""
from unittest.mock import ANY
from unittest import mock
from photometer.ui_states.main_menu import MainMenu
from photometer.photometer import Photometer
from photometer.devices.lcd import Character_LCD


@mock.patch.object(MainMenu, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test MainMenu's handle_key function for each keypad input
    """
    main_menu = MainMenu(Photometer())

    main_menu.handle_key("1")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"

    main_menu.handle_key("2")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "ReadValues"


@mock.patch.object(Character_LCD, "clear")
def test_loop(lcd_out_mock):
    """
    The function to test MainMenu's loop function's lcd_interface calls
    """
    main_menu = MainMenu(Photometer())

    main_menu.loop()
    lcd_out_mock.assert_called()
    assert main_menu.photometer.lcd.message == "1. Settings\n2. ReadValues"


@mock.patch.object(Character_LCD, "clear")
@mock.patch.object(MainMenu, "_set_next_state")
def test_main_menu(set_next_state_mock, lcd_out_mock):
    """
    The function to test the entire use case of the MainMenu class
    """
    main_menu = MainMenu(Photometer())

    main_menu.loop()
    lcd_out_mock.assert_called()
    assert main_menu.photometer.lcd.message == "1. Settings\n2. ReadValues"

    main_menu.handle_key("1")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "Settings"

    main_menu.handle_key("2")
    set_next_state_mock.assert_called_with(ANY)
    assert set_next_state_mock.call_args.args[0].name() == "ReadValues"
