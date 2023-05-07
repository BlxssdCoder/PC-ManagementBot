from aiogram import types

kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
screenshot = types.KeyboardButton(text='Скриншот')
mouse_action = types.KeyboardButton(text='Управление мышкой')
files_process = types.KeyboardButton(
    text='Файлы и процессы')
internal_management = types.KeyboardButton(
    'Внутреннее управление')
status_pc = types.KeyboardButton('Состояние компьютера')
kb.add(screenshot, mouse_action, files_process, internal_management, status_pc)

action_mouse_kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
up = types.KeyboardButton(text='⬆️')
down = types.KeyboardButton(text='⬇️')
left = types.KeyboardButton(text='⬅️')
right = types.KeyboardButton(text='➡️')
click = types.KeyboardButton(text='Click')
exit = types.KeyboardButton(text='Выйти из режима')
action_mouse_kb.add(up, down, left, right, click, exit)

process_files = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kill = types.KeyboardButton('Завершить процесс')
start_process = types.KeyboardButton('Запустить процесс')
download_file = types.KeyboardButton('Скачать файл')
exit = types.KeyboardButton(text='Выйти из режима')
process_files.add(kill, start_process, download_file, exit)

internal_management_computer = types.ReplyKeyboardMarkup(
    row_width=2, resize_keyboard=True)
cmd = types.KeyboardButton('Управление Shell')
shotdown = types.KeyboardButton('Выключить компьютер')
reload = types.KeyboardButton('Перезапустить компьютер')
exit = types.KeyboardButton(text='Выйти из режима')
internal_management_computer.add(cmd, shotdown, reload, exit)

go_to_back = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
exit = types.KeyboardButton(text='Выйти из режима')
go_to_back.add(exit)
