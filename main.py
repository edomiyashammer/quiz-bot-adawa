
import telebot
import config
import pb
import pytz
import json
import traceback

bot = telebot.TeleBot(config.TOKEN)
bot.polling(none_stop=True)

API_KEY = "6006311344:AAFpHrQxkGXuRANJAo-MCQxJIL992DJmwRA"
bot = telebot.TeleBot(API_KEY)



@bot.message_handler(commands=['start'])
def greet(message):
    bot.reply_to(message, "this is the new telegram bot that created to help")

@bot.message_handler(commands=['help'])
def help_command(message):
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.add(
       telebot.types.InlineKeyboardButton(
           ‘Message the developer’, url='telegram.me/artiomtb'
       )
   )
   bot.send_message(
       message.chat.id,
       '1) To receive a list of available currencies press /exchange.\n' +
       '2) Click on the currency you are interested in.\n' +
       '3) You will receive a message containing information regarding the source and the target currencies, ' +
       'buying rates and selling rates.\n' +
       '4) Click “Update” to receive the current information regarding the request. ' +
       'The bot will also show the difference between the previous and the current exchange rates.\n' +
       '5) The bot supports inline. Type @<botusername> in any chat and the first letters of a currency.',
       reply_markup=keyboard
   )


bot.polling()
