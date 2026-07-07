"""Сервис скоринга и определения цветового профиля"""


# Вопросы по цветам: индексы вопросов для каждого цвета
# Соответствует порядку вопросов в questions.py

BLUE_QUESTIONS = [2, 6, 10, 14, 18]  # Empathetic - Сопереживающий
GREEN_QUESTIONS = [3, 7, 11, 15, 19]  # Analytical - Аналитический
YELLOW_QUESTIONS = [1, 4, 8, 12, 16, 20]  # Enthusiast - Энтузиаст
RED_QUESTIONS = [0, 5, 9, 13, 17, 21, 22, 23]  # Leader - Лидер

# Описания для каждого цвета
COLOR_PROFILES = {
    "en": {
        "blue": {
            "name": "🔵 Blue - Empathetic",
            "description": """You are a compassionate and caring individual who values harmony and deep connections with others. 
            
Key traits:
• Excellent listener and empathetic
• Prioritizes relationships and harmony
• Supports others and creates a nurturing environment
• Values loyalty and trust
• May struggle with making tough decisions that affect others

In work:
• Great team player and mediator
• Creates supportive environments
• Excellent at understanding team dynamics
• May avoid conflict even when necessary
• Prefers collaborative approaches"""
        },
        "green": {
            "name": "🟢 Green - Analytical",
            "description": """You are a logical and detail-oriented thinker who values accuracy and understanding.

Key traits:
• Analytical and systematic
• Focuses on facts and data
• Values competence and expertise
• Prefers to understand the "why" behind decisions
• Can be cautious and thorough

In work:
• Excellent problem solver
• Quality-focused and reliable
• Does thorough research before decisions
• May be overly critical or perfectionist
• Prefers structured environments"""
        },
        "yellow": {
            "name": "🟡 Yellow - Enthusiast",
            "description": """You are an energetic and optimistic individual who brings excitement and possibilities to everything.

Key traits:
• Enthusiastic and optimistic
• Spontaneous and creative
• Sees possibilities and new opportunities
• Energizes others with enthusiasm
• Can be impulsive or lose focus

In work:
• Great at networking and building relationships
• Brings energy and creativity to projects
• Excellent communicator
• May lack follow-through on details
• Thrives in dynamic environments"""
        },
        "red": {
            "name": "🔴 Red - Leader",
            "description": """You are a decisive and ambitious individual who prefers taking action and leading others.

Key traits:
• Decisive and action-oriented
• Comfortable with authority and control
• Sets and achieves ambitious goals
• Direct and competitive
• Prefers efficiency over lengthy discussion

In work:
• Natural leader and decision-maker
• Drives results and productivity
• Takes charge in challenging situations
• May be overly directive or dismissive of others
• Prefers autonomous roles"""
        }
    },
    
    "ru": {
        "blue": {
            "name": "🔵 Синий - Сопереживающий",
            "description": """Вы сострадательный и заботливый человек, который ценит гармонию и глубокие связи с другими.

Ключевые черты:
• Отличный слушатель и эмпатичный
• Отдает приоритет отношениям и гармонии
• Поддерживает других и создает благоприятную среду
• Ценит верность и доверие
• Может испытывать трудности с принятием трудных решений, влияющих на других

На работе:
• Отличный командный игрок и посредник
• Создает поддерживающую среду
• Отлично разбирается в динамике команды
• Может избегать конфликтов даже при необходимости
• Предпочитает совместные подходы"""
        },
        "green": {
            "name": "🟢 Зеленый - Аналитический",
            "description": """Вы логичный и внимательный к деталям мыслитель, который ценит точность и понимание.

Ключевые черты:
• Аналитический и систематический
• Сосредотачивается на фактах и данных
• Ценит компетентность и опыт
• Предпочитает понимать "почему" за решениями
• Может быть осторожным и тщательным

На работе:
• Отличный решатель проблем
• Ориентирован на качество и надежность
• Проводит тщательное исследование перед решениями
• Может быть чрезмерно критичным или перфекционистом
• Предпочитает структурированную среду"""
        },
        "yellow": {
            "name": "🟡 Желтый - Энтузиаст",
            "description": """Вы энергичный и оптимистичный человек, который приносит волнение и возможности во все.

Ключевые черты:
• Энтузиастичный и оптимистичный
• Спонтанный и творческий
• Видит возможности и новые перспективы
• Вдохновляет других своим энтузиазмом
• Может быть импульсивным или теряющим фокус

На работе:
• Отличается в сетях и построении отношений
• Приносит энергию и творчество в проекты
• Отличный коммуникатор
• Может не хватать внимания к деталям
• Процветает в динамичной среде"""
        },
        "red": {
            "name": "🔴 Красный - Лидер",
            "description": """Вы решительный и амбициозный человек, который предпочитает действие и лидерство.

Ключевые черты:
• Решительный и ориентированный на действие
• Комфортабелен с властью и контролем
• Ставит и достигает амбициозные цели
• Прямой и конкурентный
• Предпочитает эффективность длительному обсуждению

На работе:
• Естественный лидер и принимающий решения
• Стимулирует результаты и производительность
• Берет на себя ответственность в сложных ситуациях
• Может быть чрезмерно директивным или пренебрегающим другими
• Предпочитает автономные роли"""
        }
    }
}


class ScoringService:
    """Сервис для скоринга и определения цвета"""
    
    @staticmethod
    def calculate_scores(answers: dict) -> dict:
        """
        Рассчитывает баллы для каждого цвета
        
        Args:
            answers: Словарь {вопрос_индекс: оценка (1-5)}
            
        Returns:
            Словарь с баллами для каждого цвета
        """
        scores = {
            "blue": 0,
            "green": 0,
            "yellow": 0,
            "red": 0
        }
        
        # Подсчитываем баллы для каждого цвета
        for q_idx in BLUE_QUESTIONS:
            if q_idx in answers:
                scores["blue"] += answers[q_idx]
        
        for q_idx in GREEN_QUESTIONS:
            if q_idx in answers:
                scores["green"] += answers[q_idx]
        
        for q_idx in YELLOW_QUESTIONS:
            if q_idx in answers:
                scores["yellow"] += answers[q_idx]
        
        for q_idx in RED_QUESTIONS:
            if q_idx in answers:
                scores["red"] += answers[q_idx]
        
        # Нормализуем баллы к шкале 0-100
        max_score = max(
            len(BLUE_QUESTIONS) * 5,
            len(GREEN_QUESTIONS) * 5,
            len(YELLOW_QUESTIONS) * 5,
            len(RED_QUESTIONS) * 5
        )
        
        for color in scores:
            scores[color] = round((scores[color] / max_score) * 100)
        
        return scores
    
    @staticmethod
    def determine_primary_secondary(scores: dict) -> tuple:
        """
        Определяет основной и вторичный цвета
        
        Returns:
            Кортеж (основной_цвет, вторичный_цвет)
        """
        sorted_colors = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_colors[0][0]
        secondary = sorted_colors[1][0]
        
        return primary, secondary
    
    @staticmethod
    def get_profile_description(language: str, color: str) -> dict:
        """Получает описание профиля для цвета"""
        if language not in COLOR_PROFILES:
            language = "en"
        
        return COLOR_PROFILES[language].get(color, {})
