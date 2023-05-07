from aiogram import executor

from loader import dp
import handlers
from utils.log import logger
from datetime import datetime

if __name__ == '__main__':
    print(datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
    logger
    executor.start_polling(dp, skip_updates=True)
