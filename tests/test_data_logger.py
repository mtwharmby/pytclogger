import os
import serial

import thermocouple_logger.data_logger
from thermocouple_logger.data_logger import (
    read_device, prepare_input, process_input
)


def test_read_device(mocker):
    patch_proc_in = mocker.patch(
        "thermocouple_logger.data_logger.process_input"
    )
    ser_dev = mocker.create_autospec(serial.Serial)
    # We only want the inner while loop to run once, so set in_waiting to 0\
    # after the first call
    type(ser_dev.__enter__()).in_waiting = mocker.PropertyMock(
        side_effect=[10, 0]
    )
    ser_dev.__enter__().read_until.return_value = b"Test Serial Text\r\n"

    read_device(ser_dev, test=True)
    patch_proc_in.assert_called_with(b"Test Serial Text\r\n")


# TODO Add additional cases - e.g. start up
def test_prepare_input():
    reading = b"int_temp=25.6;tc_temp=23.4;\r\n"
    assert prepare_input(reading) == {"int_temp": 25.6, "tc_temp": 23.4}


def test_process_input(monkeypatch, mocker):
    # Patch prepare_input.
    # N.B. lambda x is needed as prepare_input takes one argument.
    monkeypatch.setattr(thermocouple_logger.data_logger, "prepare_input",
                        lambda x: {"int_temp": 25.6, "tc_temp": 23.4})

    # Mock the open builtin. open returns open, so we set __enter__() to
    # return the mock. Set the write function to return something first!
    open_mock = mocker.MagicMock(name="open_mock")
    open_mock.write().return_value = mocker.MagicMock(name="write_mock")
    open_mock.__enter__().return_value = open_mock
    mocker.patch("builtins.open", open_mock)

    process_input(b"int_temp=25.6;tc_temp=23.4;\r\n", "outfile.csv")
    open_mock.assert_called_with("outfile.csv", "a")
    open_mock().__enter__().write.assert_called_with(f"25.6,23.4{os.linesep}")
