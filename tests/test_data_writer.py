import os
from pytclogger.data_writer import DataWriter


def test_write_data(monkeypatch, mocker):
    # TODO Move to fixture
    # Mock the open builtin. open returns open, so we set __enter__() to
    # return the mock. Set the write function to return something first!
    open_mock = mocker.MagicMock(name="open_mock")
    open_mock.write().return_value = mocker.MagicMock(name="write_mock")
    open_mock.__enter__().return_value = open_mock
    mocker.patch("builtins.open", open_mock)

    # Ensure that we always get the same unix time stamp
    fake_time = 1606084461.7003403
    monkeypatch.setattr("time.time", lambda: fake_time)

    dw = DataWriter("outfile.csv", 1606084449.7003403)
    dw.write_data({"int_temp": 25.6, "tc_temp": 23.4})
    open_mock.assert_called_with("outfile.csv", "a")
    open_mock().__enter__().write.assert_called_with(
        f"12.0,25.6,23.4{os.linesep}"
    )
