"""Обработчик команды /start"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.states.test_states import TestStates
from app.bot.keyboards.keyboards import (
    get_language_keyboard, 
    get_phone_keyboard,
    get_test_keyboard,
    get_feedback_keyboard,
    get_share_result_keyboard,
    get_main_menu_keyboard
)
from app.core.translations import get_text
from app.db.database import async_session_maker
from app.db.services import UserService

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    
    async with async_session_maker() as session:
        # Проверяем есть ли пользователь в БД
        user = await UserService.get_user(session, str(message.from_user.id))
        
        if user:
            # Пользователь существует
            text = get_text(user.language, "welcome")
        else:
            # Новый пользователь - покажем меню языков
            text = get_text("ru", "welcome")  # По умолчанию русский
    
    await message.answer(text, reply_markup=get_language_keyboard(), parse_mode="HTML")
    await state.set_state(TestStates.waiting_for_language)


@router.callback_query(TestStates.waiting_for_language, F.data.startswith("lang_"))
async def select_language(query: CallbackQuery, state: FSMContext):
    """Выбор языка"""
    
    language = query.data.split("_")[1]
    
    # Сохраняем язык в состояние
    await state.update_data(language=language)
    
    # Спрашиваем имя
    text = get_text(language, "ask_name")
    await query.message.answer(text)
    await state.set_state(TestStates.waiting_for_name)
    
    await query.answer()


@router.message(TestStates.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    """Получаем имя пользователя"""
    
    data = await state.get_data()
    language = data.get("language", "ru")
    
    # Сохраняем имя
    await state.update_data(name=message.text)
    
    # Запрашиваем телефон
    text = get_text(language, "ask_phone")
    await message.answer(text, reply_markup=get_phone_keyboard())
    await state.set_state(TestStates.waiting_for_phone)


@router.message(TestStates.waiting_for_phone)
async def get_phone(message: Message, state: FSMContext):
    """Получаем номер телефона"""
    
    data = await state.get_data()
    language = data.get("language", "ru")
    name = data.get("name")
    
    # Получаем номер телефона
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
    
    # Сохраняем пользователя в БД
    async with async_session_maker() as session:
        user = await UserService.get_or_create_user(
            session,
            telegram_id=str(message.from_user.id),
            username=name,
            phone=phone,
            language=language
        )
    
    # Сохраняем user_id в состояние
    await state.update_data(user_id=user.id, phone=phone)
    
    # Убираем ReplyKeyboard (кнопку "Отправить номер") и начинаем тест
    from aiogram.types import ReplyKeyboardRemove
    text = get_text(language, "test_intro")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    
    # Переходим к вопросам теста
    await state.update_data(question_index=0, answers={})
    await ask_test_question(message, state)


async def ask_test_question(message: Message, state: FSMContext):
    """Задает вопрос теста"""
    
    from app.core.questions import get_question, get_total_questions
    
    data = await state.get_data()
    question_index = data.get("question_index", 0)
    language = data.get("language", "ru")
    
    if question_index >= get_total_questions():
        # Тест завершен
        await complete_test(message, state)
        return
    
    # Показываем вопрос
    question = get_question(language, question_index)
    question_num = question_index + 1
    
    text = f"{get_text(language, 'question', num=question_num)}\n\n{question}"
    
    await message.answer(text, reply_markup=get_test_keyboard())
    await state.set_state(TestStates.answering_test)


@router.callback_query(TestStates.answering_test, F.data.startswith("answer_"))
async def answer_question(query: CallbackQuery, state: FSMContext):
    """Обработчик ответа на вопрос"""
    
    from app.core.questions import get_total_questions
    
    answer = int(query.data.split("_")[1])
    
    data = await state.get_data()
    question_index = data.get("question_index", 0)
    answers = data.get("answers", {})
    
    # Сохраняем ответ
    answers[question_index] = answer
    
    # Переходим к следующему вопросу
    question_index += 1
    
    await state.update_data(question_index=question_index, answers=answers)
    
    if question_index >= get_total_questions():
        # Тест завершен
        await complete_test(query.message, state)
    else:
        # Показываем следующий вопрос
        await ask_test_question(query.message, state)
    
    await query.answer()

async def complete_test(message: Message, state: FSMContext):
    """Завершение теста и расчет результатов"""
    
    from app.core.scoring import ScoringService
    from app.db.services import ResultService
    from app.services.card_generator import CardGenerationService
    
    data = await state.get_data()
    language = data.get("language", "ru")
    user_id = data.get("user_id")
    name = data.get("name")
    answers = data.get("answers", {})
    telegram_id = str(message.from_user.id)
    
    # Расчитываем баллы
    scores = ScoringService.calculate_scores(answers)
    primary, secondary = ScoringService.determine_primary_secondary(scores)
    
    # Сохраняем результат в БД
    async with async_session_maker() as session:
        result = await ResultService.create_result(session, telegram_id, user_id)
        
        await ResultService.update_result(
            session,
            result.id,
            blue_score=scores["blue"],
            green_score=scores["green"],
            yellow_score=scores["yellow"],
            red_score=scores["red"],
            primary_color=primary,
            secondary_color=secondary,
            completed=True
        )
        
        # Генерируем карточку
        card_path = CardGenerationService.generate_card(
            telegram_id, name, primary, secondary, scores, language
        )
        
        await ResultService.update_result(session, result.id, card_path=card_path)
    
    # Отправляем текстовый результат
    profile = ScoringService.get_profile_description(language, primary)
    text = f"✨ {get_text(language, 'results_title')}\n"
    text += f"<b>{profile.get('name', primary)}</b>\n\n"
    text += f"🔵 Blue: {scores['blue']}/100\n"
    text += f"🟢 Green: {scores['green']}/100\n"
    text += f"🟡 Yellow: {scores['yellow']}/100\n"
    text += f"🔴 Red: {scores['red']}/100\n\n"
    text += profile.get('description', '')
    
    await message.answer(text, parse_mode="HTML")
    
    # Кнопка поделиться результатом
    share_text = get_text(language, "share_results", name=name)
    await message.answer(
        share_text,
        reply_markup=get_share_result_keyboard()
    )
    
    # Сохраняем ID результата в состояние
    await state.update_data(result_id=result.id, card_path=card_path, scores=scores, 
                           primary_color=primary, secondary_color=secondary)
    
    await state.set_state(TestStates.viewing_results)


# Обработчики кнопок после результатов
@router.callback_query(TestStates.viewing_results, F.data == "share_result")
async def share_result(query: CallbackQuery, state: FSMContext):
    """Поделиться результатом с другом"""
    from app.bot.keyboards.keyboards import get_main_menu_keyboard
    
    data = await state.get_data()
    language = data.get("language", "ru")
    card_path = data.get("card_path")
    
    # Показываем информацию о реферальной программе
    share_texts = {
        "ru": "👥 Поделитесь ссылкой на бота с друзьями!\n\nВаши друзья получат персональный результат теста.\n\n@Behavior_Compass_bot",
        "uz": "👥 Do'stlaringiz bilan bot havolasini ulashing!\n\nDo'stlaringiz shaxsiy test natijasini oladi.\n\n@Behavior_Compass_bot",
        "en": "👥 Share the bot link with your friends!\n\nYour friends will get a personalized test result.\n\n@Behavior_Compass_bot",
        "de": "👥 Teilen Sie den Bot-Link mit Ihren Freunden!\n\nIhre Freunde erhalten ein persönliches Testergebnis.\n\n@Behavior_Compass_bot",
        "tr": "👥 Bot bağlantısını arkadaşlarınızla paylaşın!\n\nArkadaşlarınız kişiselleştirilmiş test sonuçlarını alır.\n\n@Behavior_Compass_bot",
    }
    share_text = share_texts.get(language, share_texts["ru"])
    await query.message.answer(share_text)
    
    # Показываем главное меню
    menu_titles = {
        "ru": "Что вы хотите сделать?",
        "uz": "Nima qilmoqchisiz?",
        "en": "What would you like to do?",
        "de": "Was möchten Sie tun?",
        "tr": "Ne yapmak istersiniz?",
    }
    await query.message.answer(
        menu_titles.get(language, "What would you like to do?"),
        reply_markup=get_main_menu_keyboard(language)
    )
    
    await state.set_state(TestStates.in_main_menu)
    await query.answer()


@router.callback_query(TestStates.viewing_results, F.data == "rate_result")
async def rate_result(query: CallbackQuery, state: FSMContext):
    """Оценить результат"""
    from app.bot.keyboards.keyboards import get_feedback_keyboard
    
    data = await state.get_data()
    language = data.get("language", "ru")
    
    text = get_text(language, "feedback_request")
    await query.message.answer(text, reply_markup=get_feedback_keyboard())
    
    await state.set_state(TestStates.waiting_for_feedback)
    await query.answer()


@router.callback_query(TestStates.viewing_results, F.data == "viewing_menu_home")
async def menu_home(query: CallbackQuery, state: FSMContext):
    """Главное меню"""
    from app.bot.keyboards.keyboards import get_main_menu_keyboard
    
    data = await state.get_data()
    language = data.get("language", "ru")
    
    menu_titles = {
        "ru": "🏠 Главное меню",
        "uz": "🏠 Asosiy menyu",
        "en": "🏠 Main Menu",
        "de": "🏠 Hauptmenü",
        "tr": "🏠 Ana Menü",
    }
    await query.message.answer(
        menu_titles.get(language, "🏠 Main Menu"),
        reply_markup=get_main_menu_keyboard(language)
    )
    
    await state.set_state(TestStates.in_main_menu)
    await query.answer()


# Обработчики главного меню
@router.callback_query(TestStates.in_main_menu, F.data == "menu_test")
async def menu_restart_test(query: CallbackQuery, state: FSMContext):
    """Пройти тест заново"""
    data = await state.get_data()
    language = data.get("language", "ru")
    
    text = get_text(language, "test_intro")
    await query.message.answer(text)
    
    # Сбрасываем состояние теста
    await state.update_data(question_index=0, answers={})
    await ask_test_question(query.message, state)
    
    await query.answer()


@router.callback_query(TestStates.in_main_menu, F.data == "menu_results")
async def menu_view_results(query: CallbackQuery, state: FSMContext):
    """Мои результаты"""
    from aiogram.types import FSInputFile
    
    data = await state.get_data()
    language = data.get("language", "ru")
    card_path = data.get("card_path")
    
    text = "📊 Ваши последние результаты:\n\n"
    
    if card_path:
        photo = FSInputFile(card_path)
        await query.message.answer_photo(photo=photo, caption=text)
    
    await query.answer()


@router.callback_query(TestStates.in_main_menu, F.data == "menu_referral")
async def menu_referral(query: CallbackQuery, state: FSMContext):
    """Реферальная программа"""
    data = await state.get_data()
    language = data.get("language", "ru")
    telegram_id = str(query.from_user.id)
    
    text = "👥 <b>Программа рефералов</b>\n\n" \
           "Приглашайте друзей и получайте награды!\n\n" \
           "🔗 Ваша реферальная ссылка:\n\n" \
           f"@Behavior_Compass_bot?start={telegram_id}\n\n" \
           "Каждый приглашенный друг получит скидку 20% на премиум результаты,\n" \
           "а вы получите бонусы!"
    
    await query.message.answer(text, parse_mode="HTML")
    await query.answer()


@router.callback_query(TestStates.in_main_menu, F.data == "menu_about")
async def menu_about(query: CallbackQuery, state: FSMContext):
    """О тесте"""
    text = "ℹ️ <b>О тесте Behavior Compass</b>\n\n" \
           "Это психологический тест, который определяет ваш поведенческий тип " \
           "на основе 4-цветовой модели:\n\n" \
           "🔵 <b>Синий</b> - Сопереживающий\n" \
           "Эмпатичный, дружелюбный, ценит отношения\n\n" \
           "🟢 <b>Зеленый</b> - Аналитический\n" \
           "Логичный, внимательный к деталям, системный\n\n" \
           "🟡 <b>Желтый</b> - Энтузиаст\n" \
           "Творческий, оптимистичный, вдохновляющий\n\n" \
           "🔴 <b>Красный</b> - Лидер\n" \
           "Уверенный, решительный, ориентированный на результаты"
    
    await query.message.answer(text, parse_mode="HTML")
    await query.answer()


@router.callback_query(TestStates.in_main_menu, F.data == "menu_share")
async def menu_share_bot(query: CallbackQuery, state: FSMContext):
    """Поделиться ботом"""
    text = "📢 <b>Поделиться Behavior Compass</b>\n\n" \
           "Пригласите друзей узнать свой тип личности!\n\n" \
           "@Behavior_Compass_bot\n\n" \
           "Кажди ваш друг получит уникальный результат и сможет сравнить " \
           "свой тип с вашим 🎯"
    
    await query.message.answer(text, parse_mode="HTML")
    await query.answer()
