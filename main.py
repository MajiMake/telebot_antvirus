import telebot
from _token import token
from telebot import types
from requesters import key_list, get_code, buy_key

bot = telebot.TeleBot(token=token)
uuid = None


@bot.message_handler(commands=['start'])
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
    code = button_creator('code', 'По коду')
    markup_inline.add(code)

    bot.send_message(message.chat.id, 'Выберите ключ', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global uuid
    if call.data == 'code':
        msg = bot.send_message(call.from_user.id, 'Введите промокод')
        bot.register_next_step_handler(msg, had_pass)

    elif call.data == 'crypto':
        print('zaebis')
        buy_key(uuid, call.from_user.id)
        pass

    else:
        uuid = call.data
        markup_inline = types.InlineKeyboardMarkup()
        crypto = button_creator('crypto', 'Крипта')
        markup_inline.add(crypto)
        bot.send_message(call.from_user.id, 'Выберите способ оплаты', reply_markup=markup_inline)


def had_pass(message):
    try:
        int(message.text)
        get_code(message.chat.id, message.text)

    except ValueError:
        if message.text == '/start':
            key_func()
        else:
            msg = bot.send_message(message.chat.id, "Код неверен")
            bot.register_next_step_handler(msg, had_pass)


def button_creator(callback, text):
    button = types.InlineKeyboardButton(text=text, callback_data=callback)
    return button

bot.infinity_polling()
