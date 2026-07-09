"""Scoring and profile result generation for Behavior Compass."""

BLUE_QUESTIONS = [2, 6, 10, 14, 18]
GREEN_QUESTIONS = [3, 7, 11, 15, 19]
YELLOW_QUESTIONS = [1, 4, 8, 12, 16, 20]
RED_QUESTIONS = [0, 5, 9, 13, 17, 21, 22, 23]

COLORS = ("red", "yellow", "blue", "green")
MIXED_THRESHOLD = 10

COLOR_META = {
    "red": {
        "emoji": "🔴",
        "name": "Красный",
        "role": "Результат / Действие",
        "verb": "действовать, решать и влиять на результат",
    },
    "yellow": {
        "emoji": "🟡",
        "name": "Жёлтый",
        "role": "Влияние / Энергия",
        "verb": "общаться, вдохновлять и вовлекать людей",
    },
    "blue": {
        "emoji": "🔵",
        "name": "Синий",
        "role": "Анализ / Структура",
        "verb": "анализировать, структурировать и проверять качество",
    },
    "green": {
        "emoji": "🟢",
        "name": "Зелёный",
        "role": "Стабильность / Поддержка",
        "verb": "поддерживать, стабилизировать и сохранять отношения",
    },
}

REQUIRED_SINGLE_PROFILE_KEYS = set(COLORS)
REQUIRED_MIXED_PROFILE_KEYS = {
    f"{primary}_{secondary}"
    for primary in COLORS
    for secondary in COLORS
    if primary != secondary
}
REQUIRED_PROFILE_KEYS = REQUIRED_SINGLE_PROFILE_KEYS | REQUIRED_MIXED_PROFILE_KEYS

MIXED_PROFILE_TITLES = {
    "red_yellow": "Драйвер-вдохновитель",
    "red_blue": "Стратег-результатник",
    "red_green": "Ответственный лидер",
    "yellow_red": "Энергичный инициатор",
    "yellow_green": "Коммуникатор-поддержка",
    "yellow_blue": "Убедительный объяснитель",
    "blue_red": "Аналитик-решатель",
    "blue_green": "Надёжный систематизатор",
    "blue_yellow": "Эксперт-коммуникатор",
    "green_blue": "Спокойный организатор",
    "green_yellow": "Тёплый коммуникатор",
    "green_red": "Мягкий координатор",
}

MIXED_ONE_LINERS = {
    "red_yellow": "быстро действует и умеет вовлекать",
    "red_blue": "решает быстро, но опирается на логику",
    "red_green": "ведёт к цели, но учитывает людей",
    "yellow_red": "зажигает и продвигает",
    "yellow_green": "создаёт атмосферу и связи",
    "yellow_blue": "доносит идеи структурно",
    "blue_red": "видит систему и двигает к результату",
    "blue_green": "соединяет точность, стабильность и качество",
    "blue_yellow": "объясняет сложное понятно",
    "green_blue": "держит порядок, надёжность и поддержку",
    "green_yellow": "создаёт контакт, эмпатию и атмосферу",
    "green_red": "держит людей и задачу вместе",
}

PRIMARY_SUMMARIES = {
    "red": "Вы быстро включаетесь, берёте инициативу, любите движение, ясные решения и конкретный результат.",
    "yellow": "Вы легко входите в контакт, создаёте энергию вокруг идеи и умеете вовлекать людей в движение.",
    "blue": "Вы стремитесь понять логику, структуру и качество решения, прежде чем двигаться дальше.",
    "green": "Вы цените устойчивость, доверие, спокойный ритм и бережное отношение к людям.",
}

SECONDARY_SUMMARIES = {
    "red": "Красный добавляет напор, решительность и готовность продвигать ситуацию к результату.",
    "yellow": "Жёлтый добавляет общительность, энергию, живой контакт и способность заражать людей идеей.",
    "blue": "Синий добавляет рациональность, внимание к фактам, структуре и качеству решения.",
    "green": "Зелёный добавляет терпение, поддержку, устойчивость и внимание к состоянию людей.",
}

