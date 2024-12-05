import requests
from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import telegramm.keyboards as kb
from telegramm.settings import API_URL
from telegramm.messages import *

router = Router()


class Login(StatesGroup):
    name = State()
    password = State()
    id_user = State()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAKWQGYwoJnQtmM453xUE46hATztgheOAAKsEwACOJ4hS9HIZVrp3vjbNAQ")
    await message.answer(START_MESSAGE_ANSWER, reply_markup=kb.main)


@router.message(F.text == "Вход")
async def login(message: types.Message, state: FSMContext):
    await message.answer(ANSWER_ABOUT_LOGIN)
    await state.set_state(Login.name)


@router.message(Login.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Login.password)
    await message.answer(ANSWER_ABOUT_PASSWORD)


@router.message(Login.password)
async def reg_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    nickname_check = data.get('name')
    password_check = data.get('password')
    try:
        password_ = requests.post(f'{API_URL}/password', json={'password': password_check}).json()
        response = requests.get(f'{API_URL}/data/users').json()

    except Exception as e:
        print(e)
    password_ = password_.get('password')

    for i in response:
        if i.get('nickname') == nickname_check and i.get('password') == password_:
            response = requests.put(f'{API_URL}/data/users/{nickname_check}',
                                    json={'telegram': str(message.from_user.id)})
            if response.status_code == 200:
                await message.answer('Вы успешно привязали аккаунт')
            else:
                await message.answer('Ошибка на стороне сервера, попробуйте позже')
            return

    else:
        await message.answer('Неверный логин или пароль', reply_markup=kb.main)
        print('Неверный пароль')
        return
