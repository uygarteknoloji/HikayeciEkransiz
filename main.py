# main.py
import os
import random
import time
from gpiozero import Button
from signal import pause
from aclass_printer import AClassPrinter

BASE_DIR = "/home/admin/HikayeciEkransiz"

BUTTON_FOLDERS = {
    2: "io2",
    3: "io3",
    4: "io4"
}

# Yazıcıyı tek kez oluştur
printer = AClassPrinter()

def print_random_file(folder_name):
    folder_path = os.path.join(BASE_DIR, folder_name)

    if not os.path.isdir(folder_path):
        print(f"Klasör yok: {folder_path}")
        return

    txt_files = [
        f for f in os.listdir(folder_path)
        if f.endswith(".txt")
    ]

    if not txt_files:
        print(f"{folder_name} içinde txt yok")
        return

    selected = random.choice(txt_files)
    file_path = os.path.join(folder_path, selected)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"AClass yazıcıya gönderiliyor: {selected}")
        content += "\n" * 6
        content += "\f"
        content = content.encode("cp857", errors="replace")
        printer.print_text(content)
        printer.cut_paper()  # Kağıt kesme komutu

    except Exception as e:
        print(f"Yazdırma hatası: {e}")

# Butonlar
buttons = []

for pin, folder in BUTTON_FOLDERS.items():
    btn = Button(pin, pull_up=True, bounce_time=0.3)
    btn.when_pressed = lambda f=folder: print_random_file(f)
    buttons.append(btn)

print("AClass + gpiozero sistem hazır")

pause()