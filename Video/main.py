import subprocess
from aiogram import *
import cv2
import pymysql
import time
import glob
import os
import aiogram.utils.markdown as md
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ContentType
from aiogram.utils import executor
import asyncio
import sqlite3
import requests
import subprocess
import re

def Vremya():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


# def Updater():
#     if Vremya() == "23:59:00":
#         time.sleep(1)
#         os.startfile('facetrain.exe')

API_TOKEN = '5876734711:AAEuAXxnxjF31z-_bPZAxNRrOaOzfdOjb6M'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
URL = 'https://api.telegram.org/bot'

conn = sqlite3.connect(u"D:\Python\AccessEbal0\AccessEbal0Obuchaemaya\FaceBase.db")
c = conn.cursor()

def send_message(chat_id, text):
    requests.get(f'{URL}{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
@dp.message_handler(commands=["protect"])
async def echo(message: types.Message):

    cam_address = message.text
    print(cam_address)
    p = re.compile('(\s*)/protect(\s*)')
    a2 = p.sub(' ', cam_address)
    print(a2)

    cmd = f'python D:\Python\AccessEbal0\Docker\Video\Vision.py {a2}'

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

class Form(StatesGroup):
    name = State()
    id = State()
    photo = State()


@dp.message_handler(commands='AddNewUser')
async def cmd_start(message: types.Message):

    # Set state
    await Form.name.set()

    await message.reply("Введите Name:")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Введите ID:")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.id)
async def process_id(message: types.Message, state: FSMContext):
    await state.update_data(id=int(message.text))
    await Form.next()
    await message.reply("Жду фото:")


@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.id)
async def process_id_invalid(message: types.Message):
    return await message.reply("ID должно быть числом")

flag_group_id = None

async def anything(msg: types.Message,state: FSMContext):
    global flag_group_id
    photos = msg.photo
    data = await state.get_data()
    #await photos[-1].download(destination_dir="DataSet/user." + str(data['id']) + '.' + '{0}' + ".jpg")
    await photos[-1].download(destination_dir='photos')
    if msg.media_group_id and not flag_group_id:
        flag_group_id = msg.media_group_id
        await msg.answer('Получаю вложения')
        await asyncio.sleep(0.5)
        data = await state.get_data()
        await msg.answer(f"Имя: {data['name']}\n"
                             f"ID: {data['id']}")
        print({data['name']},{data['id']})
        c.execute(f"INSERT INTO 'People' VALUES ('{data['id']}','{data['name']}')")
        conn.commit()
        list_of_photos = glob.glob(
            'D:\Python\AccessEbal0\Docker\Video\photos\photos\*')
        counter = 0
        for h in list_of_photos:
            counter += 1
            os.rename(f'{h}',"DataSet/user." + str(data['id']) + '.' + f'{counter}' + ".jpg")
        await state.finish()
    else:
        if not msg.media_group_id:
            flag_group_id = None
            await msg.answer(msg.text or msg.caption or 'Нет сообщения')
dp.register_message_handler(anything, content_types=['photo'],state=Form.photo)

@dp.message_handler(commands=["info","help"])
async def echo(message: types.Message):
    await message.answer('Для добавления нового пользователя - /AddNewUser\n'
                         'Выход - /cancel\n'
                         'Запуск программы распознавания - /protect\n'
                         'Просмотр пользователей - /SeePeople'
                         )

@dp.message_handler(commands=["SeePeople"])
async def echo(message: types.Message):
    c.execute(f"SELECT * FROM People ")
    val = c.fetchall()
    markup3 = ReplyKeyboardMarkup()
    for j in val:
        markup3.add(KeyboardButton(j[1]))
        print(markup3)
    await message.reply("Люди в базе:", reply_markup=markup3)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
