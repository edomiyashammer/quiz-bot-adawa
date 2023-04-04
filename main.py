import telebot

API_KEY = "6006311344:AAFpHrQxkGXuRANJAo-MCQxJIL992DJmwRA"
bot = telebot.TeleBot(API_KEY)



@bot.message_handler(commands=['start'])
def greet(message):
    bot.reply_to(message, "this is the new telegram bot that created to help")



bot.polling()
