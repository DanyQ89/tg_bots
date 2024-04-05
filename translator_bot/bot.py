import random

from aiogram import Router, Dispatcher, Bot, F, filters
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.methods import edit_message_text, edit_message_reply_markup

import datetime
import time
import asyncio
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
from translate import Translator
from string import ascii_letters

token = '7167007472:AAEvxsCaPQWFNiDjVJiYBeARvO1vJXq3KaQ'
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

router = Router()
tr_to_ru = Translator(to_lang='ru', from_lang='en')
tr_to_eng = Translator(to_lang='en', from_lang='ru')



@router.message(F.text)
async def start(msg: Message):
    if msg.text[0] in ascii_letters:
        print(1)
        text = tr_to_ru.translate(msg.text)
    else:
        print(2)
        text = tr_to_eng.translate(msg.text)
    await msg.answer(text)


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
