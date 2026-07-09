"""Scoring and profile result generation for Behavior Compass."""

BLUE_QUESTIONS = [2, 6, 10, 14, 18]
GREEN_QUESTIONS = [3, 7, 11, 15, 19]
YELLOW_QUESTIONS = [1, 4, 8, 12, 16, 20]
RED_QUESTIONS = [0, 5, 9, 13, 17, 21, 22, 23]

COLORS = ("red", "yellow", "blue", "green")
MIXED_THRESHOLD = 10

REQUIRED_SINGLE_PROFILE_KEYS = set(COLORS)
REQUIRED_MIXED_PROFILE_KEYS = {
    f"{primary}_{secondary}"
    for primary in COLORS
    for secondary in COLORS
    if primary != secondary
}
REQUIRED_PROFILE_KEYS = REQUIRED_SINGLE_PROFILE_KEYS | REQUIRED_MIXED_PROFILE_KEYS

STYLE_LABELS = {
    "red": "Красный - результат и влияние",
    "yellow": "Желтый - энергия и идеи",
    "blue": "Синий - анализ и точность",
    "green": "Зеленый - стабильность и поддержка",
}

PROFILE_NAMES = {
    "red": "Красный профиль",
    "yellow": "Желтый профиль",
    "blue": "Синий профиль",
    "green": "Зеленый профиль",
}

MIXED_PROFILE_NAMES = {
    key: f"{STYLE_LABELS[key.split('_')[0]].split(' - ')[0]} + {STYLE_LABELS[key.split('_')[1]].split(' - ')[0]}"
    for key in REQUIRED_MIXED_PROFILE_KEYS
}

SINGLE_PROFILE_DESCRIPTIONS = {
    "red": (
        "Вы быстро переходите к действию, берете ответственность и естественно двигаете людей к результату. "
        "Ваша сильная сторона - ясность цели, решительность и умение ускорять процессы."
    ),
    "yellow": (
        "Вы создаете энергию, легко вовлекаете людей и хорошо видите возможности. "
        "Ваша сильная сторона - коммуникация, идеи и способность оживлять даже сложные задачи."
    ),
    "blue": (
        "Вы смотрите на ситуацию через факты, структуру и качество решения. "
        "Ваша сильная сторона - анализ, точность, критическое мышление и умение снижать хаос."
    ),
    "green": (
        "Вы удерживаете устойчивость, доверие и рабочий ритм. "
        "Ваша сильная сторона - надежность, поддержка, последовательность и внимание к людям."
    ),
}

MIXED_PROFILE_DESCRIPTIONS = {
    "red_yellow": "Вы соединяете напор результата с яркой вовлекающей подачей. Хорошо запускаете инициативы, продаете идеи и заражаете темпом.",
    "red_blue": "Вы соединяете решительность с аналитикой. Умеете быстро принимать решения, но опираетесь на факты и проверку рисков.",
    "red_green": "Вы соединяете требовательность к результату с заботой о стабильности. Хорошо ведете людей через изменения, если сохраняете уважительный тон.",
    "yellow_red": "Вы начинаете с энергии и контакта, а затем быстро переводите разговор в действие. Сильны в переговорах, презентациях и запуске команд.",
    "yellow_blue": "Вы соединяете идеи с анализом. Можете придумывать варианты, объяснять их людям и при этом проверять логику решения.",
    "yellow_green": "Вы создаете теплую атмосферу и поддерживаете людей через вдохновение. Хорошо работаете там, где важны доверие, мотивация и командный дух.",
    "blue_red": "Вы начинаете с анализа, но умеете переводить выводы в жесткие решения. Сильны в диагностике, стратегии и управлении сложными задачами.",
    "blue_yellow": "Вы соединяете системное мышление с понятной коммуникацией. Умеете упаковать сложную мысль так, чтобы ее приняли другие.",
    "blue_green": "Вы соединяете точность с надежностью. Хорошо поддерживаете порядок, качество, процессы и спокойное движение без лишнего драматизма.",
    "green_red": "Вы начинаете с устойчивости и доверия, но можете брать управление, когда ситуация требует ясности. Сильны в спокойном лидерстве.",
    "green_yellow": "Вы соединяете поддержку с позитивной энергией. Умеете создавать безопасную среду, где людям легче включаться и проявляться.",
    "green_blue": "Вы соединяете стабильность с внимательным анализом. Хорошо видите детали, бережете качество и помогаете команде не терять опору.",
}

