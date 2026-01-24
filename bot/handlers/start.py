from bot.config import bot

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Assalomu aleykum Hush Kelibsiz\n\n"
        f"Sizning Telegram ID: <code>{message.chat.id}</code>\n\n"
        f"Ushbu ID ni nusxalab olib, veb-saytimizda profilingizga qo'shishingiz mumkin.\n\n"
        f"Undan so'ng ushbu bot sizga saytimiz yangiliklarini yetkazib turadi.\n\n"
        f"Kuningiz hayrli o'tsin",
        parse_mode='HTML'
    )