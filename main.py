import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode
from aiogram.utils import markdown
from aiogram.utils import executor

bot = Bot(token='6006311344:AAFpHrQxkGXuRANJAo-MCQxJIL992DJmwRA')  # Replace with your actual bot token

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Quiz question and answer dictionary
quiz_data = {
    'What is the capital of France?': 'Paris',
    'What is the largest mammal?': 'Blue whale',
    'What is the boiling point of water in Celsius?': '100',
    'What is the currency of Japan?': 'Yen',
    'What is the tallest mountain in the world?': 'Mount Everest'
}

# User's reward coins dictionary
reward_coins = {}

# Quiz command handler
@dp.message_handler(Command('quiz'))
async def cmd_quiz(message: types.Message):
    quiz_question = random.choice(list(quiz_data.keys()))
    correct_answer = quiz_data[quiz_question]

    # Store the correct answer in FSM context
    async with FSMContext(storage=storage, chat=message.chat, user=message.from_user) as quiz_context:
        quiz_context['correct_answer'] = correct_answer

        # Prompt the quiz question
        await bot.send_message(chat_id=message.chat.id, text=f'Quiz Question:\n\n{quiz_question}')
        await bot.register_next_step_handler(message, process_quiz_answer)

async def process_quiz_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as quiz_data:
        correct_answer = quiz_data['correct_answer']
        user_answer = message.text

        # Check if the answer is correct
        if user_answer == correct_answer:
            # Award 1 coin for correct answer
            await bot.send_message(chat_id=message.chat.id, text='Correct! You earned 1 coin.')
            user_id = message.from_user.id
            if user_id not in reward_coins:
                reward_coins[user_id] = 0
            reward_coins[user_id] += 1
        else:
            await bot.send_message(chat_id=message.chat.id, text='Wrong! Better luck next time.')

    # Reset the FSM state
    await state.finish()

# WiFi report command handler
@dp.message_handler(Command('wifi_report'))
async def cmd_wifi_report(message: types.Message):
    # Prompt for serial number
    await bot.send_message(chat_id=message.chat.id, text='Please enter the serial number:')
    await bot.register_next_step_handler(message, process_wifi_serial_number)

async def process_wifi_serial_number(message: types.Message):
    serial_number = message.text

    # Prompt for description
    await bot.send_message(chat_id=message.chat.id, text='Please enter the description of the Wi-Fi issue:')
    await bot.register_next_step_handler(message, process_wifi_description, serial_number)

async def process_wifi_description(message: types.Message, state: FSMContext):
    serial_number = state['serial_number']
    description = message.text

    await bot.send_message(chat_id=message.chat.id, text='Thank you for reporting the Wi-Fi issue. We will look into it.')

    await state.finish()

# PUK report command handler
@dp.message_handler(Command('puk_report'))
async def cmd_puk_report(message: types.Message):
    # Prompt for SIM card number
    await bot.send_message(chat_id=message.chat.id, text='Please enter the Phone number:')
    await bot.register_next_step_handler(message, process_puk_sim_number)

async def process_puk_sim_number(message: types.Message):
    sim_number = message.text

    # Prompt for description
    await bot.send_message(chat_id=message.chat.id, text='Please enter the description of the PUK issue:')
    await bot.register_next_step_handler(message, process_puk_description, sim_number)

async def process_puk_description(message: types.Message, state: FSMContext):
    sim_number = state['sim_number']
    description = message.text

    await bot.send_message(chat_id=message.chat.id, text='Thank you for reporting the PUK issue. We will look into it.')

    await state.finish()

# Start command handler
@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Check if user is already registered
    user_id = message.from_user.id
    if user_id in reward_coins:
        await bot.send_message(chat_id=message.chat.id, text='Welcome back! You have earned {} coins.'.format(reward_coins[user_id]))
    else:
        await bot.send_message(chat_id=message.chat.id, text='Welcome! You have not earned any coins yet.')

# Help command handler
@dp.message_handler(Command('help'))
async def cmd_help(message: types.Message):
    """
    Show help message
    """
    help_text = "You can control me by sending these commands:\n\n" \
                "/start - Start the bot and check your coins\n" \
                "/quiz - Participate in a quiz and earn coins\n" \
                "/wifi_report - Report Wi-Fi issue and earn coins\n" \
                "/puk_report - Report PUK issue and earn coins\n" \
                "/help - Show this help message"

    await bot.send_message(chat_id=message.chat.id, text=help_text, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Start the bot
    executor.start_polling(dp, skip_updates=True)