LOWEST_STYLE_BLOCKS = {
    "red": "Зона внимания: может не хватать прямого действия, жестких приоритетов и готовности брать власть в момент неопределенности.",
    "yellow": "Зона внимания: может не хватать легкости, гибкости, публичной энергии и способности быстро вовлекать людей эмоционально.",
    "blue": "Зона внимания: может не хватать анализа, проверки фактов, структуры и паузы перед важным решением.",
    "green": "Зона внимания: может не хватать терпения, устойчивого ритма, мягкости и внимания к эмоциональной безопасности людей.",
}


def _context_blocks(title: str, single_templates: dict, mixed_template: str) -> dict:
    blocks = {}
    for key in REQUIRED_SINGLE_PROFILE_KEYS:
        blocks[key] = f"<b>{title}</b>\n\n{single_templates[key]}"
    for key in REQUIRED_MIXED_PROFILE_KEYS:
        primary, secondary = key.split("_")
        blocks[key] = (
            f"<b>{title}</b>\n\n"
            f"{mixed_template.format(primary=STYLE_LABELS[primary], secondary=STYLE_LABELS[secondary])}"
        )
    return blocks


MANAGEMENT_BLOCKS = _context_blocks(
    "В управлении людьми",
    {
        "red": "Вы управляете через цель, ответственность и темп. Следите, чтобы давление не заменяло диалог.",
        "yellow": "Вы управляете через вдохновение и контакт. Фиксируйте договоренности, чтобы энергия превращалась в результат.",
        "blue": "Вы управляете через ясные критерии и логику. Добавляйте больше живой обратной связи, чтобы команда не чувствовала холодность.",
        "green": "Вы управляете через доверие и стабильность. Важно не откладывать сложные решения ради сохранения спокойствия.",
    },
    "Ваш управленческий стиль сочетает {primary} как первый импульс и {secondary} как усиливающий слой. Используйте оба, но не позволяйте второму размывать главный способ влияния.",
)

SALES_BLOCKS = _context_blocks(
    "В продажах и переговорах",
    {
        "red": "Вы сильны в закрытии, торге и прямом продвижении решения. Работайте с потребностью клиента до давления на итог.",
        "yellow": "Вы сильны в установлении контакта, презентации и создании интереса. Держите фокус на следующем конкретном шаге.",
        "blue": "Вы сильны в аргументации, доказательствах и работе с возражениями. Добавляйте эмоцию и простую выгоду для клиента.",
        "green": "Вы сильны в доверии, сопровождении и долгих отношениях. Не бойтесь яснее просить решение и обозначать сроки.",
    },
    "В продажах у вас работает связка {primary} + {secondary}. Первый стиль открывает переговоры, второй помогает удерживать баланс и адаптироваться к клиенту.",
)

TEAM_BLOCKS = _context_blocks(
    "В командной работе",
    {
        "red": "Вы берете инициативу и ускоряете группу. Полезно чаще проверять, успевают ли остальные включиться.",
        "yellow": "Вы поднимаете настроение и соединяете людей. Полезно помогать команде не терять структуру и сроки.",
        "blue": "Вы приносите качество, порядок и критическое мышление. Полезно озвучивать не только риски, но и поддержку.",
        "green": "Вы стабилизируете команду и помогаете сохранять доверие. Полезно проявлять позицию раньше, особенно в спорных темах.",
    },
    "В команде вы проявляете {primary} как основной вклад, а {secondary} как способ адаптации. Эта связка особенно ценна, когда роль человека в группе меняется по ситуации.",
)

