
# 🤖 AI Telegram Bot — ассистент на базе ChatGPT

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-blue)](https://docs.aiogram.dev/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Telegram-бот, который общается с пользователями с помощью нейросети (ChatGPT). Поддерживает контекст беседы, команды для управления историей, удобные кнопки и красивое форматирование ответов.

## ✨ Возможности

- Ответы на любые вопросы через ChatGPT (GPT-3.5/GPT-4).
- Поддержка контекста – бот помнит последние 10 сообщений в рамках диалога.
- Команды:
  - `/start` – приветствие и показ клавиатуры.
  - `/menu` – инлайн‑кнопки для управления.
  - `/clear` – очистка истории (также через кнопку "Очистить историю").
  - `/help` – список команд.
- Удобная клавиатура внизу экрана (Reply‑кнопки).
- Красивое форматирование ответов (Markdown).
- Обработка ошибок и таймаутов API.
- Сохранение истории в памяти (для каждого пользователя отдельно).

## 🛠 Технологии

- **Python 3.11**
- **aiogram** – асинхронный фреймворк для Telegram API
- **aiohttp** – асинхронные HTTP-запросы
- **CometAPI / APIYI** – прокси-сервисы для доступа к OpenAI из РФ
- **python-dotenv** – для безопасного хранения токенов

## 🚀 Установка и запуск

### 1. Клонируй репозиторий
```bash
git clone https://github.com/lirikaqq/ai-telegram-bot.git
cd ai-telegram-bot

2. Установи зависимости
Рекомендуется использовать виртуальное окружение:

bash
python -m venv venv
source venv/bin/activate      # для Linux/macOS
venv\Scripts\activate         # для Windows
pip install -r requirements.txt

3. Получи токены
Telegram Bot Token: создай бота у @BotFather и скопируй токен.

API ключ: зарегистрируйся на CometAPI или APIYI (для пользователей РФ) и получи ключ доступа к ChatGPT.

4. Настрой переменные окружения
Скопируй файл-пример и отредактируй:

bash
cp examples/.env.example .env

Открой .env и вставь свои токены:
BOT_TOKEN=твой_токен_бота
API_KEY=твой_ключ_от_api
BASE_URL=https://api.apiyi.com/v1
MODEL=gpt-3.5-turbo

5. Запусти бота
bash
python bot.py

Бот запустится и начнёт отвечать на сообщения.

📁 Структура проекта
text
ai-telegram-bot/
│
├── bot.py                 # основной код бота
├── requirements.txt       # зависимости
├── .gitignore             # игнорируемые файлы
├── LICENSE                # лицензия MIT
├── README.md              # этот файл
│
├── examples/
│   └── .env.example       # пример файла с переменными

🤝 Контакты
Автор: Артём Лола

GitHub: @lirikaqq

Email: lola.artem7@mail.ru

📄 Лицензия
Проект распространяется под лицензией MIT. Подробнее – в файле LICENSE.
