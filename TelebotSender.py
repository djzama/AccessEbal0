from aiogram import *
import os
import time

API_TOKEN = '5876734711:AAEuAXxnxjF31z-_bPZAxNRrOaOzfdOjb6M'


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["protect"])
async def echo(message: types.Message):
    print("Вошли")
    while True:
        try:

            break  
        except IOError:
            print("Сработало")
            await message.answer("")






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
