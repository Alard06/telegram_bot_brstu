from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton("Меню")
# ---- Menu ----
btnHelp = KeyboardButton("Информация")
btnRandom = KeyboardButton('Случайное число')
btnWallet = KeyboardButton('Курс валют')
btnJoke = KeyboardButton('Анекдот')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnHelp, btnJoke, btnWallet, btnRandom)


# ---- Other menu ----
btnCan = KeyboardButton("Что умеет бот?")
btnInfo = KeyboardButton("Информация о профиле")
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnCan, btnMain)
