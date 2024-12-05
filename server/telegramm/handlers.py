from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, state
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import server.telegramm.keyboards as kb
from server.telegramm.messages import *

router = Router()


async def get_user(db, user_id):
    async with db.execute() as cursor:
        row = await cursor.fetchone()
        return row[0] if row else None


class Login(StatesGroup):
    name = State()
    password = State()
    id_user = State()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAKWQGYwoJnQtmM453xUE46hATztgheOAAKsEwACOJ4hS9HIZVrp3vjbNAQ")
    await message.answer(START_MESSAGE_ANSWER, reply_markup=kb.main)
    # message.from_user.id


@router.message(Command("Вход"))
async def cmd_login(message: types.Message):
    await state.set_state(Login.name)
    await message.answer(ANSWER_ABOUT_LOGIN)
'''

@router.message()
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Login.password)
    await message.answer(ANSWER_ABOUT_PASSWORD)


@router.message(state=Login.password)
async def reg(message: Message, state: FSMContext):
    pass
'''