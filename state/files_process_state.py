from aiogram.dispatcher.filters.state import State, StatesGroup


class FilesProcessState(StatesGroup):
    action = State()
    kill = State()
    start_process = State()
    download_file = State()
    upload_file = State()
