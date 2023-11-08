import threading
import telebot
from telebot import types


def telebot_main_cycle(bot):
    bot.infinity_polling(long_polling_timeout=1)


class TgBot:
    def __init__(self, api_token, user_id=None):
        self.__user_id = user_id
        self.__force_user_id = user_id is not None and not user_id
        self.__bot = telebot.TeleBot(api_token)

        @self.__bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if not self.__force_user_id:
                btn1 = types.KeyboardButton("/subscribe")
                btn2 = types.KeyboardButton("/unsubscribe")
                markup.add(btn1)
                markup.add(btn2)
                reply = 'Run /subscribe on /unsubscribe'
            else:
                reply = 'Force user id mode is enabled'
            self.__bot.send_message(message.from_user.id, reply, reply_markup=markup)

        @self.__bot.message_handler(commands=['subscribe'])
        def url(message):
            if self.__force_user_id:
                self.__bot.send_message(message.chat.id, "cannot subscribe, force user id mode is currently enabled")
                return
            self.__user_id = message.from_user.id
            self.__bot.send_message(message.chat.id, "subscribed!")

        @self.__bot.message_handler(commands=['unsubscribe'])
        def url(message):
            if self.__force_user_id:
                return
            self.__user_id = None
            self.__bot.send_message(message.chat.id, "unsubscribed")

        self.__thread = threading.Thread(target=telebot_main_cycle, args=[self.__bot])
        self.__thread.start()

    def stop(self):
        self.__bot.stop_bot()
        self.__thread.join()
        self.__bot = None

    def send_message(self, message):
        if self.__user_id is not None and self.__bot is not None:
            self.__bot.send_message(self.__user_id, message)

    __force_user_id = False
    __user_id = None
    __thread = None
    __bot = None
