import telebot
import json


API_KEY = "6006311344:AAFpHrQxkGXuRANJAo-MCQxJIL992DJmwRA"
bot = telebot.TeleBot(API_KEY)


#file_dict = {}

# Loop through the filenames of each file
#for filename in ['file1.txt', 'file2.txt', 'file3.txt']:
  # Open the file and read in its contents
 # with open(filename, 'r') as f:
 #   contents = f.read()
  # Store the contents as a value in our dictionary, using the filename as a key
 # file_dict[filename] = contents
  
# Write the dictionary to a JSON file
#with open('all_files.json', 'w') as f:
  #json.dump(file_dict, f)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, welcome)
        
with open('text.txt', 'r') as file:
    welcome = file.read()
    
@bot.message_handler(commands=['puk'])
def puk_support(message):
    bot.send_message(message.chat.id ,"Customer Support: Thank you for calling Ethiotelecom customer service. How may I assist you today?")

@bot.message_handler(commands=['support'])
def pkg_support (message):
    bot.send_message(message.chat.id ,"1. Ethio-telecom's Unlimited Voice and SMS package - This package is ideal for people who communicate through voice calls and SMS frequently. It offers unlimited voice calls and SMS within Ethiotelecom's network for a monthly fee.")

@bot.message_handler(commands=['wifi'])
def wifi_support (message):
    bot.send_message(message.chat.id ,"wifi reports")


@bot.message_handler(commands=['rewards'])
def rewards (message):
    bot.send_message(message.chat.id , "rewards")



#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#	bot.reply_to(message, message.text)

bot.infinity_polling()