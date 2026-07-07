# Behavior Compass

Telegram-бот для проведения тестирования поведенческого стиля по 4-цветовой модели (Blue / Green / Yellow / Red).

## Возможности

- ✅ Многоязычность: Русский, O'zbekcha, English, Deutsch, Türkçe
- ✅ Полная регистрация через Telegram (имя + телефон)
- ✅ Оригинальный тест из 24 вопросов
- ✅ Генерация премиум PNG-карточки результата (1080×1600)
- ✅ Сбор обратной связи
- ✅ Реферальная система
- ✅ Админ-панель на FastAPI с экспортом в Excel

## Технологии

- Python 3.11+
- aiogram 3.x
- FastAPI + Jinja2
- SQLAlchemy + aiosqlite
- Pillow
- openpyxl

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/abdurajabsabirov-arch/Behavior-Compass.git
cd Behavior-Compass
```

2. Создайте виртуальное окружение:
```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
# или
source .venv/bin/activate  # Linux/Mac
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` из примера:
```bash
cp .env.example .env
```

5. Откройте `.env` и добавьте токен бота:
```
BOT_TOKEN=ваш_токен_от_BotFather
```

6. Запустите бота:
```bash
python run_bot.py
```

7. Запустите админ-панель (в отдельном терминале):
```bash
python run_admin.py
```

8. Откройте админ-панель: http://127.0.0.1:8000/

## Структура проекта

```
Behavior-Compass/
├── app/
│   ├── bot/              # Telegram-бот (aiogram)
│   │   ├── handlers/     # Обработчики команд
│   │   ├── keyboards/    # Клавиатуры
│   │   └── states/       # FSM состояния
│   ├── admin/            # FastAPI админ-панель
│   │   ├── routes/       # Маршруты API
│   │   ├── templates/    # HTML шаблоны
│   │   └── static/       # CSS, JS
│   ├── core/             # Бизнес-логика, переводы, скоринг
│   ├── db/               # Модели и работа с БД
│   ├── services/         # Сервисы
│   └── assets/           # Логотип и статические файлы
├── generated/            # Сгенерированные PNG-карточки
├── .env.example
├── requirements.txt
├── run_bot.py
├── run_admin.py
└── README.md
```

## Важно

- ❌ Никогда не коммитьте реальный `.env` файл
- ❌ Токен бота хранится только в переменных окружения
- ✅ При деплое используйте переменные окружения сервера
