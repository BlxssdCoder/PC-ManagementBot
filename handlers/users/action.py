import os
import platform
import subprocess

import mouse
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import (action_mouse_kb, go_to_back,
                               internal_management_computer, kb, process_files)
from loader import dp
from state.files_process_state import FilesProcessState
from state.internal_management import ManagementState
from state.mouse_state import MouseState
from config import mouse_swipe

from .functions import get_screenshot


class User:
    def __init__(self):
        keys = ['urldown', 'fin', 'curs']

        for key in keys:
            self.key = None


User.curs = mouse_swipe


@dp.message_handler(state=MouseState.action, content_types=['text'])
async def cmd_action_mouse(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == '⬆️':
            currentMouseX,  currentMouseY = mouse.get_position()
            mouse.move(currentMouseX,  currentMouseY - User.curs)
            await get_screenshot()
            await message.answer_photo(open("screen_with_mouse.png", "rb"),
                                       reply_markup=action_mouse_kb)
            os.remove("screen.png")
            os.remove("screen_with_mouse.png")
        elif message.text == '⬇️':
            currentMouseX,  currentMouseY = mouse.get_position()
            mouse.move(currentMouseX,  currentMouseY + User.curs)
            await get_screenshot()
            await message.answer_photo(open("screen_with_mouse.png", "rb"),
                                       reply_markup=action_mouse_kb)
            os.remove("screen.png")
            os.remove("screen_with_mouse.png")
        elif message.text == '⬅️':
            currentMouseX,  currentMouseY = mouse.get_position()
            mouse.move(currentMouseX - User.curs,  currentMouseY)
            await get_screenshot()
            await message.answer_photo(open("screen_with_mouse.png", "rb"),
                                       reply_markup=action_mouse_kb)
            os.remove("screen.png")
            os.remove("screen_with_mouse.png")
        elif message.text == '➡️':
            currentMouseX,  currentMouseY = mouse.get_position()
            mouse.move(currentMouseX + User.curs,  currentMouseY)
            await get_screenshot()
            await message.answer_photo(open("screen_with_mouse.png", "rb"),
                                       reply_markup=action_mouse_kb)
            os.remove("screen.png")
            os.remove("screen_with_mouse.png")
        elif message.text == 'Click':
            mouse.click()
            await get_screenshot()
            await message.answer_photo(open("screen_with_mouse.png", "rb"),
                                       reply_markup=action_mouse_kb)
            os.remove("screen.png")
            os.remove("screen_with_mouse.png")
        elif message.text == 'Выйти из режима':
            await state.finish()
            await message.answer('Вы вышли из управления компьютера',
                                 reply_markup=kb)


@dp.message_handler(state=FilesProcessState.action, content_types=['text'])
async def cmd_action_file(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Выйти из режима':
            await state.finish()
            await message.answer('Вы вышли из управления процессами и файлами.',
                                 reply_markup=kb)
        elif message.text == 'Завершить процесс':
            await message.answer('Укажите название процесса')
            await FilesProcessState.kill.set()
        elif message.text == 'Запустить процесс':
            await message.answer('Укажите путь до файла\n\n'
                                 'Пример: C:/Users/your_name/Desktop/file_name.mp3')
            await FilesProcessState.start_process.set()
        elif message.text == 'Скачать файл':
            await message.answer('Укажите путь до файла\n\n'
                                 'Пример: C:/Users/your_name/Desktop/file_name.mp3')
            await FilesProcessState.download_file.set()


@dp.message_handler(state=FilesProcessState.kill, content_types=['text'])
async def cmd_action_file_kill(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            os.system("taskkill /IM " + message.text + " -F")
            await message.answer(f'Процесс \"{message.text}\" выключен.',
                                 reply_markup=process_files)
            await state.finish()
            await FilesProcessState.action.set()
        except:
            await state.finish()
            await FilesProcessState.action.set()
            await message.answer('Процесс с таким названием не найден',
                                 reply_markup=process_files)


@dp.message_handler(state=FilesProcessState.start_process, content_types=['text'])
async def cmd_action_file_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            os.startfile(r'' + message.text)
            await message.answer(f"Файл по пути \"{message.text}\" запустился",
                                 reply_markup=process_files)
            await get_screenshot()
            await message.answer_photo(open("screen_with_mouse.png", "rb"),
                                       reply_markup=action_mouse_kb)
            os.remove("screen.png")
            os.remove("screen_with_mouse.png")
            await state.finish()
            await FilesProcessState.action.set()
        except:
            await message.answer(f"Указан неверный файл.",
                                 reply_markup=process_files)
            await state.finish()
            await FilesProcessState.action.set()


@dp.message_handler(state=FilesProcessState.download_file, content_types=['text'])
async def cmd_action_file_download(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            file_path = message.text
            if os.path.exists(file_path):
                await message.answer('Загружаю файл...')
                file_doc = open(file_path, 'rb')
                await message.answer_document(file_doc)
                await state.finish()
                await FilesProcessState.action.set()
            else:
                await message.answer('Файл не найден или указан неверный путь')
                await state.finish()
                await FilesProcessState.action.set()
        except:
            await message.answer('Файл не найден или указан неверный путь')
            await state.finish()
            await FilesProcessState.action.set()


@dp.message_handler(state=ManagementState.action, content_types=['text'])
async def cmd_action_file_kill(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Управление Shell':
            await message.answer('Введите команду:',
                                 reply_markup=go_to_back)
            await ManagementState.cmd.set()
        elif message.text == 'Выключить компьютер':
            await message.answer('Выключение компьютера',
                                 reply_markup=internal_management_computer)
            os.system('shutdown -s /t 0 /f')
        elif message.text == 'Перезапустить компьютер':
            await message.answer('Перезапускаю компьютер')
            os.system('shutdown -r /t 0 /f')
        elif message.text == 'Выйти из режима':
            await state.finish()
            await message.answer('Вы вышли из режима внутреннего управления',
                                 reply_markup=kb)


@dp.message_handler(state=ManagementState.cmd, content_types=['text'])
async def cmd_action_file_kill(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Выйти из режима':
            await message.answer('Вы вышли из управления Shell',
                                 reply_markup=internal_management_computer)
            await state.finish()
            await ManagementState.action.set()
        try:
            result = subprocess.check_output(message.text, shell=True)
            await message.answer(result.decode('utf-8'),
                                 reply_markup=go_to_back)
        except:
            await message.answer('Неизвестная команда',
                                 reply_markup=go_to_back)
