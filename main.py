
import telebot
from requests.exceptions import MissingSchema

from _token import token
from telebot import types
from requesters import key_list, get_code

bot = telebot.TeleBot(token=token)

class Antivirus_keybot:
    def __init__(self):
        self.token = token
        self.message = None

        @bot.message_handler(commands=['start'])
        def start_func(message):
            self.message = message
            self.key_func()

        @bot.callback_query_handler(func=lambda call: True)
        def answer_func(call):
            self.answer(call)


    def start_func(self):
        bot.infinity_polling()

    def key_func(self):
        markup_inline = types.InlineKeyboardMarkup()
        count = 1
        button1 = None
        for dic in key_list:
            if count == 1:
                button1 = self.button_creator(dic['uuid'], dic['name'])
                count = 2
                if dic == key_list[-1]:
                    markup_inline.add(button1)

            else:
                button2 = self.button_creator(dic['uuid'], dic['name'])
                markup_inline.add(button1, button2)
                count = 1
        code = self.button_creator('code', 'По коду')
        markup_inline.add(code)

        bot.send_message(self.message.chat.id, 'Выберите ключ', reply_markup=markup_inline)


    def answer(self, call):
        if call.data == 'code':
            bot.send_message(call.from_user.id, 'Введите промокод')

            @bot.message_handler(func=lambda message: True)
            def had_pass(message):
                try:
                    get_code(message.chat.id, message.text)
                    bot.send_message(message.chat.id, 'Код принят')
                except MissingSchema:
                    bot.send_message(message.chat.id, "пароль говно")

        elif call.data == 'crypto':
            pass

        else:
            uuid = call.data
            print(uuid)
            markup_inline = types.InlineKeyboardMarkup()
            crypto = self.button_creator('crypto', 'Крипта')
            markup_inline.add(crypto)
            bot.send_message(call.from_user.id, 'Выберите способ оплаты', reply_markup=markup_inline)


    def button_creator(self, callback, text):
        button = types.InlineKeyboardButton(text=text, callback_data=callback)
        return button

bott = Antivirus_keybot()
if __name__ == '__main__':
    bott.start_func()



