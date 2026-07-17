import os
import math

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    os.system('pip install Pillow')
    from PIL import Image, ImageDraw, ImageFont

WIDTH = 1920
HEIGHT = 500
FRAMES = 60
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'baner nwe.png')

def get_font(size):
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/ariblk.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def draw_gradient(draw, w, h):
    for y in range(h):
        r = int(20 + (y / h) * 30)
        g = int(10 + (y / h) * 20)
        b = int(60 + (y / h) * 40)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def draw_coin(draw, cx, cy, radius, alpha):
    color = (255, 215, 0, alpha)
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color, outline=(200, 170, 0, alpha), width=2)
    inner = radius * 0.6
    draw.ellipse([cx - inner, cy - inner, cx + inner, cy + inner], outline=(200, 170, 0, alpha), width=1)

def make_frame(frame_num):
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    draw_gradient(draw, WIDTH, HEIGHT)

    for i in range(25):
        x = (i * 97 + frame_num * (2 + i % 3)) % WIDTH
        y = (i * 53 + frame_num * (1 + i % 2)) % HEIGHT
        alpha = int(100 + 80 * math.sin(frame_num * 0.1 + i))
        radius = 8 + (i % 5) * 3
        draw_coin(draw, x, y, radius, alpha)

    cx, cy = WIDTH // 2, HEIGHT // 2

    draw.rounded_rectangle([cx - 620, cy - 180, cx + 620, cy + 180], radius=30, fill=(0, 0, 0, 120))

    draw.rounded_rectangle([cx - 600, cy - 160, cx + 600, cy + 160], radius=25, outline=(255, 215, 0, 200), width=3)

    font_big = get_font(72)
    font_mid = get_font(42)
    font_btn = get_font(38)
    font_small = get_font(30)

    glow_offset = int(3 * math.sin(frame_num * 0.15))

    title = "SAVE 7% Cash Back on AliExpress!"
    bbox = draw.textbbox((0, 0), title, font=font_big)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw // 2 + glow_offset, cy - 130), title, fill=(255, 255, 255), font=font_big)

    sub = "Sign up for FREE on Rakuten and get cashback every time you shop"
    bbox2 = draw.textbbox((0, 0), sub, font=font_mid)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx - tw2 // 2, cy - 30), sub, fill=(220, 220, 220), font=font_mid)

    btn_w, btn_h = 400, 60
    btn_x = cx - btn_w // 2
    btn_y = cy + 60
    pulse = int(4 * math.sin(frame_num * 0.2))
    draw.rounded_rectangle([btn_x - pulse, btn_y - pulse, btn_x + btn_w + pulse, btn_y + btn_h + pulse], radius=30, fill=(220, 30, 30))

    btn_text = ">> JOIN NOW - IT'S FREE <<"
    bbox3 = draw.textbbox((0, 0), btn_text, font=font_btn)
    tw3 = bbox3[2] - bbox3[0]
    draw.text((cx - tw3 // 2, btn_y + 8), btn_text, fill=(255, 255, 255), font=font_btn)

    note = "Use code: HICHEM107 | Works on AliExpress, Walmart, eBay & 3500+ stores"
    bbox4 = draw.textbbox((0, 0), note, font=font_small)
    tw4 = bbox4[2] - bbox4[0]
    draw.text((cx - tw4 // 2, cy + 140), note, fill=(180, 180, 180), font=font_small)

    return img.convert('RGB')

print("Generating animated banner...")
frames = []
for i in range(FRAMES):
    frames.append(make_frame(i))
    if (i + 1) % 10 == 0:
        print(f"  Frame {i + 1}/{FRAMES}")

gif_path = OUTPUT.replace('.png', '.gif')
frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=80, loop=0)
print(f"Animated GIF saved: {gif_path}")

frames[-1].save(OUTPUT)
print(f"Static PNG saved: {OUTPUT}")
print("Done!")