COMMUNICATION_BLOCKS = _context_blocks(
    "В коммуникации",
    {
        "red": "Вы говорите прямо и по делу. Смягчайте формулировки там, где собеседнику важно почувствовать уважение и участие.",
        "yellow": "Вы говорите живо и образно. Проверяйте, что после разговора у всех одинаковое понимание задачи.",
        "blue": "Вы говорите точно и аргументированно. Упрощайте сложные объяснения, если человеку нужно быстро принять решение.",
        "green": "Вы говорите спокойно и бережно. Добавляйте больше ясности, если тема требует прямой позиции.",
    },
    "В коммуникации заметна связка {primary} + {secondary}: один стиль задает тон, второй помогает достраивать контакт с разными людьми.",
)

STRESS_BLOCKS = _context_blocks(
    "В стрессе",
    {
        "red": "В стрессе вы можете давить, ускорять и резко резать лишнее. Помогает короткая пауза перед приказом или конфликтным решением.",
        "yellow": "В стрессе вы можете перескакивать между идеями и искать быстрый выход. Помогает список из трех конкретных действий.",
        "blue": "В стрессе вы можете уходить в анализ и контроль деталей. Помогает заранее ограничить время на проверку и принять рабочую версию решения.",
        "green": "В стрессе вы можете замедляться и избегать напряжения. Помогает назвать проблему прямо и выбрать первый маленький шаг.",
    },
    "В стрессе первым включается {primary}, а затем подключается {secondary}. Следите, чтобы эта пара не уходила в крайность: возвращайтесь к фактам, людям и следующему шагу.",
)

ADVICE_BLOCKS = _context_blocks(
    "Совет по развитию",
    {
        "red": "Развивайте терпение к процессу и умение слышать слабые сигналы от людей до того, как ситуация станет проблемой.",
        "yellow": "Развивайте завершение начатого: фиксируйте сроки, ответственных и критерий готовности.",
        "blue": "Развивайте скорость решения и способность объяснять сложное простыми словами.",
        "green": "Развивайте прямоту, личную инициативу и готовность входить в конструктивный конфликт.",
    },
    "Для роста вашей связки {primary} + {secondary} важно осознанно тренировать противоположные качества: не ломать свой стиль, а расширять диапазон поведения.",
)

CONTEXT_BLOCKS = {
    "management": MANAGEMENT_BLOCKS,
    "sales": SALES_BLOCKS,
    "team": TEAM_BLOCKS,
    "communication": COMMUNICATION_BLOCKS,
    "stress": STRESS_BLOCKS,
    "advice": ADVICE_BLOCKS,
}


