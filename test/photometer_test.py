"""
The file to test the Photometer class
"""
from unittest import mock
from photometer.ui_states.main_menu import MainMenu
from photometer.photometer import Photometer


@mock.patch.object(Photometer, "_handle_ui")
def test_loop(handle_ui_mock):
    """
    The function to test function calls of the loop function
    """
    photometer = Photometer()

    photometer.loop()
    handle_ui_mock.assert_called()


@mock.patch.object(Photometer, "_update_state")
def test_set_next_state_true(update_state_mock):
    """
    The function to test the set_next_state function with update parameter set to True
    """
    photometer = Photometer()

    temp = MainMenu(photometer)
    assert photometer.next_state is None
    photometer.set_next_state(temp, True)
    assert photometer.next_state == temp
    update_state_mock.assert_called()


@mock.patch.object(Photometer, "_update_state")
def test_set_next_state_false(update_state_mock):
    """
    The function to test the set_next_state function with update parameter set to False
    """
    photometer = Photometer()

    temp = MainMenu(photometer)
    assert photometer.next_state is None
    photometer.set_next_state(temp, False)
    assert photometer.next_state == temp
    update_state_mock.assert_not_called()


@mock.patch.object(MainMenu, "start")
def test_update_state_without_next_state(start_mock):
    """
    The function to test the start function when the photometer does not have a next_state
    """
    photometer = Photometer()

    assert photometer.next_state is None
    photometer._update_state()
    start_mock.assert_not_called()


@mock.patch.object(Photometer, "_update_state")
@mock.patch.object(MainMenu, "loop")
def test_handle_ui(update_state_mock, loop_mock):
    """
    The function to test function calls of the handle_ui function
    """
    photometer = Photometer()

    photometer._handle_ui()
    update_state_mock.assert_called()
    loop_mock.assert_called()
