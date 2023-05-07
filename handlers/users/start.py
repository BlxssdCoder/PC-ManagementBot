from aiogram import types

from config import allowed_id
from keyboards.default import kb
from loader import dp


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if message.chat.id not in allowed_id:
        await message.answer('У вас недостаточно прав!')
    else:
        await message.answer('Дистанционное управление PC',
                             reply_markup=kb)
