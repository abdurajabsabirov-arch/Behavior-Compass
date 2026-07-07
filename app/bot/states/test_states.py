from aiogram.fsm.state import State, StatesGroup


class TestStates(StatesGroup):
    """Состояния для теста"""
    waiting_for_language = State()
    waiting_for_name = State()
    waiting_for_phone = State()
    answering_test = State()  # Ответ на вопрос теста
    viewing_results = State()  # Просмотр результатов
    waiting_for_feedback = State()
    waiting_for_feedback_comment = State()
    in_main_menu = State()  # В главном меню


class AdminStates(StatesGroup):
    """Состояния для администратора"""
    waiting_for_action = State()
