from bot.config import bot
from bot.handlers.start import start





if __name__ == '__main__':
    print('Bot ishladi Hoji aka')
    bot.polling(none_stop=True)