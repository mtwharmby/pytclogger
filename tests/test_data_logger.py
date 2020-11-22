import mock
import serial

from thermocouple_logger.data_logger import read_device, prepare_input


@mock.patch("thermocouple_logger.data_logger.process_input")
def test_read_device(patch_proc_in, mocker):
    ser_dev = mocker.create_autospec(serial.Serial)
    # We only want the inner while loop to run once, so set in_waiting to 0\
    # after the first call
    type(ser_dev.__enter__()).in_waiting = mocker.PropertyMock(side_effect=[10, 0])
    ser_dev.__enter__().read_until.return_value = b"Test Serial Text\r\n"

    read_device(ser_dev, test=True)
    patch_proc_in.assert_called_with(b"Test Serial Text\r\n")


def test_prepare_input():
    reading = b"int_temp=25.6;tc_temp=23.4;\r\n"
    assert prepare_input(reading) == {"int_temp": 25.6, "tc_temp": 23.4}
