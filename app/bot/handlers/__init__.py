"""Инициализация handlers пакета"""

from .start import router as start_router
from .feedback import router as feedback_router

__all__ = ["start_router", "feedback_router"]
