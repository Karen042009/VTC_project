import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from googletrans import Translator

API_TOKEN = "7595042078:AAFEUfLbZl66nZV61e0GZCPVwUGtMpGKSbM"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_language = {}

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Russian → English")],
        [KeyboardButton(text="🇬🇧 English → Russian")],
        [KeyboardButton(text="🇦🇲 Armenian → English")],
        [KeyboardButton(text="🇦🇲 Armenian → Russian")],
        [KeyboardButton(text="🇬🇧 English → Armenian")],
        [KeyboardButton(text="🇷🇺 Russian → Armenian")],
    ],
    resize_keyboard=True,
)


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Ընտրեք թարգմանության ուղղությունը։", reply_markup=keyboard)


@dp.message()
async def translate_message(message: Message):
    user_id = message.from_user.id
    text = message.text

    if text in [
        "🇷🇺 Russian → English",
        "🇬🇧 English → Russian",
        "🇦🇲 Armenian → English",
        "🇦🇲 Armenian → Russian",
        "🇬🇧 English → Armenian",
        "🇷🇺 Russian → Armenian",
    ]:
        user_language[user_id] = text
        await message.answer(f"✅ Դուք ընտրեցիք {text}: Հիմա ուղարկեք տեքստը։")
        return

    if user_id not in user_language:
        await message.answer(
            "Խնդրում եմ ընտրեք լեզվի ուղղությունը։", reply_markup=keyboard
        )
        return

    direction = user_language[user_id]
    translator = Translator()

    try:
        if direction == "🇬🇧 English → Armenian":
            translated_text = translator.translate(text, src="en", dest="hy").text
        elif direction == "🇬🇧 English → Russian":
            translated_text = translator.translate(text, src="en", dest="ru").text
        elif direction == "🇦🇲 Armenian → English":
            translated_text = translator.translate(text, src="hy", dest="en").text
        elif direction == "🇦🇲 Armenian → Russian":
            translated_text = translator.translate(text, src="hy", dest="ru").text
        elif direction == "🇷🇺 Russian → English":
            translated_text = translator.translate(text, src="ru", dest="en").text
        elif direction == "🇷🇺 Russian → Armenian":
            translated_text = translator.translate(text, src="ru", dest="hy").text

        await message.answer(translated_text)
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        await message.answer("Հո դու ապուշ չես ընտրում ես մեկը գրում ես ուրիշ բան։")  #


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
