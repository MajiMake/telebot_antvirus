from _token import token
from main import bot


class AV_key_bot:
    def __init__(self, bot):
        self.token = token
        self.bot = bot

    def __call__(self, *args, **kwargs):
        self.bot.infinity_polling()

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(self, message):
        self.bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(func=lambda m: True)
    def echo_all(self, message):
        self.bot.reply_to(message, message.text)