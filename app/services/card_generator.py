"""Сервис генерации красивой PNG карточки результата"""

from PIL import Image, ImageDraw, ImageFont
import math
import os
from pathlib import Path
from datetime import datetime


class CardGenerationService:
    COLORS = {
        "blue":   (52, 152, 219),
        "green":  (46, 204, 113),
        "yellow": (241, 196, 15),
        "red":    (231, 76, 60),
    }
    COLOR_NAMES = {
        "ru": {"blue": "ДОВЕРИТЕЛЬНЫЙ", "green": "АНАЛИТИЧЕСКИЙ", "yellow": "КОММУНИКАТИВНЫЙ", "red": "РЕЗУЛЬТАТИВНЫЙ"},
        "en": {"blue": "EMPATHETIC",    "green": "ANALYTICAL",    "yellow": "ENTHUSIAST",      "red": "LEADER"},
        "uz": {"blue": "ISHONCHLI",     "green": "ANALITIK",      "yellow": "MULOQOTCHI",      "red": "NATIJAVIY"},
        "de": {"blue": "EINFÜHLSAM",    "green": "ANALYTISCH",    "yellow": "ENTHUSIAST",      "red": "FÜHRUNGSSTARK"},
        "tr": {"blue": "GÜVENİLİR",     "green": "ANALİTİK",      "yellow": "İLETİŞİMCİ",      "red": "SONUÇ ODAKLI"},
    }
    STRENGTHS = {
        "ru": {
            "blue":   ["Умеете слушать и понимать", "Поддерживаете команду", "Ценит отношения и доверие", "Создает гармонию в коллективе", "Надежный и верный"],
            "green":  ["Анализируете ситуацию", "Принимаете обоснованные решения", "Ставите цели и достигаете их", "Стремитесь к качеству", "Ответственны и надежны"],
            "yellow": ["Вдохновляете окружающих", "Генерируете идеи", "Нестандартный подход", "Создаете позитивную атмосферу", "Энергичный и оптимистичный"],
            "red":    ["Принимаете решения быстро", "Берете на себя ответственность", "Ведете команду к цели", "Нацелены на результат", "Уверенный и настойчивый"],
        },
        "en": {
            "blue":   ["Excellent listener", "Supports the team", "Values relationships", "Creates harmony", "Reliable and loyal"],
            "green":  ["Analytical thinking", "Informed decisions", "Sets and achieves goals", "Quality-focused", "Responsible"],
            "yellow": ["Inspires others", "Generates ideas", "Creative problem solver", "Positive atmosphere", "Energetic"],
            "red":    ["Fast decision-maker", "Takes responsibility", "Leads team to goals", "Results-oriented", "Confident"],
        },
        "uz": {
            "blue":   ["Yaxshi tinglovchi", "Jamoani qo'llab-quvvatlaydi", "Munosabatlarni qadrlaydi", "Uyg'unlik yaratadi", "Ishonchli"],
            "green":  ["Tahliliy fikrlash", "Asosli qarorlar", "Maqsad qo'yadi", "Sifatga e'tibor", "Mas'uliyatli"],
            "yellow": ["Ilhomlantiradi", "G'oyalar yaratadi", "Ijodiy yechimlar", "Ijobiy muhit", "Faol"],
            "red":    ["Tez qaror qabul qiladi", "Mas'uliyat oladi", "Jamoani boshqaradi", "Natijaga yo'naltirilgan", "Qat'iyatli"],
        },
        "de": {
            "blue":   ["Ausgezeichneter Zuhörer", "Unterstützt das Team", "Schätzt Beziehungen", "Schafft Harmonie", "Zuverlässig"],
            "green":  ["Analytisches Denken", "Fundierte Entscheidungen", "Ziele erreichen", "Qualitätsorientiert", "Verantwortlich"],
            "yellow": ["Inspiriert andere", "Generiert Ideen", "Kreative Lösungen", "Positive Atmosphäre", "Energetisch"],
            "red":    ["Schnelle Entscheidungen", "Übernimmt Verantwortung", "Führt zum Ziel", "Ergebnisorientiert", "Selbstbewusst"],
        },
        "tr": {
            "blue":   ["Mükemmel dinleyici", "Ekibi destekler", "İlişkilere değer verir", "Uyum yaratır", "Güvenilir"],
            "green":  ["Analitik düşünce", "Bilinçli kararlar", "Hedeflere ulaşır", "Kalite odaklı", "Sorumlu"],
            "yellow": ["Başkalarını ilhamlandırır", "Fikir üretir", "Yaratıcı çözümler", "Pozitif atmosfer", "Enerjik"],
            "red":    ["Hızlı karar verir", "Sorumluluk alır", "Ekibi yönlendirir", "Sonuç odaklı", "Özgüvenli"],
        },
    }
    GROWTH_ZONES = {
        "ru": {
            "blue":   ["Умение говорить 'нет'", "Принятие трудных решений", "Уверенность в себе", "Расстановка приоритетов"],
            "green":  ["Делегирование и доверие", "Гибкость в неопределенности", "Внимание к эмоциям людей", "Снижение перфекционизма"],
            "yellow": ["Следование плану", "Доведение дел до конца", "Структурирование работы", "Фокус на одной задаче"],
            "red":    ["Умение слушать других", "Учет чужих эмоций", "Терпение и гибкость", "Работа в команде"],
        },
        "en": {
            "blue":   ["Saying 'no' when needed", "Making tough decisions", "Self-confidence", "Setting priorities"],
            "green":  ["Delegating and trusting", "Flexibility in uncertainty", "Attention to emotions", "Reducing perfectionism"],
            "yellow": ["Following plans", "Completing tasks", "Structuring work", "Focus on one task"],
            "red":    ["Listening to others", "Considering emotions", "Patience and flexibility", "Teamwork"],
        },
        "uz": {
            "blue":   ["'Yo'q' deyishni o'rganish", "Qiyin qarorlar", "O'ziga ishonch", "Ustuvorliklarni belgilash"],
            "green":  ["Vazifalami topshirish", "Moslashuvchanlik", "Hissiyotlarga e'tibor", "Perfeksionizmni kamaytirish"],
            "yellow": ["Rejaga amal qilish", "Ishlarni tugallash", "Ishni tuzilmalashtirish", "Bitta vazifaga e'tibor"],
            "red":    ["Boshqalarni tinglash", "Hissiyotlarni hisobga olish", "Sabr", "Jamoada ishlash"],
        },
        "de": {
            "blue":   ["'Nein' sagen können", "Schwierige Entscheidungen", "Selbstvertrauen", "Prioritäten setzen"],
            "green":  ["Delegieren und vertrauen", "Flexibilität", "Aufmerksamkeit für Emotionen", "Perfektionismus reduzieren"],
            "yellow": ["Plänen folgen", "Aufgaben abschließen", "Arbeit strukturieren", "Fokus auf eine Aufgabe"],
            "red":    ["Anderen zuhören", "Emotionen berücksichtigen", "Geduld", "Teamarbeit"],
        },
        "tr": {
            "blue":   ["'Hayır' diyebilmek", "Zor kararlar", "Özgüven", "Öncelikleri belirlemek"],
            "green":  ["Görevleri devretmek", "Esneklik", "Duygulara dikkat", "Mükemmeliyetçiliği azaltmak"],
            "yellow": ["Plana uymak", "Görevleri tamamlamak", "İşi yapılandırmak", "Tek göreve odaklanmak"],
            "red":    ["Başkalarını dinlemek", "Duyguları dikkate almak", "Sabır", "Takım çalışması"],
        },
    }
    COMBO_TEXTS = {
        "ru": {
            ("blue","green"):   ("Эмпатичный Аналитик",    "Вы сочетаете глубокое понимание людей с аналитическим мышлением."),
            ("blue","yellow"):  ("Вдохновляющий Дипломат",  "Вы умеете вдохновлять, создавая теплую и оптимистичную атмосферу."),
            ("blue","red"):     ("Командный Лидер",          "Вы ведете за собой, не теряя человеческого подхода."),
            ("green","blue"):   ("Аналитик + Дипломат",      "Вы сочетаете логику с эмпатией. Обдуманные решения с заботой о людях."),
            ("green","yellow"): ("Креативный Стратег",       "Вы видите картину целиком и генерируете свежие идеи."),
            ("green","red"):    ("Аналитик + Результативный","Вы сочетаете аналитическое мышление с ориентацией на результат."),
            ("yellow","blue"):  ("Энергичный Миротворец",    "Вы создаете радость, тонко чувствуя людей."),
            ("yellow","green"): ("Творческий Аналитик",      "Вы умеете генерировать идеи и анализировать их реалистичность."),
            ("yellow","red"):   ("Энергичный Лидер",         "Вы заряжаете энергией и ведете за собой."),
            ("red","blue"):     ("Лидер с Сердцем",          "Вы принимаете быстрые решения, сохраняя заботу о людях."),
            ("red","green"):    ("Стратегический Лидер",     "Вы принимаете решения на основе данных и движетесь к цели."),
            ("red","yellow"):   ("Харизматичный Лидер",      "Вы ведете через вдохновение. Ваш энтузиазм заразителен."),
        },
        "en": {
            ("blue","green"):   ("Empathetic Analyst",   "You combine deep understanding of people with analytical thinking."),
            ("blue","yellow"):  ("Inspiring Diplomat",   "You inspire people while creating a warm and optimistic atmosphere."),
            ("blue","red"):     ("Team Leader",          "You lead without losing the human touch. Decisive yet caring."),
            ("green","blue"):   ("Analyst + Diplomat",   "You combine logic with empathy. Thoughtful decisions considering people."),
            ("green","yellow"): ("Creative Strategist",  "You see the big picture and generate fresh ideas."),
            ("green","red"):    ("Analytical Leader",    "You combine analytical thinking with a results orientation."),
            ("yellow","blue"):  ("Energetic Peacemaker", "You create joy while deeply sensing people."),
            ("yellow","green"): ("Creative Analyst",     "You generate ideas and analyze their feasibility."),
            ("yellow","red"):   ("Energetic Leader",     "You energize and lead. Your charisma opens doors."),
            ("red","blue"):     ("Leader with Heart",    "You make fast decisions without losing care for people."),
            ("red","green"):    ("Strategic Leader",     "You make data-driven decisions and move toward goals."),
            ("red","yellow"):   ("Charismatic Leader",   "You lead through inspiration. Your enthusiasm is contagious."),
        },
        "uz": {
            ("blue","green"):   ("Empatik Analitik",   "Odamlarni tushunish va analitik fikrlashni uyg'unlashtirasiz."),
            ("blue","yellow"):  ("Ilhomlovchi Diplomat","Iliq va optimistik muhit yaratib ilhomlantira olasiz."),
            ("blue","red"):     ("Jamoa Yetakchisi",    "Insoniy yondashuvni yo'qotmasdan yetakchilasiz."),
            ("green","blue"):   ("Analitik + Diplomat", "Mantiq va empatiyani uyg'unlashtirasiz."),
            ("green","yellow"): ("Ijodiy Strateg",      "Katta rasmni ko'rasiz va yangi g'oyalar yaratasiz."),
            ("green","red"):    ("Analitik Yetakchi",   "Analitik fikrlash va natijaga yo'naltirilganlikni uyg'unlashtirasiz."),
            ("yellow","blue"):  ("Faol Tinchlikchi",    "Odamlarni his qilgan holda quvonch yaratasiz."),
            ("yellow","green"): ("Ijodiy Analitik",     "G'oyalar yaratasiz va ularning real ekanligini tahlil qilasiz."),
            ("yellow","red"):   ("Faol Yetakchi",       "Energiya berasiz va yetaklaysiz."),
            ("red","blue"):     ("Yurakli Yetakchi",    "Odamlarga g'amxo'rlikni yo'qotmasdan tez qarorlar qabul qilasiz."),
            ("red","green"):    ("Strategik Yetakchi",  "Ma'lumotlarga asoslanib qaror qabul qilasiz."),
            ("red","yellow"):   ("Xarizmali Yetakchi",  "Ilhom orqali yetaklaysiz. Entuziazmingiz yuqumli."),
        },
        "de": {
            ("blue","green"):   ("Empathischer Analytiker", "Sie verbinden tiefes Menschenverständnis mit analytischem Denken."),
            ("blue","yellow"):  ("Inspirierender Diplomat",  "Sie inspirieren Menschen und schaffen eine warme Atmosphäre."),
            ("blue","red"):     ("Teamleader",               "Sie führen ohne den menschlichen Ansatz zu verlieren."),
            ("green","blue"):   ("Analytiker + Diplomat",    "Sie kombinieren Logik mit Empathie."),
            ("green","yellow"): ("Kreativer Stratege",       "Sie sehen das große Bild und generieren frische Ideen."),
            ("green","red"):    ("Analytischer Leiter",      "Sie kombinieren analytisches Denken mit Ergebnisorientierung."),
            ("yellow","blue"):  ("Energetischer Friedensstifter", "Sie schaffen Freude und spüren Menschen tief."),
            ("yellow","green"): ("Kreativer Analytiker",     "Sie generieren Ideen und analysieren deren Realisierbarkeit."),
            ("yellow","red"):   ("Energetischer Leiter",     "Sie laden mit Energie auf und führen."),
            ("red","blue"):     ("Leiter mit Herz",          "Sie treffen schnelle Entscheidungen ohne Fürsorge zu verlieren."),
            ("red","green"):    ("Strategischer Leiter",     "Sie treffen datenbasierte Entscheidungen."),
            ("red","yellow"):   ("Charismatischer Leiter",   "Sie führen durch Inspiration. Ihr Enthusiasmus ist ansteckend."),
        },
        "tr": {
            ("blue","green"):   ("Empatik Analist",      "İnsanları derinlemesine anlama ve analitik düşünceyi birleştiriyorsunuz."),
            ("blue","yellow"):  ("İlham Veren Diplomat",  "İnsanları ilhamlandırırken sıcak bir atmosfer yaratıyorsunuz."),
            ("blue","red"):     ("Takım Lideri",          "İnsani yaklaşımı kaybetmeden liderlik ediyorsunuz."),
            ("green","blue"):   ("Analist + Diplomat",    "Mantığı empatiyle birleştiriyorsunuz."),
            ("green","yellow"): ("Yaratıcı Stratejist",   "Büyük resmi görüyor ve yeni fikirler üretiyorsunuz."),
            ("green","red"):    ("Analitik Lider",        "Analitik düşünce ile sonuç odaklılığı birleştiriyorsunuz."),
            ("yellow","blue"):  ("Enerjik Barışçı",       "İnsanları derinlemesine hissederek neşe yaratıyorsunuz."),
            ("yellow","green"): ("Yaratıcı Analist",      "Fikir üretiyor ve gerçekçiliklerini analiz ediyorsunuz."),
            ("yellow","red"):   ("Enerjik Lider",         "Enerji veriyor ve liderlik ediyorsunuz."),
            ("red","blue"):     ("Kalpli Lider",          "İnsanlara özen göstermeyi kaybetmeden hızlı kararlar alıyorsunuz."),
            ("red","green"):    ("Stratejik Lider",       "Veriye dayalı kararlar alıyor ve hedefe ilerliyorsunuz."),
            ("red","yellow"):   ("Karizmatik Lider",      "İlham yoluyla liderlik ediyorsunuz. Coşkunuz bulaşıcı."),
        },
    }

    @staticmethod
    def _load_font(size):
        candidates = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "arial.ttf",
        ]
        for path in candidates:
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
        return ImageFont.load_default()

    @staticmethod
    def _wrap(text, font, max_w):
        words = text.split()
        line, lines = "", []
        for w in words:
            test = (line + " " + w).strip()
            try:
                w_px = font.getlength(test)
            except Exception:
                w_px = len(test) * 8
            if w_px < max_w:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        return lines

    @staticmethod
    def generate_card(telegram_id: str, username: str, primary_color: str,
                      secondary_color: str, scores: dict, language: str = "ru") -> str:

        output_dir = Path("generated")
        output_dir.mkdir(exist_ok=True)

        W, H = 900, 1260
        BG          = (245, 246, 250)
        WHITE       = (255, 255, 255)
        DARK        = (25, 25, 35)
        GRAY        = (110, 120, 135)
        LIGHT_GRAY  = (220, 222, 228)
        ACCENT_BLUE = (41, 128, 185)

        img  = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)

        fBig   = CardGenerationService._load_font(34)
        fTitle = CardGenerationService._load_font(26)
        fMed   = CardGenerationService._load_font(20)
        fSm    = CardGenerationService._load_font(16)
        fTiny  = CardGenerationService._load_font(13)

        lang = language if language in CardGenerationService.COLOR_NAMES else "ru"

        def card(x1, y1, x2, y2, fill=WHITE, radius=10):
            draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=LIGHT_GRAY, width=1)

        # ─── HEADER ────────────────────────────────────────────────────────
        draw.rectangle([0, 0, W, 82], fill=ACCENT_BLUE)
        draw.text((22, 14), "BEHAVIOR COMPASS", font=fBig, fill=WHITE)
        draw.text((22, 56), "YOUR BEHAVIOR COMPASS PROFILE", font=fTiny, fill=(180, 210, 240))
        date_str = datetime.now().strftime("%d.%m.%Y")
        lbl = {"ru":"Дата:","en":"Date:","uz":"Sana:","de":"Datum:","tr":"Tarih:"}.get(lang,"Date:")
        draw.text((W-140, 22), lbl,     font=fTiny,  fill=(180,210,240))
        draw.text((W-140, 40), date_str, font=fSm,   fill=WHITE)

        # ─── ROW 1: PROFILE + PIE ──────────────────────────────────────────
        card(14, 92, W//2-6, 360)
        pl = {"ru":"ВАШ ПРОФИЛЬ","en":"YOUR PROFILE","uz":"PROFIL","de":"IHR PROFIL","tr":"PROFİLİNİZ"}.get(lang,"PROFILE")
        draw.text((30, 106), pl, font=fSm, fill=ACCENT_BLUE)

        cx, cy, r_out, r_in = 160, 240, 98, 46
        colors_order = ["red","green","yellow","blue"]
        total = sum(scores.get(c,0) for c in colors_order) or 1
        start = -90.0
        for color in colors_order:
            val   = scores.get(color, 0)
            sweep = val / total * 360
            rgb   = CardGenerationService.COLORS[color]
            thick = r_out - r_in
            for offset in range(0, thick, 2):
                r = r_out - offset
                box = [cx-r, cy-r, cx+r, cy+r]
                draw.arc(box, start=start, end=start+sweep-0.5, fill=rgb, width=3)
            start += sweep

        leg_x, leg_y = 280, 140
        for color in colors_order:
            pct  = round(scores.get(color,0) / total * 100)
            rgb  = CardGenerationService.COLORS[color]
            cname= CardGenerationService.COLOR_NAMES[lang][color]
            draw.rectangle([leg_x, leg_y+4, leg_x+14, leg_y+18], fill=rgb)
            draw.text((leg_x+20, leg_y), f"{pct}%", font=fSm, fill=rgb)
            draw.text((leg_x+58, leg_y), cname, font=fTiny, fill=DARK)
            leg_y += 32

        # Имя пользователя под диаграммой
        draw.text((30, 330), username, font=fMed, fill=DARK)

        # ─── ROW 1 RIGHT: COMBINATION ──────────────────────────────────────
        card(W//2+6, 92, W-14, 360)
        cl = {"ru":"ВАША КОМБИНАЦИЯ","en":"YOUR COMBINATION","uz":"KOMBINATSIYA","de":"KOMBINATION","tr":"KOMBİNASYON"}.get(lang,"COMBINATION")
        draw.text((W//2+22, 106), cl, font=fSm, fill=ACCENT_BLUE)

        pname = CardGenerationService.COLOR_NAMES[lang][primary_color]
        sname = CardGenerationService.COLOR_NAMES[lang][secondary_color]
        pc    = CardGenerationService.COLORS[primary_color]
        sc    = CardGenerationService.COLORS[secondary_color]
        draw.text((W//2+22, 140), pname, font=fMed, fill=pc)
        try:
            pw = fMed.getlength(pname)
        except Exception:
            pw = len(pname)*10
        draw.text((W//2+22+pw+10, 140), "+", font=fMed, fill=GRAY)
        draw.text((W//2+22, 170), sname, font=fMed, fill=sc)

        combo_src = CardGenerationService.COMBO_TEXTS.get(lang, CardGenerationService.COMBO_TEXTS.get("en", {}))
        combo_key = (primary_color, secondary_color)
        combo_title, combo_desc = combo_src.get(combo_key, ("", ""))
        if combo_title:
            draw.text((W//2+22, 208), combo_title, font=fSm, fill=DARK)
        for i, ln in enumerate(CardGenerationService._wrap(combo_desc, fTiny, W//2-44)[:4]):
            draw.text((W//2+22, 232+i*20), ln, font=fTiny, fill=GRAY)

        # ─── ROW 2: STRENGTHS + GROWTH ─────────────────────────────────────
        card(14,  370, W//2-6,  590)
        card(W//2+6, 370, W-14, 590)

        sl = {"ru":"СИЛЬНЫЕ СТОРОНЫ","en":"YOUR STRENGTHS","uz":"KUCHLI TOMONLAR","de":"STÄRKEN","tr":"GÜÇLÜ YÖNLER"}.get(lang,"STRENGTHS")
        gl = {"ru":"ЗОНЫ РАЗВИТИЯ","en":"GROWTH ZONES","uz":"RIVOJLANISH","de":"ENTWICKLUNG","tr":"GELİŞİM"}.get(lang,"GROWTH")
        draw.text((30, 384),         sl, font=fSm, fill=ACCENT_BLUE)
        draw.text((W//2+22, 384),    gl, font=fSm, fill=(210, 105, 30))

        strengths = CardGenerationService.STRENGTHS.get(lang, CardGenerationService.STRENGTHS["ru"]).get(primary_color, [])
        growth    = CardGenerationService.GROWTH_ZONES.get(lang, CardGenerationService.GROWTH_ZONES["ru"]).get(primary_color, [])

        for i, s in enumerate(strengths[:5]):
            draw.ellipse([30, 410+i*34, 40, 420+i*34], fill=(46,204,113))
            draw.text((50, 408+i*34), s, font=fTiny, fill=DARK)

        for i, g in enumerate(growth[:4]):
            draw.ellipse([W//2+22, 410+i*34, W//2+32, 420+i*34], fill=(241,196,15))
            draw.text((W//2+40, 408+i*34), g, font=fTiny, fill=DARK)

        # ─── ROW 3: INTENSITY ──────────────────────────────────────────────
        card(14, 600, W-14, 660)
        il = {"ru":"ИНТЕНСИВНОСТЬ ПРОФИЛЯ","en":"PROFILE INTENSITY","uz":"INTENSIVLIK","de":"INTENSITÄT","tr":"YOĞUNLUK"}.get(lang,"INTENSITY")
        draw.text((30, 612), il, font=fTiny, fill=GRAY)

        primary_score = scores.get(primary_color, 0)
        intensity = min(primary_score / 40.0, 1.0)
        bx1, by1, bx2, by2 = 30, 632, W-30, 648
        draw.rounded_rectangle([bx1,by1,bx2,by2], radius=6, fill=LIGHT_GRAY)
        fx = bx1 + int((bx2-bx1)*intensity)
        if fx > bx1:
            draw.rounded_rectangle([bx1,by1,fx,by2], radius=6, fill=ACCENT_BLUE)

        iv = {"ru":["Низкая","Средняя","Высокая"],"en":["Low","Medium","High"],
              "uz":["Past","O'rta","Yuqori"],"de":["Niedrig","Mittel","Hoch"],"tr":["Düşük","Orta","Yüksek"]}.get(lang,["Low","Med","High"])
        vw = iv[2] if intensity>0.7 else (iv[1] if intensity>0.4 else iv[0])
        draw.text((bx2+8, 630), vw, font=fTiny, fill=ACCENT_BLUE)

        # ─── ROW 4: SCORE BARS ─────────────────────────────────────────────
        card(14, 670, W-14, 830)
        sl2 = {"ru":"ВАШИ ПОКАЗАТЕЛИ","en":"YOUR SCORES","uz":"NATIJALAR","de":"IHRE WERTE","tr":"PUANLARINIZ"}.get(lang,"YOUR SCORES")
        draw.text((30, 684), sl2, font=fSm, fill=ACCENT_BLUE)

        bar_y = 712
        bar_max_w = W - 200
        for color in colors_order:
            val  = scores.get(color, 0)
            rgb  = CardGenerationService.COLORS[color]
            cname= CardGenerationService.COLOR_NAMES[lang][color]
            pct  = round(val/total*100)
            draw.text((30, bar_y), cname, font=fTiny, fill=DARK)
            bg_rect = [160, bar_y+2, 160+bar_max_w, bar_y+16]
            draw.rounded_rectangle(bg_rect, radius=4, fill=LIGHT_GRAY)
            fw = int(bar_max_w * (val/total))
            if fw > 0:
                draw.rounded_rectangle([160, bar_y+2, 160+fw, bar_y+16], radius=4, fill=rgb)
            draw.text((160+bar_max_w+10, bar_y), f"{pct}%", font=fTiny, fill=rgb)
            bar_y += 28

        # ─── FOOTER ────────────────────────────────────────────────────────
        draw.rectangle([0, H-86, W, H], fill=ACCENT_BLUE)
        ft = {"ru":"ВАШ КОМПАС НАПРАВЛЕН ПРАВИЛЬНО","en":"YOUR COMPASS IS POINTING RIGHT",
              "uz":"KOMPASINGIZ TO'G'RI YO'NALGAN","de":"IHR KOMPASS ZEIGT RICHTIG","tr":"PUSULANI DOĞRU YÖNDESİNİZ"}.get(lang,"YOUR COMPASS IS POINTING RIGHT")
        fs = {"ru":"Используйте свои сильные стороны, развивайтесь там, где это важно.",
              "en":"Use your strengths and grow where it matters.",
              "uz":"Kuchli tomonlaringizdan foydalaning, rivojlaning.",
              "de":"Nutzen Sie Ihre Stärken und wachsen Sie.","tr":"Güçlü yönlerinizi kullanın, büyüyün."}.get(lang,"Use your strengths.")
        draw.text((22, H-78), ft, font=fMed,  fill=WHITE)
        draw.text((22, H-46), fs, font=fTiny, fill=(180,210,240))
        draw.text((22, H-22), "@Behavior_Compass_bot", font=fTiny, fill=(150,190,230))

        output_path = output_dir / f"{telegram_id}_{primary_color}.png"
        img.save(str(output_path), quality=95)
        return str(output_path)
