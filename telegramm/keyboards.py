from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)

main = ReplyKeyboardMarkup(one_time_keyboard=True,
                           keyboard=[
                               [KeyboardButton(text="Вход")]
                           ], resize_keyboard=True,
                           input_field_placeholder="Выберите пункт меню...")

password = ReplyKeyboardMarkup(one_time_keyboard=True,
                               keyboard=[
                                   [KeyboardButton(text="Пароль")]
                               ], resize_keyboard=True,
                               input_field_placeholder="Выберите пункт меню...")
