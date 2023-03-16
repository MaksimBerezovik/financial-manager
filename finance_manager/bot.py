from aiogram import executor
from dispatcher import dp
import personal_actions

from db import BotDB
BotDB = BotDB('DB_FM/account.db')

#run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)