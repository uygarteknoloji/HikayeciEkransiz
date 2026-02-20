# main.py
import os
import random
import textwrap
from gpiozero import Button
from signal import pause
from escpos.printer import Usb
from PIL import Image, ImageDraw, ImageFont

TITLE_FONT_SIZE = 34
BODY_FONT_SIZE = 24
LINE_SPACING = 10

title_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", TITLE_FONT_SIZE
)
body_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", BODY_FONT_SIZE
)

BASE_DIR = "/home/admin/HikayeciEkransiz"

BUTTON_FOLDERS = {
    2: "io2",
    3: "io3",
    4: "io4"
}

printer = Usb(
    idVendor=0x0483,   # Ã¶rnek â†’ KENDÄ° YAZICINA GÃ–RE DEÄÄ°ÅTÄ°R
    idProduct=0x5740,  # Ã¶rnek â†’ KENDÄ° YAZICINA GÃ–RE DEÄÄ°ÅTÄ°R
    in_ep=0x81,
    out_ep=0x01
)

def print_image_to_printer(image_path):
    printer.image(image_path)
    printer.cut()

def text_to_image_80mm(file_path, output_path="print_temp.png"):
    WIDTH = 560  # 80mm gÃ¼venli alan
    MARGIN_X = 20
    MARGIN_Y = 20

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    title = lines[0]
    body = lines[1:]

    wrapped_body = []
    for line in body:
        wrapped_body.extend(textwrap.wrap(
            line, width=55, replace_whitespace=False
        ) or [""])

    title_height = title_font.getbbox("Ay")[3]
    body_height = body_font.getbbox("Ay")[3]

    total_height = (
        MARGIN_Y +
        title_height + 20 +
        len(wrapped_body) * (body_height + LINE_SPACING) +
        40
    )

    img = Image.new("L", (WIDTH, total_height), 255)
    draw = ImageDraw.Draw(img)

    # ğŸ”¹ BaÅŸlÄ±k (ortalanmÄ±ÅŸ)
    title_width = draw.textlength(title, font=title_font)
    draw.text(
        ((WIDTH - title_width) // 2, MARGIN_Y),
        title,
        font=title_font,
        fill=0
    )

    y = MARGIN_Y + title_height + 20

    # ğŸ”¹ GÃ¶vde
    for line in wrapped_body:
        draw.text(
            (MARGIN_X, y),
            line,
            font=body_font,
            fill=0
        )
        y += body_height + LINE_SPACING

    # ğŸ”¹ Otomatik ayraÃ§
    draw.line(
        (MARGIN_X, y + 10, WIDTH - MARGIN_X, y + 10),
        fill=0,
        width=2
    )

    img.save(output_path)



def print_random_file(folder_name):
    folder_path = os.path.join(BASE_DIR, folder_name)

    if not os.path.isdir(folder_path):
        print(f"KlasÃ¶r yok: {folder_path}")
        return

    txt_files = [
        f for f in os.listdir(folder_path)
        if f.endswith(".txt")
    ]

    if not txt_files:
        print(f"{folder_name} iÃ§inde txt yok")
        return

    selected = random.choice(txt_files)
    file_path = os.path.join(folder_path, selected)

    try:
        text_to_image_80mm(file_path, "print_temp.png")
        print_image_to_printer("print_temp.png")
        print(f"YazdÄ±rÄ±ldÄ±: {selected}")
    except Exception as e:
        print(f"YazdÄ±rma hatasÄ±: {e}")

# Butonlar
buttons = []

for pin, folder in BUTTON_FOLDERS.items():
    btn = Button(pin, pull_up=True, bounce_time=0.3)
    btn.when_pressed = lambda f=folder: print_random_file(f)
    buttons.append(btn)

print("AClass + gpiozero sistem hazÄ±r")

pause()