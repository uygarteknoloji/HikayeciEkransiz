import os
import random
import textwrap
import time
from gpiozero import Button
from signal import pause
from escpos.printer import Usb
from PIL import Image, ImageDraw, ImageFont
from threading import Thread

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
LOGO_PATH = "/home/admin/HikayeciEkransiz/logo.png" # Logo dosyanın yolu

BUTTON_FOLDERS = {
    2: "io2",
    3: "io3",
    4: "io4"
}

# Mevcut satï¿½rï¿½ ï¿½ununla deï¿½iï¿½tirmeyi dene:
printer = Usb(
    0x0483, 
    0x5840, 
    in_ep=0x81, 
    out_ep=0x03, 
    profile="TM-T88V" # Genel bir 80mm profili iï¿½ gï¿½recektir
)

def handle_button(folder):
    Thread(
        target=print_random_file,
        args=(folder,),
        daemon=True
    ).start()


def print_image_to_printer(image_path):
    printer.image(image_path)
    time.sleep(0.2)
    printer.cut()
    time.sleep(0.2)

def text_to_image_80mm(file_path, output_path="print_temp.png"):
    WIDTH = 512 # Daha önce belirlediğimiz çalışan genişlik
    MARGIN_X = 20
    MARGIN_Y = 20

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    title = lines[0]
    body = lines[1:]

    wrapped_body = []
    for line in body:
        wrapped_body.extend(textwrap.wrap(line, width=45, replace_whitespace=False) or [""])

    title_height = title_font.getbbox("Ay")[3]
    body_height = body_font.getbbox("Ay")[3]
    
    # Logo yüksekliğini hesapla
    logo_img = None
    logo_height = 0
    if os.path.exists(LOGO_PATH):
        logo_img = Image.open(LOGO_PATH).convert("L")
        # Logoyu yazıcı genişliğine göre orantılı boyutlandır (isteğe bağlı)
        logo_aspect = logo_img.height / logo_img.width
        new_logo_width = 200 # Logonun çok büyük olmaması için sabit genişlik
        logo_height = int(new_logo_width * logo_aspect)
        logo_img = logo_img.resize((new_logo_width, logo_height))

    total_height = (
        MARGIN_Y + title_height + 20 +
        len(wrapped_body) * (body_height + LINE_SPACING) +
        40 + logo_height + 40 # Logo alanı ve boşluklar
    )

    img = Image.new("L", (WIDTH, total_height), 255)
    draw = ImageDraw.Draw(img)

    # Başlık
    title_width = draw.textlength(title, font=title_font)
    draw.text(((WIDTH - title_width) // 2, MARGIN_Y), title, font=title_font, fill=0)

    y = MARGIN_Y + title_height + 20

    # Gövde
    for line in wrapped_body:
        draw.text((MARGIN_X, y), line, font=body_font, fill=0)
        y += body_height + LINE_SPACING

    # Ayraç Çizgisi
    draw.line((MARGIN_X, y + 10, WIDTH - MARGIN_X, y + 10), fill=0, width=2)
    y += 30

    # LOGO EKLEME
    if logo_img:
        logo_x = (WIDTH - logo_img.width) // 2 # Ortala
        img.paste(logo_img, (logo_x, y))

    img.save(output_path)



def print_random_file(folder_name):
    folder_path = os.path.join(BASE_DIR, folder_name)

    if not os.path.isdir(folder_path):
        print(f"KlasÃƒÂ¶r yok: {folder_path}")
        return

    txt_files = [
        f for f in os.listdir(folder_path)
        if f.endswith(".txt")
    ]

    if not txt_files:
        print(f"{folder_name} iÃƒÂ§inde txt yok")
        return

    selected = random.choice(txt_files)
    file_path = os.path.join(folder_path, selected)

    # print_random_file fonksiyonundaki try-except bloï¿½unu bï¿½yle gï¿½ncelle:
    try:
        output = f"/tmp/print_{os.getpid()}_{random.randint(1000,9999)}.png"
        text_to_image_80mm(file_path, output)
        print_image_to_printer(output)  # Bu satï¿½r yeterli
        
        # Geï¿½ici dosyayï¿½ temizle
        if os.path.exists(output):
            os.remove(output)
            
        print(f"Baï¿½arï¿½yla yazdï¿½rï¿½ldï¿½: {selected}")
    except Exception as e:
        print(f"Yazdï¿½rma hatasï¿½ oluï¿½tu: {e}")

# Butonlar
buttons = []

for pin, folder in BUTTON_FOLDERS.items():
    btn = Button(pin, pull_up=True, bounce_time=0.3)
    btn.when_pressed = lambda f=folder: handle_button(f)
    buttons.append(btn)

print("AClass + gpiozero sistem hazÃ„Â±r")

pause()