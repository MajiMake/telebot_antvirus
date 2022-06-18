from telebot import types

from requesters import key_list

data_callback_list = []
admin_callback_list = []


def button_creator(callback, text):
    button = types.InlineKeyboardButton(text=text, callback_data=callback)
    return button


def product_buttons(admin=False):
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
