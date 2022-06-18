from _token import token

import telebot
from telebot import types

from buttons import button_creator

bot = telebot.TeleBot(token=token)


def admin_creator(message):
    administrator = Admin(message)
    return administrator


class Admin:

    def __init__(self, message):
        self.id = message.chat_id
        self.name = message.chat_id.username


def admin_list(id):
    adm = []
    with open('adminlist', 'r') as adminlist:
        for admin in adminlist:
            adm.append(int(admin))

    if id in adm:
        return True


def add_admin(id):
    with open('adminlist', 'a') as adminlist:
        adminlist.write(id + '\n')


def add_key_step_2(message, uuid):
    handler = message.text
    handler = handler.split(' ')
    key_json = {}
    key_json[uuid] = handler
    print(key_json)
    markup_inline = types.InlineKeyboardMarkup()
    yes = button_creator('yes_add_key_step_2', 'ДА')
    no = button_creator('no_add_key_step_2', 'НЭТ')
    markup_inline.add(yes, no)
    bot.send_message(message.chat.id, 'Хотите добавить еще ключей?', reply_markup=markup_inline)


def admin_keyup(call):
    uuid = call.data
    msg = bot.send_message(call.from_user.id, "Введите ключи через пробел")
    bot.register_next_step_handler(msg, add_key_step_2, uuid=uuid)


def admin_start(message):
    markup_inline = types.InlineKeyboardMarkup()
    add_key = button_creator('add_key', 'Добавить ключ')
    markup_inline.add(add_key)
    bot.send_message(message.chat.id, 'Вы вошли в админку, выберите действие', reply_markup=markup_inline)


def admin_init(message):
    print(message.chat.id)
    if admin_list(message.chat.id) is True:
        admin_start(message)

    else:
        bot.send_message(message.chat.id, 'У вас нет прав доступа')
