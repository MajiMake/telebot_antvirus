import telebot
from _token import token
from telebot import types

from admin import admin_init, admin_list, admin_keyup
from buttons import product_buttons, button_creator
from requesters import get_code, buy_key, key_list

bot = telebot.TeleBot(token=token)
uuid = None
admin = False

@bot.message_handler(commands=['admin'])
def call_admin_start(message):
    global admin
    if admin_list(message.chat.id):
        admin = True
        admin_init(message)
    else:
        bot.send_message(message.chat.id, 'Ты не одмен сука')

@bot.message_handler(commands=['start'])
def key_func(message):
    markup_inline = product_buttons(admin=False)
    code = button_creator('code', 'По коду')
    markup_inline.add(code)
    bot.send_message(message.chat.id, 'Выберите ключ', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    print(call.data)
    if call.data[1] == 'code':
        msg = bot.send_message(call.from_user.id, 'Введите промокод')
        bot.register_next_step_handler(msg, had_pass)

    elif call.data == 'crypto':
        print('zaebis')
        buy_key(uuid, call.from_user.id)

    elif call.data == 'add_key' or call.data == 'yes_add_key_step_2':
        markup_inline = product_buttons(admin=True)
        bot.send_message(call.from_user.id, 'Выберите версию', reply_markup=markup_inline)
        print(call.data)

    elif call.data == 'no_add_key_step_2':
        bot.send_message(call.from_user.id, 'Ну пиздец тогда, я больше нихуя не умею')

    else:
        if admin is True:
            admin_keyup(call)

        else:
            choose_product(call)


def choose_product(call):
    global uuid
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


def callback_list_taker(switch=False):
    if switch is False:
        return False
    else:
        callback_list = []
        for directory in key_list:
            callback_list.append(directory['uuid'])
        return callback_list



bot.infinity_polling()
