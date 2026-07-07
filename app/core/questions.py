"""Тестовые вопросы"""

QUESTIONS = {
    "en": [
        "I prefer working in a structured environment with clear guidelines.",
        "I enjoy being the center of attention in social situations.",
        "I focus on how decisions might affect people.",
        "I like to analyze all available information before making decisions.",
        "I bring enthusiasm and energy to group activities.",
        "I prefer to lead rather than follow in team situations.",
        "I prefer to build harmony and maintain good relationships.",
        "I approach problems with logic and systematic thinking.",
        "I often express my ideas spontaneously.",
        "I enjoy having control and authority in my role.",
        "I prioritize the emotional well-being of those around me.",
        "I prefer accuracy and precision in my work.",
        "I am naturally optimistic and see possibilities.",
        "I prefer direct, decisive action over lengthy discussion.",
        "I am a good listener and care about people's feelings.",
        "I need to understand the 'why' before proceeding.",
        "I can adapt quickly to new situations and changes.",
        "I prefer to set and achieve ambitious goals.",
        "I work best in a supportive, team-oriented environment.",
        "I prefer to plan and organize my work thoroughly.",
        "I thrive in dynamic and fast-paced environments.",
        "I am detail-oriented and notice what others might miss.",
        "I prefer to work independently and trust my instincts.",
        "I make decisions based on established principles and values.",
    ],
    
    "ru": [
        "Я предпочитаю работать в структурированной среде с четкими рекомендациями.",
        "Я люблю быть в центре внимания в социальных ситуациях.",
        "Я думаю о том, как решения могут повлиять на людей.",
        "Мне нравится анализировать всю доступную информацию перед принятием решения.",
        "Я привношу энтузиазм и энергию в групповые мероприятия.",
        "Я предпочитаю руководить, а не следовать в командных ситуациях.",
        "Я предпочитаю создавать гармонию и поддерживать хорошие отношения.",
        "Я подхожу к проблемам с логикой и систематическим мышлением.",
        "Я часто спонтанно выражаю свои идеи.",
        "Мне нравится иметь контроль и авторитет в своей роли.",
        "Я отдаю приоритет эмоциональному благополучию окружающих.",
        "Я предпочитаю точность и аккуратность в своей работе.",
        "Я естественно оптимистичен и вижу возможности.",
        "Я предпочитаю прямые, решительные действия длительному обсуждению.",
        "Я хороший слушатель и забочусь о чувствах людей.",
        "Мне нужно понимать 'почему' перед тем, как действовать.",
        "Я могу быстро адаптироваться к новым ситуациям и изменениям.",
        "Я предпочитаю ставить и достигать амбициозные цели.",
        "Я работаю лучше всего в поддерживающей, командной среде.",
        "Я предпочитаю тщательно планировать и организовывать свою работу.",
        "Я процветаю в динамичной и быстро развивающейся среде.",
        "Я внимателен к деталям и замечаю то, что другие могут пропустить.",
        "Я предпочитаю работать независимо и доверять своей интуиции.",
        "Я принимаю решения на основе установленных принципов и ценностей.",
    ],
    
    "uz": [
        "Men aniq qoidalari bilan tuzilgan muhitda ishlashni afzal ko'raman.",
        "Ijtimoiy situatsiyalarda diqqat markazida bo'lishni yoqtiraman.",
        "Men qaysi qarorlar odamlarni qanday ta'sir qilishi haqida o'ylayman.",
        "Qaror qabul qilishdan oldin barcha mavjud ma'lumotlarni tahlil qilishni yoqtiraman.",
        "Men guruh faoliyatlariga shavqat va energiya olib kelaman.",
        "Men jamoa vaziyatlarida etakchilikning o'rniga qo'llab-quvvatlashni afzal ko'raman.",
        "Men uygunlik yaratishni va yaxshi munosabatlarni saqlashni afzal ko'raman.",
        "Men muammolarga mantiq va tizimli fikrlash bilan yaqinlashaman.",
        "Men ko'pincha o'z g'oyalarimni o'zini bilishi sifatida ifodalaman.",
        "Men o'z rolimda nazorat va hokimiyatga ega bo'lishni yoqtiraman.",
        "Men atrofimdalarimdagi odamlarning emosional farovonligiga ustunlik beraman.",
        "Men o'z ishimda aniqlik va aniqlikni afzal ko'raman.",
        "Men tabiatan optimistman va imkoniyatlarni ko'raman.",
        "Men uzoq muhokama qilishdan ko'ra to'g'ridan-to'g'ri, qat'iy harakatlarni afzal ko'raman.",
        "Men yaxshi tinlovchi va odamlarning his-tuyg'ulariga qarashaman.",
        "Men harakat qilishdan oldin 'nima uchun' deb tushunishim kerak.",
        "Men yangi situatsiyalar va o'zgarishlarga tez moslashim mumkin.",
        "Men ambisius maqsadlarni o'rnattirish va erishishni afzal ko'raman.",
        "Men qo'llab-quvvatlovchi, jamoa yo'naltirilgan muhitda eng yaxshi ishlaman.",
        "Men o'z ishimni diqqat bilan rejalashtirish va tashkil etishni afzal ko'raman.",
        "Men dinamik va tez rivojlanayotgan muhitda qamoq bo'laman.",
        "Men tafsilotlar haqida diqqat qilaman va boshqalar o'tkazib yuborishi mumkin bo'lgan narsalarni sezaman.",
        "Men mustaqil ravishda ishlashni va o'z instinktimga ishonishni afzal ko'raman.",
        "Men qarorlarni o'rnatilgan tamoyillar va qiymatlar asosida qabul qilaman.",
    ],
    
    "de": [
        "Ich bevorzuge es, in einer strukturierten Umgebung mit klaren Richtlinien zu arbeiten.",
        "Ich mag es, im Mittelpunkt von sozialen Situationen zu stehen.",
        "Ich denke über die Auswirkungen von Entscheidungen auf Menschen nach.",
        "Ich analysiere gerne alle verfügbaren Informationen, bevor ich Entscheidungen treffe.",
        "Ich bringe Begeisterung und Energie in Gruppenaktivitäten ein.",
        "Ich bevorzuge es, in Teamsituationen zu führen, anstatt zu folgen.",
        "Ich bevorzuge es, Harmonie zu schaffen und gute Beziehungen zu pflegen.",
        "Ich gehe Probleme mit Logik und systematischem Denken an.",
        "Ich drücke meine Ideen oft spontan aus.",
        "Ich mag es, Kontrolle und Autorität in meiner Rolle zu haben.",
        "Ich priorisiere das emotionale Wohlbefinden der Menschen um mich herum.",
        "Ich bevorzuge Genauigkeit und Präzision in meiner Arbeit.",
        "Ich bin von Natur aus optimistisch und sehe Möglichkeiten.",
        "Ich bevorzuge direkte, entschiedene Maßnahmen über längere Diskussionen.",
        "Ich bin ein guter Zuhörer und kümmere mich um die Gefühle der Menschen.",
        "Ich muss das 'Warum' verstehen, bevor ich voranschreite.",
        "Ich kann mich schnell an neue Situationen und Veränderungen anpassen.",
        "Ich bevorzuge es, ehrgeizige Ziele zu setzen und zu erreichen.",
        "Ich arbeite am besten in einer unterstützenden, teamorientierten Umgebung.",
        "Ich bevorzuge es, meine Arbeit sorgfältig zu planen und zu organisieren.",
        "Ich gedeihe in dynamischen und schnelllebigen Umgebungen.",
        "Ich bin detailorientiert und bemerke, was andere übersehen könnten.",
        "Ich arbeite lieber unabhängig und vertraue meinem Instinkt.",
        "Ich treffe Entscheidungen auf der Grundlage etablierter Prinzipien und Werte.",
    ],
    
    "tr": [
        "Açık yönergeleri olan yapılandırılmış bir ortamda çalışmayı tercih ederim.",
        "Sosyal durumlarda dikkat çekmekten hoşlanırım.",
        "Kararların insanları nasıl etkileyebileceğini düşünürüm.",
        "Karar vermeden önce tüm mevcut bilgileri analiz etmeyi severim.",
        "Grup faaliyetlerine heyecan ve enerji getiririm.",
        "Takım durumlarında takip etmek yerine liderlik etmeyi tercih ederim.",
        "Uyum yaratmayı ve iyi ilişkileri sürdürmeyi tercih ederim.",
        "Sorunlara mantık ve sistematik düşünme ile yaklaşırım.",
        "Fikirlerimi sık sık kendiliğinden ifade ederim.",
        "Rolümde kontrol ve yetki sahibi olmayı severim.",
        "Çevremdeki insanların duygusal refahına öncelik veririm.",
        "İşimde doğruluk ve hassasiyeti tercih ederim.",
        "Doğal olarak iyimserim ve olanakları görürüm.",
        "Uzun tartışmalar yerine doğrudan, kararlı eylemleri tercih ederim.",
        "İyi bir dinleyiciyim ve insanların duygularıyla ilgilenirim.",
        "İlerleme yapmadan önce 'neden' i anlamam gerekir.",
        "Yeni durumlar ve değişikliklere hızlı adapte olabilirim.",
        "Iddialı hedefler belirleme ve ulaşmayı tercih ederim.",
        "Destekleyici, takım odaklı bir ortamda en iyi çalışırım.",
        "İşimi dikkatle planlama ve organize etmeyi tercih ederim.",
        "Dinamik ve hızlı tempolu ortamlarda gelişebilirim.",
        "Detaylara dikkat ederim ve başkaları tarafından gözden kaçırılabilecek şeyleri fark ederim.",
        "Bağımsız çalışmayı ve içgüdülerime güvenmeyi tercih ederim.",
        "Kararları kuruluş ilkeleri ve değerleri temelinde alırım.",
    ]
}


def get_question(language: str, question_num: int) -> str:
    """Получить вопрос"""
    if language not in QUESTIONS:
        language = "en"
    
    if 0 <= question_num < len(QUESTIONS[language]):
        return QUESTIONS[language][question_num]
    
    return f"Question {question_num + 1}"


def get_total_questions() -> int:
    """Получить общее количество вопросов"""
    return len(QUESTIONS["en"])
