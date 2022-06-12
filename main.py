import telebot
from _token import token
from telebot import types

bot = telebot.TeleBot(token=token)

@bot.message_handler(func=lambda message: True)
def buttons(message):
	markup_inline = types.InlineKeyboardMarkup()
	item_yes = types.InlineKeyboardButton(text= 'ДА', callback_data='y')
	item_no = types.InlineKeyboardButton(text='НЕТ', callback_data='n')

	markup_inline.add(item_yes, item_no)
	bot.send_message(message.chat.id, 'Желаете узнать небольшую информацию о вас',
		reply_markup=markup_inline
	)

bot.callback_query_handler(func = lambda call: True)
def answer(call):
	if call.data =='yes':
		pass
	if call.data == 'no':
		pass

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Test, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()
