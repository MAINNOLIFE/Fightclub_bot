from PIL import Image, ImageDraw, ImageFont
import io

def draw_bars(draw, x, y, value, max_length=10):
    bar_width = 15
    for i in range(max_length):
        fill = "gold" if i < value else "lightgray"
        draw.rectangle([x + i*bar_width, y, x + i*bar_width + 10, y + 10], fill=fill)

def generate_card_image(data):
    # پس‌زمینه سفید
    img = Image.new("RGB", (600, 400), "ivory")
    draw = ImageDraw.Draw(img)

    # فونت
    font = ImageFont.load_default()

    # عکس کاربر
    user_photo = Image.open(data["photo_path"]).resize((100, 100))
    img.paste(user_photo, (20, 20))

    # اثر انگشت
    fingerprint = Image.open("templates/fingerprint.png").resize((80, 80))
    img.paste(fingerprint, (500, 300))

    # نوشتن متن‌ها
    draw.text((140, 20), f"Name: {data['name']}", font=font, fill="black")
    draw.text((140, 40), f"Age: {data['age']}", font=font, fill="black")
    draw.text((140, 60), f"Number: {data['number']}", font=font, fill="black")
    draw.text((140, 80), f"Status: ACTIVE", font=font, fill="black")
    draw.text((140, 100), f"Fights: {data['fights']}", font=font, fill="black")
    draw.text((140, 120), f"Victories: {data['victories']}", font=font, fill="black")

    # نوار قدرت‌ها
    draw.text((30, 160), "Resistance:", font=font, fill="black")
    draw_bars(draw, 150, 160, data["resistance"])

    draw.text((30, 180), "Strength:", font=font, fill="black")
    draw_bars(draw, 150, 180, data["strength"])

    draw.text((30, 200), "Speed:", font=font, fill="black")
    draw_bars(draw, 150, 200, data["speed"])

    draw.text((30, 220), "Rage:", font=font, fill="black")
    draw_bars(draw, 150, 220, data["rage"])

    # ذخیره در بایت
    output = io.BytesIO()
    img.save(output, format='JPEG')
    output.seek(0)
    return output
