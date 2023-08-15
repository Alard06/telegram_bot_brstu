import logging
import sqlite3
import datetime
from random import randint

import markup as nav
from api import parser_wallet
from api.jokes import scraper_joke

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ----- API_TOKEN -----
API_TOKEN = "5851899280:AAE8T4t_Yfpr6ENreMNNjuj3hLX-_2eOqUM"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# ======================================================

# ----- Data base -----
with sqlite3.connect('data_base.bd') as sql:
    cursor = sql.cursor()
# ======================================================

async def on_startup(_):
    print("Bot active")

# ----- Информация пользователя -----
class User:
    id = None
# ======================================================

# ----- Случайный анекдот -----
@dp.message_handler(Text(equals='Анекдот'))
async def jokes(message: types.Message) -> None:
    await message.answer(f"""<i>Анекдот: </i>
{scraper_joke.scrapping()}
                         """, parse_mode=types.ParseMode.HTML, reply_markup=inline_keyboard_jokes()
                         )
    await message.delete()

def inline_keyboard_jokes() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Случайный анекдот', callback_data='btn_joke_random')]
    ])
    return ikb


# ----- Курсы валют -----
@dp.message_handler(Text(equals='Курс валют'))
async def info(message: types.Message):
    wallets = parser_wallet.scrapping().items()
    BYN, EUR, JPY, USD = 0, 0, 0, 0
    for wallet, price in wallets:
        if wallet == 'Белорусский рубль':
            BYN = price
        elif wallet == 'Доллар США':
            USD = price
        elif wallet == 'Евро':
            EUR = price
        else: JPY = price
    time_now = datetime.datetime.now().strftime("%d.%m.%Y")
    await message.answer(f"""
<u><b>Курсы валют на {time_now}</b></u>
<i>Курс доллара:</i> <b>{USD} </b>
<i>Курс евро:</i> <b>{EUR}</b>
<i>Курс японской иены:</i> <b>{JPY}</b>
<i>Курс белорусского рубля:</i> <b>{BYN}</b>
----------------------------
*<s><i>Данные взяты с сайта </i><b>cbr.ru</b> <i>(банк России)</i></s>
""", parse_mode=types.ParseMode.HTML)
    await message.delete()
# ======================================================

# ----- Генератор рандомных чисел -----
def inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Плюс', callback_data='btn_plus'), InlineKeyboardButton('Минус',
                                                                                      callback_data='btn_minus'),
         InlineKeyboardButton('Рандом', callback_data='btn_random_number')]
    ])
    return ikb

@dp.message_handler(Text(equals='Случайное число'))
async def info(message: types.Message) -> None:
    await message.answer(f"<b>Ваше рандомное число:</b> <i> ---- </i>", parse_mode=types.ParseMode.HTML,
                         reply_markup=inline_keyboard())
    await message.delete()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('btn'))
async def keys_inline(callback: types.CallbackQuery) -> None:
    global number
    try:
        if callback.data == 'btn_plus':
            number += 1
            await callback.message.edit_text(f"<b>Ваше рандомное число:</b> <i>{number}</i>",parse_mode=types.ParseMode.HTML,
                                             reply_markup=inline_keyboard())
        elif callback.data == 'btn_minus':
            number -= 1
            await callback.message.edit_text(f"<b>Ваше рандомное число:</b> <i>{number}</i>",parse_mode=types.ParseMode.HTML,
                                             reply_markup=inline_keyboard())
        elif callback.data == 'btn_random_number':
            number = randint(0, 100)
            await callback.message.edit_text(f"<b>Ваше рандомное число:</b> <i>{number}</i>",parse_mode=types.ParseMode.HTML,
                                             reply_markup=inline_keyboard())
        elif callback.data == 'btn_joke_random':
            await callback.message.edit_text(f"""<i>Анекдот: </i>    
{scraper_joke.scrapping()}
        """, parse_mode=types.ParseMode.HTML, reply_markup=inline_keyboard_jokes())
    except:
        pass
# ======================================================

# ----- Меню -----
@dp.message_handler(Text(equals='Меню'))
async def info(message: types.Message):
    User_id = message.from_user.id
    info = cursor.execute(f"SELECT * FROM data WHERE id_user = {User_id}").fetchone()
    User.status = info[-1]
    await message.answer('Меню', reply_markup=nav.mainMenu)
    await message.delete()
# ======================================================

# ----- Информация -----
@dp.message_handler(Text(equals='Информация'))
async def info(message: types.Message):
    await message.answer("Выберите команду.", reply_markup=nav.otherMenu)
    await message.delete()

@dp.message_handler(Text(equals='Что умеет бот?'))
async def can_bot(message: types.Message):
    await message.answer("""<u><b>
- Выдаст случайный анекдот
- Скажет курс валют
- Скажет случайное число</b></u>""", reply_markup=nav.mainMenu, parse_mode=types.ParseMode.HTML)
    await message.delete()

@dp.message_handler(Text(equals='Информация о профиле'))
async def can_bot(message: types.Message):
    user_id = message.from_user.id
    user_info = cursor.execute(f"SELECT * FROM data WHERE id_user = {user_id}").fetchone()
    print(user_info)
    await message.answer(f"""
    - <i>Ваш id:</i> <b>{user_info[1]}</b>
<i>- Ваше имя:</i> <b>{message.from_user.first_name}</b>
<i>- Ваш никнейм:</i> <b>{message.from_user.username}</b>
<i>- Ваш порядковый номер в базе данных:</i> <b> {user_info[0]} </b>
<i>- Дата активация бота:</i> <b> {user_info[2]} </b>
""", reply_markup=nav.mainMenu, parse_mode=types.ParseMode.HTML)
    if user_info[-1] == 'Admin':
        users_data = cursor.execute(f"SELECT * FROM data").fetchall()
        await message.answer(f"Кто состоит в боте: ")
        for i in users_data:
            await message.answer(f"{i}")
    await message.delete()
# ======================================================

# ----- Старт бота -----
@dp.message_handler(commands=['start'])
async def send_welcome(message = types.Message):
    User_id = message.from_user.id
    cursor.execute(f"SELECT id_user FROM data WHERE id_user = '{User_id}'")
    if cursor.fetchone() is None:
        await message.answer("Добро пожаловать!")
        user_connect_data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M ")
        User_status = "User"
        values = [User_id, user_connect_data, User_status]
        print('Create_new_user ', User.id)
        cursor.execute("INSERT INTO data(id_user, joining_date, status) VALUES(?,?,?)", values)
        sql.commit()
    else:
        pass
    User.status = "User"
    await message.answer("""
    У данного бота присутствуют такие функции как:
- Выдаст случайный анекдот
- Скажет курс валют
- Скажет случайное число
Что Вас интересует?
    """, reply_markup=nav.mainMenu, parse_mode=types.ParseMode.HTML)
# ======================================================

@dp.message_handler()
async def can_bot(message: types.Message):
    print(f"User {message.from_user.id} : {message.text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
