import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.utils import executor
from enum import Enum


# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and storage
bot = Bot(token="6006311344:AAFpHrQxkGXuRANJAo-MCQxJIL992DJmwRA")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Quiz states
class QuizState(Enum):
    Q1 = 1
    Q2 = 2
    Q3 = 3


# Start command handler
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Send a welcome message and instructions on how to use the bot
    """
    await bot.send_message(chat_id=message.chat.id, text='Welcome to the Multi-Task Bot!\n'
                                                     'You can use this bot for the following tasks:\n'
                                                     '- Quiz: Answer quiz questions and win rewards\n'
                                                     '- WiFi: Report WiFi problems\n'
                                                     '- PUK: Report PUK problems\n'
                                                     'Type /quiz to start the quiz, or type /help for instructions.')


# Help command handler
@dp.message_handler(commands='help')
async def cmd_help(message: types.Message):
    """
    Send instructions on how to use the bot
    """
    await bot.send_message(chat_id=message.chat.id, text='Here are the available commands:\n'
                                                     '- /quiz: Start the quiz\n'
                                                     '- /wifi: Report WiFi problems\n'
                                                     '- /puk: Report PUK problems')


# Quiz command handler
@dp.message_handler(commands='quiz')
async def cmd_quiz(message: types.Message):
    """
    Start the quiz and reward users for correct answers
    """
    # Set initial quiz state
    await bot.send_message(chat_id=message.chat.id, text='Welcome to the quiz! Answer the following questions:')
    await bot.send_message(chat_id=message.chat.id, text='What is the capital of France?')
    await QuizState.Q1.set()


# WiFi problem reporting handler
@dp.message_handler(commands='wifi')
async def cmd_wifi(message: types.Message):
    """
    Report WiFi problems
    """
    bot.send_message(chat_id=message.chat.id, text='Please Enter your WiFi Serial:')

    await bot.send_message(chat_id=message.chat.id, text='Please describe your WiFi problem:')
    # Set WiFi problem reporting state
    await FSMContext.set_state('wifi_report')


# PUK problem reporting handler
@dp.message_handler(commands='puk')
async def cmd_puk(message: types.Message):
    """
    Report PUK problems
    """
    await bot.send_message(chat_id=message.chat.id, text='Please describe your PUK problem:')
    # Set PUK problem reporting state
    await FSMContext.set_state('puk_report')


# Answer handler for quiz questions
@dp.message_handler(lambda message: message.text, state=QuizState.Q1)
async def process_quiz_q1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Process answer for Q1
        if message.text == 'Paris':
            # Correct answer
            await bot.send_message(chat_id=message.chat.id, text='Correct answer! Next question:')
            await bot.send_message(chat_id=message.chat.id, text='What is the currency of Japan?')
            data['quiz_state'] = QuizState.Q2.value  # Update quiz state to Q2
# Answer handler for quiz questions
@dp.message_handler(lambda message: message.text, state=QuizState.Q2)
async def process_quiz_q2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Process answer for Q2
        if message.text == 'Yen':
            # Correct answer
            await bot.send_message(chat_id=message.chat.id, text='Correct answer! Final question:')
            await bot.send_message(chat_id=message.chat.id, text='What is the tallest mountain in the world?')
            data['quiz_state'] = QuizState.Q3.value  # Update quiz state to Q3
        else:
            # Incorrect answer
            await bot.send_message(chat_id=message.chat.id, text='Wrong answer. Try again:')
            await bot.send_message(chat_id=message.chat.id, text='What is the currency of Japan?')


@dp.message_handler(lambda message: message.text, state=QuizState.Q3)
async def process_quiz_q3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Process answer for Q3
        if message.text == 'Mount Everest':
            # Correct answer
            await bot.send_message(chat_id=message.chat.id, text='Congratulations! You answered all questions correctly.')
            await bot.send_message(chat_id=message.chat.id, text='You have won a reward!')
        else:
            # Incorrect answer
            await bot.send_message(chat_id=message.chat.id, text='Wrong answer. Try again:')
            await bot.send_message(chat_id=message.chat.id, text='What is the tallest mountain in the world?')


# WiFi problem reporting handler
@dp.message_handler(state='wifi_report')
async def process_wifi_report(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Process WiFi problem report
        wifi_problem = message.text
        await bot.send_message(chat_id=message.chat.id, text='Thank you for reporting your WiFi problem:\n'
                                                             f'{md.quote_html(wifi_problem)}')
        # Reset state
        await state.finish()


# PUK problem reporting handler
@dp.message_handler(state='puk_report')
async def process_puk_report(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Process PUK problem report
        puk_problem = message.text
        await bot.send_message(chat_id=message.chat.id, text='Thank you for reporting your PUK problem:\n'
                                                             f'{md.quote_html(puk_problem)}')
        # Reset state
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
