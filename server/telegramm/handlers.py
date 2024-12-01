from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, state
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import server.telegramm.keyboards as kb
from server.telegramm.messages import *

router = Router()


class Register(StatesGroup):
    name = State()
    password = State()
    id_user = State()
    phone_user = State()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAKWQGYwoJnQtmM453xUE46hATztgheOAAKsEwACOJ4hS9HIZVrp3vjbNAQ")
    await message.answer(START_MESSAGE_ANSWER, reply_markup=kb.main)


@router.message(Command("Вход"))
async def cmd_start(message: types.Message):
    await state.set_state(Register.name)
    await message.answer(ANSWER_ABOUT_LOGIN)


@router.message(Register.name)
async def reg_name(messange: Message, state: FSMContext):
    await state.update_data(name=messange.text)
    await state.set_state(Register.password)
    await messange.answer(ANSWER_ABOUT_PASSWORD)


@router.message(Register.password)
async def reg_age(messange: Message, state: FSMContext):
    pass