LOWEST_STYLE_BLOCKS = {
    "red": "Низкий Красный может означать, что вам сложнее быстро брать власть, жёстко расставлять приоритеты и продавливать решение в неопределённости.",
    "yellow": "Низкий Жёлтый может означать, что вам сложнее быстро создавать лёгкий контакт, публичную энергию и эмоциональное вовлечение.",
    "blue": "Низкий Синий может означать, что в скорости вы иногда пропускаете проверку фактов, структуру и спокойный анализ деталей.",
    "green": "Низкий Зелёный может означать, что вам не всегда легко ждать, сглаживать острые углы, подстраиваться под чужой темп и сохранять спокойствие в затянутых обсуждениях.",
}

ACTION_BLOCKS = {
    "red": "Вы быстро включаетесь в задачу, берёте инициативу и стараетесь довести ситуацию до результата. Вам комфортнее там, где есть движение, ответственность и возможность влиять на ход событий.",
    "yellow": "Вы чаще начинаете с контакта, идеи и эмоционального включения. Вам важно оживить ситуацию, найти интерес и подключить людей к разговору или задаче.",
    "blue": "Вы обычно начинаете с понимания системы: что известно, где риски, какие факты важны и по каким критериям принимать решение.",
    "green": "Вы стараетесь удерживать стабильность, рабочий ритм и отношения. Вам важно, чтобы движение вперёд не разрушало доверие и спокойствие людей.",
}

STRENGTHS = {
    "red": ["быстро принимаете решения", "не боитесь ответственности", "двигаете процесс вперёд", "говорите прямо и по существу"],
    "yellow": ["легко устанавливаете контакт", "заряжаете людей энергией", "видите возможности", "умеете оживлять разговор"],
    "blue": ["видите структуру", "замечаете риски", "опираетесь на факты", "умеете объяснять сложное через логику"],
    "green": ["создаёте доверие", "удерживаете спокойствие", "поддерживаете людей", "помогаете команде не рассыпаться"],
}

RISKS = {
    "red": ["торопить собеседника", "слишком быстро переходить к решению", "звучать жёстче, чем планировали", "недооценивать эмоции и сомнения других"],
    "yellow": ["перескакивать между идеями", "терять фокус на деталях", "обещать быстрее, чем система готова выполнить", "уходить в эмоцию вместо решения"],
    "blue": ["затягивать анализ", "звучать чрезмерно критично", "терять контакт из-за деталей", "откладывать действие до полной ясности"],
    "green": ["избегать конфликта", "слишком долго терпеть неопределённость", "медлить с жёстким решением", "сглаживать проблему вместо прямого разговора"],
}

COMMUNICATION = {
    "red": "С вами лучше говорить ясно, прямо и по делу: цель, проблема, варианты, решение и следующий шаг. Длинные объяснения без движения могут раздражать.",
    "yellow": "С вами лучше говорить живо, открыто и через идею. Вам важны контакт, интерес и ощущение, что в разговоре есть энергия.",
    "blue": "С вами лучше говорить структурно: факты, логика, критерии, риски и вывод. Вам важно понимать, почему решение выглядит разумным.",
    "green": "С вами лучше говорить спокойно и уважительно. Вам важно видеть, что решение учитывает людей, отношения и устойчивость процесса.",
}

IRRITANTS = {
    "red": "медленный темп, бесконечные обсуждения, отсутствие решения, пассивность и фразы вроде «давайте ещё подумаем», когда вам уже всё ясно",
    "yellow": "сухость, холодная критика, запрет на идеи, отсутствие контакта и разговор только через ограничения",
    "blue": "хаос, эмоциональное давление, слабая аргументация, неточные данные и решения «на ощущениях»",
    "green": "резкость, давление, постоянная срочность, конфликт ради конфликта и игнорирование человеческого состояния",
}

