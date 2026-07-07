from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=False, index=True)
    username = Column(String(100))
    phone = Column(String(20), nullable=False)
    language = Column(String(10), default="ru")  # ru, uz, en, de, tr
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    referrer_id = Column(String(50), nullable=True)  # telegram_id того, кто пригласил


class Result(Base):
    """Модель результата теста"""
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), nullable=False, index=True)
    user_id = Column(Integer, nullable=False)
    
    # Баллы по цветам (0-100)
    blue_score = Column(Integer, default=0)
    green_score = Column(Integer, default=0)
    yellow_score = Column(Integer, default=0)
    red_score = Column(Integer, default=0)
    
    # Основной и вторичный цвет
    primary_color = Column(String(10))  # blue, green, yellow, red
    secondary_color = Column(String(10))
    
    # Описание профиля
    description = Column(Text)
    
    # Путь к сгенерированной карточке
    card_path = Column(String(255), nullable=True)
    
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Feedback(Base):
    """Модель обратной связи"""
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), nullable=False, index=True)
    result_id = Column(Integer, nullable=False)
    
    # Оценка: 1-5 звезд
    rating = Column(Integer)
    
    # Комментарий
    comment = Column(Text, nullable=True)
    
    # Согласие на реферальную систему
    agree_referral = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class Referral(Base):
    """Модель реферальной системы"""
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    referrer_id = Column(String(50), nullable=False, index=True)  # telegram_id того, кто пригласил
    referred_id = Column(String(50), nullable=False, index=True)  # telegram_id приглашенного
    
    completed_test = Column(Boolean, default=False)  # Если приглашенный завершил тест
    
    created_at = Column(DateTime, default=datetime.utcnow)
