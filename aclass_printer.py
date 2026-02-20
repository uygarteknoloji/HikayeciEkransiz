# aclass_printer.py
import serial

class AClassPrinter:
    def __init__(self, port="/dev/usb/lp0", baudrate=9600):
        self.port = port
        self.baudrate = baudrate

    def print_text(self, text: str):
        with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
            ser.write(text.encode("utf-8"))
            ser.write(b"\n\n")