SALES = {
    "red": "В продажах ваш стиль помогает уверенно вести разговор, держать фокус на результате и продвигать клиента к решению. Риск — начать вести клиента быстрее, чем он готов двигаться.",
    "yellow": "В продажах ваш стиль помогает быстро устанавливать контакт, оживлять интерес и показывать ценность через живую коммуникацию. Риск — увлечься презентацией и потерять следующий шаг.",
    "blue": "В продажах ваш стиль помогает работать с аргументами, возражениями, цифрами и рациональным обоснованием. Риск — перегрузить клиента деталями до того, как он эмоционально готов слушать.",
    "green": "В продажах ваш стиль помогает строить доверие, сопровождать клиента и развивать долгие отношения. Риск — слишком мягко вести к решению и поздно закрывать следующий шаг.",
}

NEGOTIATIONS = {
    "red": "В переговорах вы сильны за счёт уверенности, скорости реакции и ориентации на результат. Риск — слишком рано начать давить или воспринимать паузу другой стороны как сопротивление.",
    "yellow": "В переговорах вы сильны за счёт контакта, гибкости и умения создавать позитивную динамику. Риск — уступить структуру ради хорошей атмосферы.",
    "blue": "В переговорах вы сильны за счёт подготовки, логики и точных аргументов. Риск — выглядеть холодно или спорить с эмоцией через факты.",
    "green": "В переговорах вы сильны за счёт спокойствия, терпения и доверия. Риск — избегать жёстких условий, когда их важно обозначить.",
}

TEAM = {
    "red": "В команде вы помогаете не застревать: берёте ответственность, задаёте направление и требуете результата. Важно помнить, что не все медлят из сопротивления: иногда люди проверяют риски.",
    "yellow": "В команде вы создаёте энергию, атмосферу и движение вокруг идеи. Важно помогать группе фиксировать договорённости, чтобы вдохновение превращалось в результат.",
    "blue": "В команде вы приносите порядок, качество и способность видеть слабые места решения. Важно добавлять поддержку, чтобы ваша точность не считывалась как холодная критика.",
    "green": "В команде вы удерживаете доверие, спокойствие и рабочий ритм. Важно не откладывать прямой разговор, если проблема уже мешает результату.",
}

STRESS = {
    "red": "В стрессе вы можете становиться более резким, быстрым и требовательным. Проверяйте себя: вы сейчас ведёте людей или просто усиливаете давление?",
    "yellow": "В стрессе вы можете ускоряться, перескакивать между идеями и искать быстрый эмоциональный выход. Помогает короткий список из трёх конкретных действий.",
    "blue": "В стрессе вы можете уходить в анализ и контроль деталей. Помогает ограничить время на проверку и выбрать рабочую версию решения.",
    "green": "В стрессе вы можете замедляться, избегать конфликта и ждать, пока напряжение спадёт само. Помогает назвать проблему прямо и выбрать первый маленький шаг.",
}

ADVICE = {
    "red": "Перед тем как продвигать решение, задайте один вопрос: «Что для вас сейчас важно учесть, чтобы принять решение уверенно?» Это сохраняет вашу силу, но снижает ощущение давления.",
    "yellow": "После идеи сразу фиксируйте следующий шаг: кто делает, когда и как поймём, что готово. Это превращает энергию в результат.",
    "blue": "Перед длинным анализом спросите себя: «Какое решение уже достаточно надёжно для первого шага?» Это помогает не застревать в деталях.",
    "green": "Когда чувствуете напряжение, задайте прямой вопрос мягким тоном: «Что сейчас мешает нам двигаться дальше?» Это сохраняет уважение и добавляет ясность.",
}


def color_label(color: str) -> str:
    meta = COLOR_META[color]
    return f"{meta['emoji']} {meta['name']}"


