from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup

from random import randint

from BotGPT.management.commands import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
win = randint(1, 100)

button_1 = KeyboardButton('привет')
button_2 = KeyboardButton('помоги')
button_3 = KeyboardButton('скинь дз')

markup = ReplyKeyboardMarkup()
markup.add(button_1, button_2, button_3)

win = 0
num_1 = 0
num_2 = 0


@dp.message_handler(commands='start')
async def start_bot(message: types.Message):
    await message.reply('Спасибо что начали чат со мной!')


@dp.message_handler(commands='inline')
async def stsrt_bot(message: types.Message):
    inline_btn_1 = InlineKeyboardButton('Первая кнопка', callback_data='button1')
    inline_km_1 = InlineKeyboardMarkup().add(inline_btn_1)

    await message.reply('Спасибо, что начали чат о мной!', reply_markup=inline_km_1)


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def procces_callback_button1(callbak_query: types.CallbackQuery):
    await bot.answer_callback_query(callbak_query.id)
    await bot.send_message(callbak_query.from_user.id, 'Нажата первая кнопка')


@dp.message_handler(commands='game')
async def start_bot(message: types.Message):
    global win, num_1, num_2

    win = randint(1, 100)
    num_1 = randint(1, 100)
    num_2 = randint(1, 100)

    button_game_1 = KeyboardButton(f'{num_1}')
    button_game_2 = KeyboardButton(f'{num_2}')
    button_game_3 = KeyboardButton(f'{win}')

    markup_2 = ReplyKeyboardMarkup()
    markup_2.add(button_1, button_2, button_3)

    await message.reply('Выбери какое число я загадал:', reply_markup=markup_2)


@dp.message_handler(content_types='text')
@dp.message_handler(commands='game')
async def echo_bot(message: types.Message):
    global num_1
    global num_2
    global win

    if message.text.lower() == str(win):
        await message.answer('Ураа, ты угадал!!!')
    elif message.text.lower() == str(num_1):
        await message.answer('Ошибка, попробуй ещё раз!')
    elif message.text.lower() == str(num_2):
        await message.answer('Ошибка, попробуй ещё раз!')

    if message.text.lower() == 'привет':
        await message.answer('Привет, кожаный')
    elif message.text.lower() == 'помоги':
        await message.answer('Что мне нужно сделать?')
    elif message.text.lower() == 'скинь дз':
        await message.answer('Обойдёшься')


if __name__ == '__main__':
    executor.start_polling(dp)
