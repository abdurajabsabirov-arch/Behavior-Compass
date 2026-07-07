from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User, Result, Feedback, Referral
from datetime import datetime


class UserService:
    """Сервис работы с пользователями"""
    
    @staticmethod
    async def get_or_create_user(session: AsyncSession, telegram_id: str, username: str, phone: str, language: str = "ru", referrer_id: str = None):
        """Получает или создает пользователя"""
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                phone=phone,
                language=language,
                referrer_id=referrer_id
            )
            session.add(user)
            await session.commit()
        
        return user
    
    @staticmethod
    async def get_user(session: AsyncSession, telegram_id: str):
        """Получает пользователя"""
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    async def update_user(session: AsyncSession, telegram_id: str, **kwargs):
        """Обновляет пользователя"""
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            await session.commit()
        
        return user


class ResultService:
    """Сервис работы с результатами"""
    
    @staticmethod
    async def create_result(session: AsyncSession, telegram_id: str, user_id: int):
        """Создает новый результат"""
        result = Result(telegram_id=telegram_id, user_id=user_id)
        session.add(result)
        await session.commit()
        return result
    
    @staticmethod
    async def get_result(session: AsyncSession, result_id: int):
        """Получает результат"""
        stmt = select(Result).where(Result.id == result_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    async def get_latest_result(session: AsyncSession, telegram_id: str):
        """Получает последний результат пользователя"""
        stmt = select(Result).where(Result.telegram_id == telegram_id).order_by(Result.created_at.desc())
        result = await session.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    async def update_result(session: AsyncSession, result_id: int, **kwargs):
        """Обновляет результат"""
        stmt = select(Result).where(Result.id == result_id)
        result = await session.execute(stmt)
        result_obj = result.scalars().first()
        
        if result_obj:
            for key, value in kwargs.items():
                if hasattr(result_obj, key):
                    setattr(result_obj, key, value)
            result_obj.updated_at = datetime.utcnow()
            await session.commit()
        
        return result_obj


class FeedbackService:
    """Сервис работы с отзывами"""
    
    @staticmethod
    async def create_feedback(session: AsyncSession, telegram_id: str, result_id: int, rating: int, comment: str = None, agree_referral: bool = False):
        """Создает отзыв"""
        feedback = Feedback(
            telegram_id=telegram_id,
            result_id=result_id,
            rating=rating,
            comment=comment,
            agree_referral=agree_referral
        )
        session.add(feedback)
        await session.commit()
        return feedback


class ReferralService:
    """Сервис работы с реферальной системой"""
    
    @staticmethod
    async def create_referral(session: AsyncSession, referrer_id: str, referred_id: str):
        """Создает запись о реферале"""
        stmt = select(Referral).where(
            (Referral.referrer_id == referrer_id) & 
            (Referral.referred_id == referred_id)
        )
        result = await session.execute(stmt)
        existing = result.scalars().first()
        
        if not existing:
            referral = Referral(referrer_id=referrer_id, referred_id=referred_id)
            session.add(referral)
            await session.commit()
            return referral
        
        return existing
    
    @staticmethod
    async def get_referral_count(session: AsyncSession, referrer_id: str):
        """Получает количество приглашенных"""
        stmt = select(Referral).where(Referral.referrer_id == referrer_id)
        result = await session.execute(stmt)
        return len(result.scalars().all())
