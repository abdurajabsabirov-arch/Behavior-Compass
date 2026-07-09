from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_language_keyboard():
    """Клавиатура выбора языка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton(text="🇹🇷 Türkçe", callback_data="lang_tr")],
    ])


def get_phone_keyboard():
    """Клавиатура для отправки номера телефона"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить номер", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_test_keyboard():
    """Клавиатура для ответов на тест (1-5 баллов)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="answer_1"),
            InlineKeyboardButton(text="2", callback_data="answer_2"),
            InlineKeyboardButton(text="3", callback_data="answer_3"),
            InlineKeyboardButton(text="4", callback_data="answer_4"),
            InlineKeyboardButton(text="5", callback_data="answer_5"),
        ]
    ])


def get_feedback_keyboard():
    """Клавиатура для оценки (звёзды на 2 строки)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐", callback_data="rating_1"),
            InlineKeyboardButton(text="⭐⭐", callback_data="rating_2"),
            InlineKeyboardButton(text="⭐⭐⭐", callback_data="rating_3"),
        ],
        [
            InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data="rating_4"),
            InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data="rating_5"),
        ]
    ])


def get_feedback_action_keyboard():
    """Клавиатура действий после теста"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Оставить отзыв", callback_data="action_feedback")],
        [InlineKeyboardButton(text="🔗 Поделиться ботом", callback_data="action_share")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_home")],
    ])


def get_confirm_referral_keyboard():
    """Клавиатура подтверждения участия в реферальной программе"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data="referral_yes"),
            InlineKeyboardButton(text="❌ Нет", callback_data="referral_no"),
        ]
    ])


def get_share_result_keyboard():
    """Клавиатура поделиться результатом"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Поделиться с другом", callback_data="share_result")],
        [InlineKeyboardButton(text="❤️ Оценить результат", callback_data="rate_result")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="viewing_menu_home")],
    ])


def get_context_keyboard(language="ru"):
    """Кнопки для раскрытия результата в рабочих контекстах."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 Подробнее о моём стиле", callback_data="context_detailed")],
        [
            InlineKeyboardButton(text="💪 Сильные стороны", callback_data="context_strengths"),
            InlineKeyboardButton(text="⚠️ Риски", callback_data="context_risks"),
        ],
        [InlineKeyboardButton(text="💬 Как со мной общаться", callback_data="context_communication")],
        [
            InlineKeyboardButton(text="💼 Я в продажах", callback_data="context_sales"),
            InlineKeyboardButton(text="🤝 Я в переговорах", callback_data="context_negotiations"),
        ],
        [
            InlineKeyboardButton(text="👥 Я в команде", callback_data="context_team"),
            InlineKeyboardButton(text="🔥 В стрессе", callback_data="context_stress"),
        ],
        [InlineKeyboardButton(text="🚀 Совет по развитию", callback_data="context_advice")],
    ])


def get_main_menu_keyboard(language="ru"):
    """Главное меню бота"""
    texts = {
        "ru": {
            "test": "🧠 Пройти тест заново",
            "results": "📊 Мои результаты",
            "referral": "👥 Реферальная программа",
            "about": "ℹ️ О тесте",
            "share": "📢 Поделиться ботом"
        },
        "uz": {
            "test": "🧠 Testni qayta o'tish",
            "results": "📊 Mening natijalarim",
            "referral": "👥 Tavsiylar dasturi",
            "about": "ℹ️ Test haqida",
            "share": "📢 Botni baham ko'rish"
        },
        "en": {
            "test": "🧠 Retake Test",
            "results": "📊 My Results",
            "referral": "👥 Referral Program",
            "about": "ℹ️ About Test",
            "share": "📢 Share Bot"
        },
        "de": {
            "test": "🧠 Test erneut durchführen",
            "results": "📊 Meine Ergebnisse",
            "referral": "👥 Referral-Programm",
            "about": "ℹ️ Über den Test",
            "share": "📢 Bot teilen"
        },
        "tr": {
            "test": "🧠 Testi Tekrar Al",
            "results": "📊 Sonuçlarım",
            "referral": "👥 Referral Programı",
            "about": "ℹ️ Test Hakkında",
            "share": "📢 Botu Paylaş"
        }
    }
    
    lang_texts = texts.get(language, texts["ru"])
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lang_texts["test"], callback_data="menu_test")],
        [InlineKeyboardButton(text=lang_texts["results"], callback_data="menu_results")],
        [InlineKeyboardButton(text=lang_texts["about"], callback_data="menu_about")],
        [InlineKeyboardButton(text=lang_texts["share"], callback_data="menu_share")],
    ])
