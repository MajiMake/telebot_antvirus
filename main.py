import telebot
from _token import token
from telebot import types
from requesters import key_list, get_code, buy_key, add_key
from admin import admin_list

bot = telebot.TeleBot(token=token)
uuid = None


@bot.message_handler(commands=['start'])
def key_func(message):
    print(message.chat.id)
    if admin_list(message.chat.id) is True:
        markup_inline = types.InlineKeyboardMarkup()
        add_key = button_creator('add_key', 'Добавить ключ')
        markup_inline.add(add_key)
        bot.send_message(message.chat.id, 'Вы вошли в админку, выберите действие', reply_markup=markup_inline)

    else:
        markup_inline = product_buttons()
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

    elif call.data == 'add_key' or call.data == 'yes_add_key_step_2':
        markup_inline = product_buttons()
        bot.send_message(call.from_user.id, 'Выберите версию', reply_markup=markup_inline)
        print(call.data)

    elif call.data == 'no_add_key_step_2':
        bot.send_message(call.from_user.id, 'Ну пиздец тогда, я больше нихуя не умею')


    else:
        uuid = call.data
        if admin_list(call.from_user.id) is True:
            msg = bot.send_message(call.from_user.id, "Введите ключи через запятую")
            bot.register_next_step_handler(msg, add_key_step_2, uuid=uuid)

        else:
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


def product_buttons():
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

    return markup_inline


def add_key_step_2(message, uuid):
    handler = message.text
    handler = handler.split(',')
    key_json = {}
    key_json[uuid] = handler
    print(key_json)
    markup_inline = types.InlineKeyboardMarkup()
    yes = button_creator('yes_add_key_step_2', 'ДА')
    no = button_creator('no_add_key_step_2', 'НЭТ')
    markup_inline.add(yes, no)
    bot.send_message(message.chat.id, 'Хотите добавить еще ключей?', reply_markup=markup_inline)


bot.infinity_polling()
