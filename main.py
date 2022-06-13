import telebot
from _token import token
from telebot import types

bot = telebot.TeleBot(token=token)
list = {'1': 'a', '2': 'б', '3': 'в', '4': 'г', '5': 'д', '6': 'е', '7': 'ж', '8': 'з', '9': 'й', '10': 'к',
        }


@bot.message_handler(commands=['start'])
def start_func(message):
    markup_inline = types.InlineKeyboardMarkup()
    count = 1
    button1 = None
    for callback, text in list.items():
        if count == 1:
            button1 = button_creator(callback, text)
            count = 2
        else:
            button2 = button_creator(callback, text)
            markup_inline.add(button1,button2)

    bot.send_message(message.chat.id, 'Выберите ключ', reply_markup=markup_inline)



@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'y':
        markup_inline = types.InlineKeyboardMarkup()
        one_pc = button_creator('1pc', '1 ПК')
        three_pc = button_creator('3pc', '3 ПК')
        markup_inline.add(one_pc, three_pc)
        bot.send_message(call.from_user.id, 'на сколько пк',
                         reply_markup=markup_inline
                         )
        bot.send_message(call.message.chat.id, type(call.message.chat.id))


def button_creator(callback, text):
    button = types.InlineKeyboardButton(text=text, callback_data=callback)
    return button


bot.infinity_polling()
