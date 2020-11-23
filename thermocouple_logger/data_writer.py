import os
import time


class DataWriter:

    def __init__(self, filename, start_time):
        self.filename = filename
        self.start_time = start_time

        # TODO Make "w" and warn if exists
        # TODO Needs test
        with open(self.filename, "a") as out_f:
            out_f.write(f"start_time={time.time()}{os.linesep}")
            out_f.write(
                "Offset Time [s],Reference Temperature [°C],Thermocouple "
                + f"Temperature [°C]{os.linesep}"
            )

    def write_data(self, data):
        time_offs = time.time() - self.start_time
        with open(self.filename, "a") as out_f:
            line = ",".join(str(v) for v in data.values())
            line = f"{time_offs},{line}{os.linesep}"
            out_f.write(line)
