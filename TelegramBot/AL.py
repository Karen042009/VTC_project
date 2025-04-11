import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from pprint import pprint
import re
from mistralai import Mistral


api_key = "Vn9jeBwiumcmFsnE0zd8YVM6HT1GXgVa"
model = "mistral-small-latest"
client = Mistral(api_key=api_key)
logging.basicConfig(level=logging.INFO)
bot = Bot(token="7814164870:AAE_JsC6cD03rSSdfu4aSB2XVZZcIHttodU")
dp = Dispatcher()


@dp.message(Command("/start"))
async def cmd_start(message: types.Message):
    start_text = "Welcome to user"
    await bot.send_message(message.chat.id, start_text)


@dp.message()
async def message_handler(msg: Message):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "your bane is KarenAL",
            },
            {
                "role": "user",
                "content": msg.text,
            },
        ],
    )
    await bot.send_message(
        msg.chat.id, chat_response.choices[0].message.content, parse_mode="Markdown"
    )


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


asyncio.run(main())
