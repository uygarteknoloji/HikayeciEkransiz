# aclass_printer.py

class AClassPrinter:
    def __init__(self, device="/dev/usb/lp0"):
        self.device = device

    def print_text(self, text: str):
        with open(self.device, "wb") as printer:
            printer.write(text.encode("cp1254", errors="replace"))
            printer.write(b"\n\n\n\n")   # kağıt ilerlet