import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor

API_TOKEN = "8607291936:AAFlYBgzLwzBtsERNScwR5rZb4cHAmnEbUk"
ADMIN_ID = 5963914350

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- КНОПКИ ---
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add("📚 Уровень", "ℹ️ О занятиях")
main_kb.add("📝 Записаться")

levels_kb = ReplyKeyboardMarkup(resize_keyboard=True)
levels_kb.add("A1", "A2", "B1", "B2", "C1")
levels_kb.add("Назад")

# --- ХРАНЕНИЕ ДАННЫХ ---
user_data = {}

# --- СТАРТ ---
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот репетитора по немецкому 🇩🇪\n\n"
        "Выбери, что тебя интересует:",
        reply_markup=main_kb
    )

# --- УРОВЕНЬ ---
@dp.message_handler(lambda message: message.text == "📚 Уровень")
async def choose_level(message: types.Message):
    await message.answer("Выбери свой уровень:", reply_markup=levels_kb)

@dp.message_handler(lambda message: message.text in ["A1","A2","B1","B2","C1"])
async def level_selected(message: types.Message):
    user_data[message.from_user.id] = {"level": message.text}
    await message.answer(f"Отлично! Твой уровень: {message.text}")

# --- О ЗАНЯТИЯХ ---
@dp.message_handler(lambda message: message.text == "ℹ️ О занятиях")
async def about(message: types.Message):
    await message.answer(
        "📖 О занятиях:\n\n"
        "— Индивидуальные уроки\n"
        "— Подбор программы под цель\n"
        "— Разговорная практика\n"
        "— Подготовка к экзаменам\n\n"
        "Напиши 'Записаться', чтобы попасть на пробное занятие"
    )

# --- ЗАПИСЬ ---
@dp.message_handler(lambda message: message.text == "📝 Записаться")
async def signup_start(message: types.Message):
    user_data[message.from_user.id] = {}
    await message.answer("Хочешь пробное занятие? Напиши 'Да'")

@dp.message_handler(lambda message: message.text.lower() == "да")
async def ask_level(message: types.Message):
    user_data[message.from_user.id]["trial"] = "Да"
    await message.answer("Какой у тебя уровень? (A1-C1)")

@dp.message_handler(lambda message: message.text in ["A1","A2","B1","B2","C1"])
async def ask_time(message: types.Message):
    user_data[message.from_user.id]["level"] = message.text
    await message.answer("Когда тебе удобно заниматься?")

@dp.message_handler(lambda message: "level" in user_data.get(message.from_user.id, {}))
async def ask_experience(message: types.Message):
    if "time" not in user_data[message.from_user.id]:
        user_data[message.from_user.id]["time"] = message.text
        await message.answer("Расскажи немного о своём опыте изучения немецкого:")
    else:
        user_data[message.from_user.id]["experience"] = message.text

        data = user_data[message.from_user.id]

        text = (
            f"📥 Новая заявка:\n\n"
            f"👤 @{message.from_user.username}\n"
            f"📊 Уровень: {data.get('level')}\n"
            f"⏰ Время: {data.get('time')}\n"
            f"📚 Опыт: {data.get('experience')}\n"
        )

        await bot.send_message(ADMIN_ID, text)

        await message.answer("Спасибо! Я свяжусь с тобой 😊")

# --- НАЗАД ---
@dp.message_handler(lambda message: message.text == "Назад")
async def back(message: types.Message):
    await message.answer("Главное меню", reply_markup=main_kb)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
