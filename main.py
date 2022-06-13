import telebot
from _token import token
from telebot import types
from requesters import key_list, get_code

bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start'])
def start_func(message):
    userID = message.from_user.firstname
    key_func(message)








@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'code':
        print(get_code)
    elif call.data == 'crypto':
        pass
    else:
        uuid = call.data
        print(uuid)
        markup_inline = types.InlineKeyboardMarkup()
        crypto = button_creator('crypto', 'Крипта')
        code = button_creator('code', 'По коду')
        markup_inline.add(crypto, code)
        bot.send_message(call.from_user.id, 'Выберите способ оплаты', reply_markup=markup_inline)





def button_creator(callback, text):
    button = types.InlineKeyboardButton(text=text, callback_data=callback)
    return button

def key_func(message):
    markup_inline = types.InlineKeyboardMarkup()
    count = 1
    button1 = None
    for dic in key_list:
        if count == 1:
            button1 = button_creator(dic['uuid'], dic['name'])
            count = 2
            if dic == key_list[-1]:
                markup_inline.add(button1)

        else:
            button2 = button_creator(dic['uuid'], dic['name'])
            markup_inline.add(button1, button2)
            count = 1

    bot.send_message(message.chat.id, 'Выберите ключ', reply_markup=markup_inline)

bot.infinity_polling()
