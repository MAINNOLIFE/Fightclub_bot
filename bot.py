import logging
import json
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

from generate_card import generate_card_image

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)

# مسیر فایل داده‌ها
DATA_FILE = "data.json"

# مراحل مکالمه
(NAME, AGE, FIGHTS, VICTORIES, RESISTANCE, STRENGTH, SPEED, RAGE, PHOTO) = range(9)

# خواندن و افزایش شماره عضویت
def get_next_number():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"last_number": 0}

    data["last_number"] += 1
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

    return f"{data['last_number']:03d}"  # مثل 001

# شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["number"] = get_next_number()
    await update.message.reply_text("به باشگاه مبارزان خوش آمدی! اسم مبارزتو بگو:")
    return NAME

async def get_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("سن چند ساله‌ته؟")
    return AGE

async def get_age(update, context):
    context.user_data["age"] = update.message.text
    await update.message.reply_text("تا حالا چند تا مبارزه داشتی؟")
    return FIGHTS

async def get_fights(update, context):
    context.user_data["fights"] = update.message.text
    await update.message.reply_text("چند تا پیروزی داشتی؟")
    return VICTORIES

async def get_victories(update, context):
    context.user_data["victories"] = update.message.text
    await update.message.reply_text("میزان مقاومت (0 تا 10):")
    return RESISTANCE

async def get_resistance(update, context):
    context.user_data["resistance"] = int(update.message.text)
    await update.message.reply_text("قدرت (0 تا 10):")
    return STRENGTH

async def get_strength(update, context):
    context.user_data["strength"] = int(update.message.text)
    await update.message.reply_text("سرعت (0 تا 10):")
    return SPEED

async def get_speed(update, context):
    context.user_data["speed"] = int(update.message.text)
    await update.message.reply_text("خشم؟ (0 تا 10):")
    return RAGE

async def get_rage(update, context):
    context.user_data["rage"] = int(update.message.text)
    await update.message.reply_text("حالا یه عکس از خودت بفرست:")
    return PHOTO

async def get_photo(update, context):
    photo_file = await update.message.photo[-1].get_file()
    image_path = f"user_{context.user_data['number']}.jpg"
    await photo_file.download_to_drive(image_path)
    context.user_data["photo_path"] = image_path

    # ساخت کارت نهایی
    card = generate_card_image(context.user_data)
    await update.message.reply_photo(photo=card, caption="کارت مبارزه‌ات آماده‌ست!")
    return ConversationHandler.END

# لغو عملیات
async def cancel(update, context):
    await update.message.reply_text("لغو شد.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# اجرای بات
def main():
    import os
TOKEN = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()
app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            FIGHTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fights)],
            VICTORIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_victories)],
            RESISTANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_resistance)],
            STRENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_strength)],
            SPEED: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_speed)],
            RAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_rage)],
            PHOTO: [MessageHandler(filters.PHOTO, get_photo)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
