from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import randint

bot = Bot(token='6006311344:AAFpHrQxkGXuRANJAo-MCQxJIL992DJmwRA')
dp = Dispatcher(bot)

button1 = InlineKeyboardButton(text="🧑🏻‍💻 button1", callback_data="randomvalue_of10")
button2 = InlineKeyboardButton(text="📵 button2", callback_data="randomvalue_of20")
button3 = InlineKeyboardButton(text="📶 button1", callback_data="randomvalue_of30")
button4 = InlineKeyboardButton(text="🏆 button2", callback_data="randomvalue_of40")
button5 = InlineKeyboardButton(text="🧑🏻‍💻 button5", callback_data="randomvalue_of50")
button6 = InlineKeyboardButton(text="📵 button6", callback_data="randomvalue_of60")
button7 = InlineKeyboardButton(text="📶 button7", callback_data="randomvalue_of70")
button8 = InlineKeyboardButton(text="🏆 button8", callback_data="randomvalue_of80")

keyboard_inline = InlineKeyboardMarkup().add(button1, button2, button3, button4, button5, button6, button7, button8)

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Quiz", "Rewards", "Wifi_report", "Puk_report","Pkg-sup", "other", "about us", "FAQ")

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply(welcome, reply_markup=keyboard1)

with open('text.txt', 'r') as file:
    welcome = file.read()

@dp.message_handler(commands=['Support'])
async def support(message: types.Message):
    await message.reply(cust_sup, reply_markup=keyboard1)

with open('cust-sup.txt', 'r') as file:
    cust_sup = file.read()

@dp.callback_query_handler(text=["randomvalue_of10", "randomvalue_of20", "randomvalue_of30", "randomvalue_of40", "randomvalue_of50", "randomvalue_of60", "randomvalue_of70", "randomvalue_of80"])
async def random_value(call: types.CallbackQuery):
    if call.data == "randomvalue_of10":
        await call.message.answer(randint(1, 10))
    if call.data == "randomvalue_of20":
        await call.message.answer(randint(1, 20))
    if call.data == "randomvalue_of30":
        await call.message.answer(randint(1, 30))
    if call.data == "randomvalue_of40":
        await call.message.answer(randint(1, 40))
    if call.data == "randomvalue_of50":
        await call.message.answer(randint(1, 50))
    if call.data == "randomvalue_of60":
        await call.message.answer(randint(1, 60))
    if call.data == "randomvalue_of70":
        await call.message.answer(randint(1, 70))
    if call.data == "randomvalue_of80":
        await call.message.answer(randint(1, 80))
        
    await call.answer()


@dp.message_handler()
async def kb_answer(message: types.Message):
    if message.text == 'Quiz':
        await message.reply("Hi! How are you?")
    elif message.text == 'Rewards':
        await message.reply("Rewards ")
    elif message.text == 'Wifi_report':
        await message.reply("wifi repoerter")
    elif message.text == 'Puk_report':
        await message.reply("puk repoerter")
    elif message.text == 'pkg-sup':
        await message.reply("sup")
    elif message.text == 'about us':
        await message.reply("wifi repoerter")
    elif message.text == 'others':
        await message.reply("puk repoerter")
    elif message.text == 'FAQ':
        await message.reply("puk repoerter")
    else:
        await message.reply(f"Your message is: {message.text}")


executor.start_polling(dp)
