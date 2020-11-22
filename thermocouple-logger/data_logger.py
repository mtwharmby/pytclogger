import time

import serial


def process_input(serial_in):
    print(serial_in)


def read_device(ser_dev):
    with ser_dev as ser:
        while True:
            time.sleep(.5)
            while ser.in_waiting > 0:
                process_input(ser.read_until())


def main():
    read_device(serial.Serial("/dev/ttyACM0", 9600, timeout=10))


if __name__ == "__main__":
    main()
