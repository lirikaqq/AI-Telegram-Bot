import asyncio
import logging
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Проверка обязательных переменных
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.apiyi.com/v1")  # значение по умолчанию
MODEL = os.getenv("MODEL", "gpt-3.5-turbo")

if not BOT_TOKEN or not API_KEY:
    raise ValueError("Не заданы BOT_TOKEN или API_KEY в .env файле")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище истории сообщений
user_history = {}

# Системный промпт для форматирования ответов
SYSTEM_PROMPT = {
    "role": "system",
    "content": "Ты полезный ассистент. Отвечай на русском языке, используй форматирование Markdown: **жирный**, *курсив*, списки, заголовки, если это уместно. Будь кратким и понятным."
}

# Постоянная клавиатура (Reply)
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Очистить историю")],
        [KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Inline-кнопки (для /menu)
inline_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Очистить историю", callback_data="clear")],
    [InlineKeyboardButton(text="Помощь", callback_data="help")]
])

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я AI-ассистент. Задавай вопросы, а я помогу.\n\n"
        "Кнопки внизу экрана:\n"
        "• Очистить историю\n"
        "• Помощь",
        reply_markup=main_keyboard
    )

@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer("Выбери действие:", reply_markup=inline_menu)

@dp.message(lambda message: message.text == "Очистить историю")
async def handle_clear_button(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_history:
        del user_history[user_id]
    await message.answer("История очищена.", reply_markup=main_keyboard)

@dp.message(lambda message: message.text == "Помощь")
async def handle_help_button(message: types.Message):
    await message.answer(
        "Команды:\n"
        "/start - начало\n"
        "/clear - очистить историю\n"
        "/help - помощь\n"
        "/menu - меню (inline)",
        reply_markup=main_keyboard
    )

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "clear":
        user_id = callback.from_user.id
        if user_id in user_history:
            del user_history[user_id]
        await callback.message.answer("История очищена.", reply_markup=main_keyboard)
    elif callback.data == "help":
        await callback.message.answer(
            "Команды:\n/start - начало\n/clear - очистить историю\n/help - помощь\n/menu - меню",
            reply_markup=main_keyboard
        )
    await callback.answer()

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_msg = message.text

    if user_id not in user_history:
        user_history[user_id] = []
    user_history[user_id].append({"role": "user", "content": user_msg})
    if len(user_history[user_id]) > 10:
        user_history[user_id] = user_history[user_id][-10:]

    messages = [SYSTEM_PROMPT] + user_history[user_id]
    reply = await get_ai_response(messages)

    if reply:
        user_history[user_id].append({"role": "assistant", "content": reply})
        try:
            await message.answer(reply, parse_mode="Markdown", reply_markup=main_keyboard)
        except Exception as e:
            logging.error(f"Markdown error: {e}")
            await message.answer(reply, reply_markup=main_keyboard)
    else:
        await message.answer("Извини, не удалось получить ответ. Попробуй позже.", reply_markup=main_keyboard)

async def get_ai_response(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BASE_URL}/chat/completions", json=data, headers=headers, timeout=30) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result['choices'][0]['message']['content']
                else:
                    error_text = await resp.text()
                    logging.error(f"API HTTP Error {resp.status}: {error_text}")
                    return None
    except asyncio.TimeoutError:
        logging.error("API request timeout")
        return None
    except aiohttp.ClientConnectorError as e:
        logging.error(f"Connection error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

async def clean_old_histories():
    """Фоновая задача для очистки старых историй (заглушка)."""
    while True:
        await asyncio.sleep(3600)
        logging.info("Очистка старых историй... (пока не реализовано)")

async def main():
    asyncio.create_task(clean_old_histories())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())