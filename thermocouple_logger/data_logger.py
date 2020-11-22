import re
import time

import serial

from .data_writer import DataWriter


def prepare_input(serial_in):
    # TODO Make into class
    temp_patt = re.compile(br"int_temp=(?P<int_temp>\d+\.\d+);tc_temp=(?P<tc_temp>\d+\.\d+);\r\n")
    for temp_match in temp_patt.finditer(serial_in):
        data = temp_match.groupdict()
        for k, v in data.items():
            data[k] = float(v)

    return data


def process_input(serial_in, handlers):
    data = prepare_input(serial_in)

    for proc in handlers:
        proc.write_data(data)


def read_device(ser_dev, handlers, test=False):
    with ser_dev as ser:
        while True:
            time.sleep(.5)
            while ser.in_waiting > 0:
                process_input(ser.read_until(), handlers)

            if test:
                # Break after out of infinite loop
                break


def main():
    filename = "outfile.csv"
    start_time = time.time()
    handlers = []
    handlers.append(DataWriter(filename, start_time))
    read_device(serial.Serial("/dev/ttyACM0", 9600, timeout=10), handlers)


if __name__ == "__main__":
    main()
