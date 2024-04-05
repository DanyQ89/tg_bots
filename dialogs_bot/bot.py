import random

from aiogram import Router, Dispatcher, Bot, F, filters
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.methods import edit_message_text, edit_message_reply_markup

import datetime
import time
import asyncio
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio

token = '7167007472:AAEvxsCaPQWFNiDjVJiYBeARvO1vJXq3KaQ'
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

router = Router()


class Ans(StatesGroup):
    city = State()
    weather = State()


@router.message(Command('start'))
async def start(msg: Message, state: FSMContext):
    await msg.answer(f'Пройдите опрос\nвы можете прервать его командой /stop\nили пропустить вопрос командой /skip',
                     reply_markup=ReplyKeyboardRemove())
    await msg.answer('Введите свой город')
    await state.set_state(Ans.city)


@router.message(Ans.city)
async def city(msg: Message, state: FSMContext):
    await state.update_data(city=msg.text)
    if msg.text != '/skip':
        await msg.answer(f'Какая погода сейчас в городе {msg.text}?')
    else:
        await msg.answer('Какая у вас сейчас погода?')
    await state.set_state(Ans.weather)


@router.message(Ans.weather)
@router.message(Command('stop'))
async def city(msg: Message, state: FSMContext):
    await state.update_data(weather=msg.text)
    data = await state.get_data()
    await state.clear()
    print(data)
    await msg.answer('Спасибо за опрос')


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