class ScoringService:
    """Service for scoring answers and producing profile text."""

    @staticmethod
    def calculate_scores(answers: dict) -> dict:
        scores = {"blue": 0, "green": 0, "yellow": 0, "red": 0}

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

        max_score = max(
            len(BLUE_QUESTIONS) * 5,
            len(GREEN_QUESTIONS) * 5,
            len(YELLOW_QUESTIONS) * 5,
            len(RED_QUESTIONS) * 5,
        )

        for color in scores:
            scores[color] = round((scores[color] / max_score) * 100)

        return scores

    @staticmethod
    def sort_scores(scores: dict) -> list:
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)

    @staticmethod
    def determine_primary_secondary(scores: dict) -> tuple:
        sorted_colors = ScoringService.sort_scores(scores)
        return sorted_colors[0][0], sorted_colors[1][0]

    @staticmethod
    def get_level(score: int) -> str:
        if score <= 30:
            return "слабо выражен"
        if score <= 50:
            return "ситуативно выражен"
        if score <= 70:
            return "заметно выражен"
        return "ярко выражен"

    @staticmethod
    def get_profile_key(scores: dict) -> dict:
        sorted_scores = ScoringService.sort_scores(scores)
        primary_style, primary_score = sorted_scores[0]
        secondary_style, secondary_score = sorted_scores[1]
        lowest_style, lowest_score = sorted_scores[-1]
        difference = primary_score - secondary_score

        if difference <= MIXED_THRESHOLD:
            profile_type = "mixed"
            profile_key = f"{primary_style}_{secondary_style}"
        else:
            profile_type = "single"
            profile_key = primary_style

        return {
            "profile_type": profile_type,
            "profile_key": profile_key,
            "primary_style": primary_style,
            "secondary_style": secondary_style,
            "lowest_style": lowest_style,
            "lowest_score": lowest_score,
            "difference": difference,
        }

    @staticmethod
    def generate_score_table(scores: dict) -> str:
        rows = []
        for color, score in ScoringService.sort_scores(scores):
            rows.append(f"• {STYLE_LABELS[color]}: <b>{score}/100</b> ({ScoringService.get_level(score)})")
        return "\n".join(rows)

    @staticmethod
    def generate_universal_result(scores: dict) -> str:
        profile_info = ScoringService.get_profile_key(scores)
        profile_key = profile_info["profile_key"]
        profile_type = profile_info["profile_type"]
        lowest_style = profile_info["lowest_style"]
        lowest_score = profile_info["lowest_score"]

        if profile_type == "mixed":
            title = MIXED_PROFILE_NAMES[profile_key]
            description = MIXED_PROFILE_DESCRIPTIONS[profile_key]
            kind = "Смешанный профиль"
        else:
            title = PROFILE_NAMES[profile_key]
            description = SINGLE_PROFILE_DESCRIPTIONS[profile_key]
            kind = "Основной профиль"

        result = [
            "✨ <b>Ваш результат Behavior Compass</b>",
            "",
            f"<b>{kind}: {title}</b>",
            description,
            "",
            "<b>Баллы по стилям</b>",
            ScoringService.generate_score_table(scores),
            "",
            (
                "Если разница между двумя ведущими стилями 10 баллов или меньше, "
                "результат считается смешанным: оба стиля реально влияют на поведение."
            ),
            "",
            f"<b>Самый низкий стиль:</b> {STYLE_LABELS[lowest_style]} - {lowest_score}/100.",
        ]

        if lowest_score <= 30:
            result.extend(["", LOWEST_STYLE_BLOCKS[lowest_style]])

        result.extend([
            "",
            "Главная мысль: это не ярлык, а рабочая карта поведения. Ее смысл - понять, где вы сильны, где можете перегибать, и какой стиль стоит включать осознанно.",
        ])

        return "\n".join(result)

    @staticmethod
    def generate_context_result(scores: dict, context: str) -> str:
        profile_key = ScoringService.get_profile_key(scores)["profile_key"]
        context_blocks = CONTEXT_BLOCKS.get(context)
        if not context_blocks:
            return "Контекст не найден. Выберите один из предложенных вариантов."
        return context_blocks[profile_key]

    @staticmethod
    def generate_result(scores: dict, context: str = None) -> str:
        if context:
            return ScoringService.generate_context_result(scores, context)
        return ScoringService.generate_universal_result(scores)

    @staticmethod
    def get_profile_description(language: str, color: str) -> dict:
        return {
            "name": PROFILE_NAMES.get(color, color),
            "description": SINGLE_PROFILE_DESCRIPTIONS.get(color, ""),
        }

    @staticmethod
    def validate_profile_blocks() -> None:
        missing_single = REQUIRED_SINGLE_PROFILE_KEYS - set(SINGLE_PROFILE_DESCRIPTIONS)
        missing_mixed = REQUIRED_MIXED_PROFILE_KEYS - set(MIXED_PROFILE_DESCRIPTIONS)
        missing_lowest = REQUIRED_SINGLE_PROFILE_KEYS - set(LOWEST_STYLE_BLOCKS)

        if missing_single:
            raise ValueError(f"Missing single profile descriptions: {sorted(missing_single)}")
        if missing_mixed:
            raise ValueError(f"Missing mixed profile descriptions: {sorted(missing_mixed)}")
        if missing_lowest:
            raise ValueError(f"Missing lowest style blocks: {sorted(missing_lowest)}")

        for context_name, blocks in CONTEXT_BLOCKS.items():
            missing = REQUIRED_PROFILE_KEYS - set(blocks)
            if missing:
                raise ValueError(f"Missing {context_name} blocks: {sorted(missing)}")


ScoringService.validate_profile_blocks()
