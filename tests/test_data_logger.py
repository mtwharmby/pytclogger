import serial

from pytclogger.data_logger import read_device, process_input


def test_read_device(mocker):
    patch_proc_in = mocker.patch(
        "pytclogger.data_logger.process_input"
    )
    ser_dev = mocker.create_autospec(serial.Serial)
    # We only want the inner while loop to run once, so set in_waiting to 0\
    # after the first call
    type(ser_dev.__enter__()).in_waiting = mocker.PropertyMock(
        side_effect=[10, 0]
    )
    ser_dev.__enter__().read_until.return_value = b"Test Serial Text\r\n"

    read_device(ser_dev, [], test=True)
    patch_proc_in.assert_called_with(b"Test Serial Text\r\n", [])


# TODO Add additional cases - e.g. start up
def test_process_input(mocker):
    reading = b"int_temp=25.6;tc_temp=23.4;\r\n"
    dummy_handler = mocker.MagicMock()

    process_input(reading, [dummy_handler])
    dummy_handler.write_data.assert_called_once()
    dummy_handler.write_data.assert_called_with(
        {"int_temp": 25.6, "tc_temp": 23.4}
    )
