import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN, TOKEN_OPENAI

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
openai.api_key = TOKEN_OPENAI

dialog = []


@dp.message_handler()
async def handle_message(message: types.Message):
    global dialog
    user_input = message.text

    dialog.append({'role': 'system', 'content': user_input})

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant'},
            *dialog
        ]
    )

    answer = response.choices[0].message.content

    dialog.append({'role': 'assistant', 'content': answer})

    await message.reply(answer)


if __name__ == '__main__':
    executor.start_polling(dp)
