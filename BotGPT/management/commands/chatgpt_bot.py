import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from .config import TOKEN, TOKEN_OPENAI

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.conf import settings

from BotGPT.models import Dialog, Message

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
openai.api_key = TOKEN_OPENAI

dialog = []

class Command(BaseCommand):
    help = 'Telegram bot setup command'

    def handle(selfself, *args, **options):
        sync_to_async(executor.start_polling(dp))

@sync_to_async
def save_user_message(dialog, user_input):
    role_user = 'user'
    dialog_obj, _ = Dialog.objects.get_or_create(username=f'{dialog}', role=role_user)
    user_message = Message(dialog=dialog_obj, role=role_user, content=user_input)
    user_message.save()


@sync_to_async
def save_assistant_message(dialog, answer):
    role_assistant = 'assistant'
    dialog_obj, _ = Dialog.objects.get_or_create(username=f'{dialog}', role=role_assistant)
    assistant_message = Message(dialog=dialog_obj, role=role_assistant, content=answer)
    assistant_message.save()


@dp.message_handler(commands=['delete_dialog'])
async def delete_dialog(message: types.Message):
    dialog_str = f'{message.from_user.username}'

    dialogs = await sync_to_async(Dialog.objects.filter)(username=dialog_str)

    for dialog in dialogs:
        await sync_to_async(dialog.delete)()

    messages = await sync_to_async(Message.objects.filter)(dialog__username=dialog_str)

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
@dp.message_handler()
async def handle_message(message: types.Message)
    if message.text == '/delete_dialog'
        await delete_dialog(message)

    user_input = message.text

    dialog_str = f'{message.from_user.username}'

    await save_user_message(dialog_str, user_input)

    dialog_objs = await sync_to_async(Dialog.objects.filter)(username=f'{dialog_str}')
    previous_messages = await sync_to_async(Message.objects.filter)(dialog__in=dialog_objs)

    messages = await sync_to_async(
        lambda: [
                    {'role': 'system', 'content': 'You are a helpful assistant'}
                ] + [
                    {'role': message.role, 'content': message.content}
                    for message in previous_messages
                ] + [
                    {'role': 'user', 'content': user_input}
                ]
    )()

    response = await sync_to_async(openai.ChatCompletion.create)(
        model='gpt-3.5-turbo-0301',
        messages=messages
    )

    answer = response.choices[0].message.content

    dialog.append({'role': 'assistant', 'content': answer})

    await message.reply(answer)


if __name__ == '__main__':
    executor.start_polling(dp)