def pair_title(primary: str, secondary: str) -> str:
    key = f"{primary}_{secondary}"
    return MIXED_PROFILE_TITLES.get(key, f"{COLOR_META[primary]['name']}-{COLOR_META[secondary]['name']} профиль")


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
            return "выражен слабо"
        if score <= 50:
            return "проявляется ситуативно"
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

        if all(45 <= score <= 60 for score in scores.values()):
            profile_type = "balanced"
            profile_key = f"{primary_style}_{secondary_style}"
        elif difference <= MIXED_THRESHOLD:
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
            rows.append(f"{color_label(color)}: <b>{score}/100</b> — {ScoringService.get_level(score)}")
        return "\n".join(rows)

    @staticmethod
    def generate_universal_result(scores: dict) -> str:
        info = ScoringService.get_profile_key(scores)
        primary = info["primary_style"]
        secondary = info["secondary_style"]
        lowest = info["lowest_style"]
        key = f"{primary}_{secondary}"

        if info["profile_type"] == "balanced":
            title = "Сбалансированный / адаптивный профиль"
            profile_line = (
                "Ваши стили расположены близко друг к другу. Это похоже не на один яркий цвет, "
                "а на адаптивный рисунок поведения: вы можете переключаться между разными способами действия."
            )
        elif info["profile_type"] == "mixed":
            title = f"{COLOR_META[primary]['name']}-{COLOR_META[secondary]['name']} профиль: {pair_title(primary, secondary)}"
            profile_line = (
                f"Это не просто {COLOR_META[primary]['name']} профиль. Это связка "
                f"{color_label(primary)} + {color_label(secondary)}: {MIXED_ONE_LINERS[key]}."
            )
        else:
            title = f"{COLOR_META[primary]['name']} профиль с выраженным вторым стилем"
            profile_line = (
                f"Ведущий стиль заметно выше остальных, но второй стиль тоже важен: "
                f"он показывает, как именно проявляется ваш основной способ действия."
            )

        return "\n".join([
            "✨ 🎯 <b>Ваш результат Behavior Compass</b>",
            "",
            f"<b>{title}</b>",
            "",
            f"<b>Ведущий стиль:</b> {color_label(primary)} — {COLOR_META[primary]['role']}",
            f"<b>Дополнительный стиль:</b> {color_label(secondary)} — {COLOR_META[secondary]['role']}",
            "",
            "<b>Ваш профиль:</b>",
            ScoringService.generate_score_table(scores),
            "",
            "<b>Кратко:</b>",
            f"{PRIMARY_SUMMARIES[primary]} {SECONDARY_SUMMARIES[secondary]}",
            "",
            profile_line,
            "",
            f"<b>Зона внимания:</b> {color_label(lowest)} — {scores[lowest]}/100.",
            LOWEST_STYLE_BLOCKS[lowest],
            "",
            "<b>Главная мысль:</b> ваша сила — это не ярлык, а рабочий способ поведения. Ниже можно открыть подробный разбор: сила, риски, коммуникация, продажи, переговоры, команда, стресс и совет.",
        ])

    @staticmethod
    def generate_detailed_result(scores: dict) -> str:
        info = ScoringService.get_profile_key(scores)
        primary = info["primary_style"]
        secondary = info["secondary_style"]
        lowest = info["lowest_style"]

        return "\n".join([
            "📌 <b>Подробный разбор профиля</b>",
            "",
            "<b>Как вы обычно действуете</b>",
            ACTION_BLOCKS[primary],
            SECONDARY_SUMMARIES[secondary],
            "",
            "<b>Ваши сильные стороны</b>",
            ScoringService.generate_context_result(scores, "strengths"),
            "",
            "<b>Возможные риски</b>",
            ScoringService.generate_context_result(scores, "risks"),
            "",
            f"<b>Самый низкий стиль:</b> {color_label(lowest)}",
            LOWEST_STYLE_BLOCKS[lowest],
        ])

    @staticmethod
    def generate_context_result(scores: dict, context: str) -> str:
        info = ScoringService.get_profile_key(scores)
        primary = info["primary_style"]
        secondary = info["secondary_style"]

        if context == "detailed":
            return ScoringService.generate_detailed_result(scores)
        if context == "strengths":
            items = STRENGTHS[primary] + STRENGTHS[secondary][:2]
            return "💪 <b>Мои сильные стороны</b>\n\n" + "\n".join(f"• {item}" for item in items)
        if context == "risks":
            items = RISKS[primary] + RISKS[secondary][:2]
            return "⚠️ <b>Мои риски</b>\n\n" + "\n".join(f"• {item}" for item in items) + "\n\nЭто не «плохо». Это зона внимания: сила становится риском, когда её слишком много."
        if context == "communication":
            return f"💬 <b>Как со мной общаться</b>\n\n{COMMUNICATION[primary]}\n\n{SECONDARY_SUMMARIES[secondary]}\n\n<b>Что может раздражать:</b> {IRRITANTS[primary]}."
        if context == "sales":
            return f"💼 <b>Я в продажах</b>\n\n{SALES[primary]}\n\nС учётом второго стиля: {SECONDARY_SUMMARIES[secondary]}\n\nПолезная формула: сначала понять темп клиента — потом ускорять решение."
        if context == "negotiations":
            return f"🤝 <b>Я в переговорах</b>\n\n{NEGOTIATIONS[primary]}\n\nВторой стиль добавляет нюанс: {SECONDARY_SUMMARIES[secondary]}"
        if context == "team":
            return f"👥 <b>Я в команде</b>\n\n{TEAM[primary]}\n\nВторой стиль добавляет нюанс: {SECONDARY_SUMMARIES[secondary]}"
        if context == "stress":
            return f"🔥 <b>В стрессе</b>\n\n{STRESS[primary]}\n\nПроверочный вопрос: вы сейчас действительно ведёте людей или просто усиливаете давление?"
        if context == "advice":
            return f"🚀 <b>Совет по развитию</b>\n\n{ADVICE[primary]}\n\nГлавная задача — не ломать свой стиль, а расширять диапазон поведения."

        return "Контекст не найден. Выберите один из предложенных вариантов."

    @staticmethod
    def generate_result(scores: dict, context: str = None) -> str:
        if context:
            return ScoringService.generate_context_result(scores, context)
        return ScoringService.generate_universal_result(scores)

    @staticmethod
    def get_profile_description(language: str, color: str) -> dict:
        return {
            "name": f"{color_label(color)} — {COLOR_META[color]['role']}",
            "description": PRIMARY_SUMMARIES[color],
        }

    @staticmethod
    def validate_profile_blocks() -> None:
        missing_mixed = REQUIRED_MIXED_PROFILE_KEYS - set(MIXED_PROFILE_TITLES)
        if missing_mixed:
            raise ValueError(f"Missing mixed profile titles: {sorted(missing_mixed)}")

        for mapping_name, mapping in {
            "PRIMARY_SUMMARIES": PRIMARY_SUMMARIES,
            "SECONDARY_SUMMARIES": SECONDARY_SUMMARIES,
            "LOWEST_STYLE_BLOCKS": LOWEST_STYLE_BLOCKS,
            "ACTION_BLOCKS": ACTION_BLOCKS,
            "STRENGTHS": STRENGTHS,
            "RISKS": RISKS,
            "COMMUNICATION": COMMUNICATION,
            "IRRITANTS": IRRITANTS,
            "SALES": SALES,
            "NEGOTIATIONS": NEGOTIATIONS,
            "TEAM": TEAM,
            "STRESS": STRESS,
            "ADVICE": ADVICE,
        }.items():
            missing = REQUIRED_SINGLE_PROFILE_KEYS - set(mapping)
            if missing:
                raise ValueError(f"Missing {mapping_name}: {sorted(missing)}")


ScoringService.validate_profile_blocks()
