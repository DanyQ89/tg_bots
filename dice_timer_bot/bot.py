import random

from aiogram import Router, Dispatcher, Bot, F, filters
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery
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


def start_inline_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='dice', callback_data='dice')
    builder.button(text='time', callback_data='time')
    builder.adjust(1)
    return builder.as_markup()


def dice_inline_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='🎲 - 6', callback_data=Dice_numbers(number=random.randint(1, 6)).pack())
    builder.button(text='🎲+🎲 - 12', callback_data=Dice_numbers(number=random.randint(1, 12)).pack())
    builder.button(text='🎲🎲🎲 - 20', callback_data=Dice_numbers(number=random.randint(1, 20)).pack())
    builder.button(text='🔙 Go back', callback_data='home')
    builder.adjust(1)
    return builder.as_markup()


def time_inline_kb():
    buider = InlineKeyboardBuilder()
    buider.button(text='⏲⏳⌛ 5 sec', callback_data=Time_seconds(seconds=5).pack())
    buider.button(text='⏲⏳⌛ 1 min', callback_data=Time_seconds(seconds=60).pack())
    buider.button(text='⏲⏳⌛ 5 min', callback_data=Time_seconds(seconds=300).pack())
    buider.button(text='🔙 Go back', callback_data='home')
    buider.adjust(1)
    return buider.as_markup()


def time_going_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='✔ Stop time', callback_data='stop_time')
    builder.adjust(1)
    return builder.as_markup()


class Dice_numbers(CallbackData, prefix='dice'):
    number: int


class Time_seconds(CallbackData, prefix='time'):
    seconds: int


class Time(StatesGroup):
    stop = State()


@router.message(Command('start'))
async def start(msg: Message):
    await msg.answer('choose game', reply_markup=start_inline_kb())


@router.callback_query(F.data == 'home')
async def start(query: CallbackQuery):
    await query.message.edit_text('choose game', reply_markup=start_inline_kb())


@router.callback_query(F.data == 'dice')
async def chase_dice(query: CallbackQuery):
    # await query.answer()
    await query.message.edit_text(text='You`ve chosen dice', reply_markup=dice_inline_kb())


@router.callback_query(Dice_numbers.filter())
async def throw_dice(query: CallbackQuery):
    # await query.answer()
    num = query.data.split(':')[1]
    await query.message.edit_text(f'Your number is {num}', reply_markup=dice_inline_kb())


@router.callback_query(F.data == 'time')
async def choose_time(query: CallbackQuery):
    await query.message.edit_text('You`ve chosen time', reply_markup=time_inline_kb())


@router.callback_query(Time_seconds.filter())
@router.callback_query(F.data == 'stop_time')
async def time_mark(query: CallbackQuery, state: FSMContext):
    print(query.data, query.message.text)
    if 'time:' in query.data:
        sec = query.data.split(':')[1]
        await query.message.edit_text(f'Timer is set on {sec} seconds', reply_markup=time_going_kb())
        await asyncio.sleep(int(sec))
        await state.set_state(Time.stop)
        try:
            data = await state.get_data()
            if data['stop']:
                await state.clear()
        except Exception:
            await query.message.edit_text(f'I`m back!', reply_markup=time_inline_kb())
    else:
        await state.update_data(stop=True)
        await query.message.edit_text('Time has stopped', reply_markup=time_inline_kb())


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
