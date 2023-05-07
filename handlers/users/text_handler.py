import os
import socket
from datetime import datetime

import cpuinfo
import psutil
from aiogram import types

from config import allowed_id
from keyboards.default import (action_mouse_kb, internal_management_computer,
                               kb, process_files)
from loader import dp
from state.files_process_state import FilesProcessState
from state.internal_management import ManagementState
from state.mouse_state import MouseState

from .functions import get_screenshot

date_now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
info = cpuinfo.get_cpu_info()



@dp.message_handler(content_types=['text'])
async def text_handlers(message: types.Message):
    if message.chat.id not in allowed_id:
        await message.answer('У вас недостаточно прав!')
    else:
        if message.text == 'Скриншот':
            if message.chat.id not in allowed_id:
                await message.answer('У вас недостаточно прав!')
            else:
                await get_screenshot()
                await message.answer_photo(open("screen_with_mouse.png", "rb"),
                                        f'<b>Время скриншота</b>: <code>{date_now}</code>',
                                        parse_mode='html',
                                        reply_markup=kb)
                os.remove("screen.png")
                os.remove("screen_with_mouse.png")
        elif message.text == 'Управление мышкой':
            if message.chat.id not in allowed_id:
                await message.answer('У вас недостаточно прав!')
            else:
                await message.answer('Вы перешли в режим управления компьютером.',
                                    reply_markup=action_mouse_kb)
                await MouseState.action.set()
        elif message.text == 'Выйти из режима':
            if message.chat.id not in allowed_id:
                await message.answer('У вас недостаточно прав!')
            else:
                await message.answer('Вы перенесены в меню',
                                    reply_markup=kb)
        elif message.text == 'Файлы и процессы':
            if message.chat.id not in allowed_id:
                await message.answer('У вас недостаточно прав!')
            else:
                await message.answer('Вы перешли в режим управления процессами и файлами',
                                    reply_markup=process_files)
                await FilesProcessState.action.set()
        elif message.text == 'Внутреннее управление':
            if message.chat.id not in allowed_id:
                await message.answer('У вас недостаточно прав!')
            else:
                await message.answer('Вы перешли в режим внутреннего управления.',
                                    reply_markup=internal_management_computer)
                await ManagementState.action.set()
        elif message.text == 'Состояние компьютера':
            if message.chat.id not in allowed_id:
                await message.answer('У вас недостаточно прав!')
            else:
                load = psutil.cpu_percent()
                disks = psutil.disk_partitions()
                mem = psutil.virtual_memory()
                file_system = ''
                total_size = ''
                used = ''
                free = ''
                cpu_name = info['brand_raw']
                count_streams = info['count']
                base_frequency = info['hz_actual_friendly']
                total_memory = "{:.2f} GB".format(mem.total / (1024**3))
                available_memory = "{:.2f} GB".format(mem.available / (1024**3))
                used_memory = "{:.2f} GB".format(mem.used / (1024**3))
                memory_load = "{:.2f} %".format(mem.percent)
                hostname = socket.gethostname()
                try:
                    for disk in disks:
                        file_system += "{}".format(disk.fstype)
                        total_size += "{:.2f} GB".format(
                            psutil.disk_usage(disk.mountpoint).total / (1024 ** 3))
                        used += "{:.2f} GB".format(
                            psutil.disk_usage(disk.mountpoint).used / (1024 ** 3))
                        free += "{:.2f} GB".format(
                            psutil.disk_usage(disk.mountpoint).free / (1024 ** 3))
                except:
                    ...
                text = f"""
<b>Информация о компьютере {hostname}</b>

<b>CPU {cpu_name}</b>

<b>Загруженность:</b> <code>{load} %</code>
<b>Количество потоков:</b> <code>{count_streams}</code>
<b>Базовая частота:</b> <code>{base_frequency}</code>

<b>Диск</b>

<b>Файловая система:</b> <code>{file_system}</code>
<b>Размер:</b> <code>{total_size}</code>
<b>Использовано:</b> <code>{used}</code>
<b>Свободно:</b> <code>{free}</code>

<b>Оперативная память</b>

<b>Общая память:</b> <code>{total_memory}</code>
<b>Доступно памяти:</b> <code>{available_memory}</code>
<b>Используется памяти:</b> <code>{used_memory}</code>
<b>Загруженность:</b> <code>{memory_load}</code> 
        """
                await message.answer(text, parse_mode='html', reply_markup=kb)