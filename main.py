import telebot

API_KEY = "6006311344:AAFpHrQxkGXuRANJAo-MCQxJIL992DJmwRA"
bot = telebot.TeleBot(API_KEY)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()