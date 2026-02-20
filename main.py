from gpiozero import Button
from signal import pause
import os
import random
import subprocess
import time

BASE_DIR = "/home/admin/HikayeciEkransiz"

BUTTON_FOLDERS = {
    2: "io2",
    3: "io3",
    4: "io4"
}

def print_random_file(folder_name):
    folder_path = os.path.join(BASE_DIR, folder_name)

    if not os.path.isdir(folder_path):
        print(f"Klasï¿½r yok: {folder_path}")
        return

    txt_files = [
        f for f in os.listdir(folder_path)
        if f.endswith(".txt")
    ]

    if not txt_files:
        print(f"{folder_name} iï¿½inde txt yok")
        return

    selected = random.choice(txt_files)
    file_path = os.path.join(folder_path, selected)

    print(f"Yazdï¿½rï¿½lï¿½yor: {file_path}")
    subprocess.run(["lp", file_path])

# Butonlarï¿½ oluï¿½tur
buttons = []

for pin, folder in BUTTON_FOLDERS.items():
    btn = Button(pin, pull_up=True, bounce_time=0.3)

    # lambda iï¿½inde default arg kullanï¿½yoruz (closure bug ï¿½nlemi)
    btn.when_pressed = lambda f=folder: print_random_file(f)

    buttons.append(btn)

print("Sistem hazï¿½r (gpiozero)...")

pause()  # programï¿½ ayakta tutar