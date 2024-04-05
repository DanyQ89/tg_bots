from aiogram import Router, Dispatcher, Bot, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
import datetime
import time

# from aiogram.utils.keyboard import ReplyKeyboardBuilder
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext

import asyncio

token = '7167007472:AAEvxsCaPQWFNiDjVJiYBeARvO1vJXq3KaQ'

form_router = Router()


@form_router.message(Command('time'))
async def show_time(message: Message):
    await message.answer(time.asctime().split()[3])


@form_router.message(Command('date'))
async def show_date(message: Message):
    await message.answer(str(datetime.date.today()))


@form_router.message(Command('start'))
@form_router.message(F.text)
async def answer(message: Message):
    await message.answer(f'Я получил сообщение {message.text}')


async def main():
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
