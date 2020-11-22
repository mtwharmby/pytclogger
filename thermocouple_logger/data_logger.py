import os
import time

import serial


def prepare_input(serial_in):
    data = serial_in.decode("utf-8").strip().strip(";")
    data = data.split(";")

    return {d_item.split("=")[0]: float(d_item.split("=")[1])
            for d_item in data}


def process_input(serial_in, filename):
    data = prepare_input(serial_in)

    with open(filename, "a") as out_f:
        line = ",".join(str(v) for v in data.values())
        line = f"{line}{os.linesep}"
        out_f.write(line)


def read_device(ser_dev, test=False):
    with ser_dev as ser:
        while True:
            time.sleep(.5)
            while ser.in_waiting > 0:
                process_input(ser.read_until())

            if test:
                # Break after out of infinite loop
                break


def main():
    read_device(serial.Serial("/dev/ttyACM0", 9600, timeout=10))


if __name__ == "__main__":
    main()
