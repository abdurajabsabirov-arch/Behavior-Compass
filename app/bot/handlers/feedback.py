"""Обработчик обратной связи"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.states.test_states import TestStates
from app.core.translations import get_text
from app.db.database import async_session_maker
from app.db.services import FeedbackService, ReferralService

router = Router()


@router.callback_query(TestStates.waiting_for_feedback, F.data.startswith("rating_"))
async def process_feedback_rating(query: CallbackQuery, state: FSMContext):
    """Обработчик оценки"""
    
    rating = int(query.data.split("_")[1])
    
    data = await state.get_data()
    language = data.get("language", "ru")
    
    await state.update_data(rating=rating)
    
    # Спрашиваем комментарий
    text = get_text(language, "feedback_comment")
    await query.message.answer(text)
    
    await state.set_state(TestStates.waiting_for_feedback_comment)
    await query.answer()


@router.message(TestStates.waiting_for_feedback_comment)
async def process_feedback_comment(message: Message, state: FSMContext):
    """Обработчик комментария"""
    
    from app.bot.keyboards.keyboards import get_confirm_referral_keyboard
    
    data = await state.get_data()
    language = data.get("language", "ru")
    result_id = data.get("result_id")
    rating = data.get("rating")
    telegram_id = str(message.from_user.id)
    
    comment = message.text if message.text != "/skip" else None
    
    # Сохраняем отзыв в БД
    async with async_session_maker() as session:
        await FeedbackService.create_feedback(
            session,
            telegram_id=telegram_id,
            result_id=result_id,
            rating=rating,
            comment=comment,
            agree_referral=False  # Спросим дальше
        )
    
    # Спрашиваем про реферальную программу
    text = get_text(language, "referral_question")
    await message.answer(text, reply_markup=get_confirm_referral_keyboard())
    
    await state.clear()


@router.callback_query(F.data == "referral_yes")
async def confirm_referral(query: CallbackQuery, state: FSMContext):
    """Подтверждение участия в реферальной программе"""
    
    telegram_id = str(query.from_user.id)
    language = "ru"  # Можно получить из БД
    
    # Генерируем реферальную ссылку
    referral_link = f"https://t.me/Behavior_Compass_bot?start=ref_{telegram_id}"
    
    text = get_text(language, "referral_link") + referral_link
    await query.message.answer(text)
    
    # Спасибо за обратную связь
    thank_you_text = get_text(language, "thank_you")
    await query.message.answer(thank_you_text)
    
    await query.answer()
    await state.clear()


@router.callback_query(F.data == "referral_no")
async def decline_referral(query: CallbackQuery, state: FSMContext):
    """Отказ от реферальной программы"""
    
    language = "ru"  # Можно получить из БД
    
    thank_you_text = get_text(language, "thank_you")
    await query.message.answer(thank_you_text)
    
    await query.answer()
    await state.clear()
