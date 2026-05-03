from aiogram.types import BotCommand


language_codes = [
    'ru', 'en', 'kk', 'de', 'fr', 'it', 'es', 'nl', 'sv', 
    'fi', 'no', 'he', 'ko', 'ja', 'cs', 'sk', 'sl', 'pl', 'pt', 
    'hr', 'ar', 'be', 'ca', 'hu', 'id', 'ms', 'fa', 'ro', 'sr', 
    'tr', 'uk', 'uz', 'hi', 'vi', 'th', 'zh', 'el'
]


DESCRIPTIONS = {
    'ru': "🤖 Бот поможет подготовиться к экзамену на знание ПДД и закрепить полученные в автошколе знания",
    'en': "🤖 The bot helps you prepare for the traffic rules exam and reinforce knowledge gained in driving school",
    'kk': "🤖 Бот ЖҚЕ емтиханына дайындалуға және авто-мектепте алған білімді бекітуге көмектеседі",
    'de': "🤖 Der Bot hilft bei der Vorbereitung auf die Verkehrsregeln-Prüfung und festigt das in der Fahrschule erworbene Wissen",
    'fr': "🤖 Le bot aide à se préparer à l’examen du code de la route et à renforcer les connaissances acquises à l’auto-école",
    'it': "🤖 Il bot aiuta a prepararsi all’esame di teoria della guida e a consolidare le conoscenze acquisite a scuola guida",
    'es': "🤖 El bot ayuda a prepararse para el examen de normas de tráfico y a reforzar los conocimientos adquiridos en la autoescuela",
    'nl': "🤖 De bot helpt bij de voorbereiding op het verkeersregels-examen en versterkt de kennis opgedaan in de rijschool",
    'sv': "🤖 Boten hjälper dig att förbereda dig för trafikreglerprovet och förstärka kunskaper från körskolan",
    'fi': "🤖 Botti auttaa valmistautumaan liikennesääntöjen kokeeseen ja vahvistamaan autokoulussa opittuja tietoja",
    'no': "🤖 Boten hjelper deg med å forberede deg til trafikkregler-eksamen og styrke kunnskapen fra kjøreskolen",
    'he': "🤖 הבוט עוזר להתכונן למבחן חוקי התנועה ולחזק את הידע שנרכש בבית הספר לנהיגה",
    'ko': "🤖 이 봇은 교통 법규 시험 준비와 운전학원에서 배운 지식을 강화하는 데 도움을 줍니다",
    'ja': "🤖 このボットは交通ルール試験の準備と自動車教習所で得た知識の定着をサポートします",
    'cs': "🤖 Bot pomáhá s přípravou na zkoušku z dopravních předpisů a upevňuje znalosti získané v autoškole",
    'sk': "🤖 Bot pomáha pripraviť sa na skúšku z dopravných predpisov a upevniť vedomosti získané v autoškole",
    'sl': "🤖 Bot pomaga pri pripravi na izpit iz prometnih predpisov in utrjevanju znanja iz avtošole",
    'pl': "🤖 Bot pomaga przygotować się do egzaminu z przepisów ruchu drogowego i utrwalić wiedzę zdobytą w szkole jazdy",
    'pt': "🤖 O bot ajuda a preparar para o exame de regras de trânsito e reforçar o conhecimento adquirido na autoescola",
    'hr': "🤖 Bot pomaže u pripremi za ispit iz prometnih propisa i učvršćivanju znanja iz autoškole",
    'ar': "🤖 يساعدك البوت على الاستعداد لاختبار قواعد المرور وتعزيز المعرفة المكتسبة في مدرسة القيادة",
    'be': "🤖 Бот дапамагае падрыхтавацца да экзамену па правілах дарожнага руху і замацаваць веды з аўташколы",
    'ca': "🤖 El bot ajuda a preparar-se per a l’examen de normes de trànsit i reforçar els coneixements de l’autoescola",
    'hu': "🤖 A bot segít felkészülni a közlekedési szabályok vizsgájára és megerősíteni a tanultakat az autósiskolában",
    'id': "🤖 Bot membantu mempersiapkan ujian peraturan lalu lintas dan memperkuat pengetahuan dari sekolah mengemudi",
    'ms': "🤖 Bot membantu anda bersedia untuk ujian peraturan lalu lintas dan mengukuhkan pengetahuan dari sekolah memandu",
    'fa': "🤖 این ربات به شما کمک می‌کند برای آزمون قوانین رانندگی آماده شوید و دانش خود را تقویت کنید",
    'ro': "🤖 Botul te ajută să te pregătești pentru examenul de reguli de circulație și să consolidezi cunoștințele din școala de șoferi",
    'sr': "🤖 Bot pomaže u pripremi za ispit iz saobraćajnih propisa i utvrđivanju znanja iz auto-škole",
    'tr': "🤖 Bot, trafik kuralları sınavına hazırlanmanıza ve sürücü kursunda edindiğiniz bilgileri pekiştirmenize yardımcı olur",
    'uk': "🤖 Бот допомагає підготуватися до іспиту з правил дорожнього руху та закріпити знання, отримані в автошколі",
    'uz': "🤖 Bot yo‘l harakati qoidalari imtihoniga tayyorlanishga va haydovchilik maktabida olingan bilimlarni mustahkamlashga yordam beradi",
    'hi': "🤖 यह बॉट आपको ट्रैफिक नियमों की परीक्षा की तैयारी करने और ड्राइविंग स्कूल में सीखी गई जानकारी को मजबूत करने में मदद करता है",
    'vi': "🤖 Bot giúp bạn chuẩn bị cho kỳ thi luật giao thông và củng cố kiến thức học được từ trường lái xe",
    'th': "🤖 บอทช่วยคุณเตรียมตัวสำหรับการสอบกฎจราจรและเสริมความรู้จากโรงเรียนสอนขับรถ",
    'zh': "🤖 该机器人帮助你准备交通规则考试，并巩固在驾校学到的知识",
    'el': "🤖 Το bot βοηθά στην προετοιμασία για την εξέταση κανόνων κυκλοφορίας και στην ενίσχυση των γνώσεων από τη σχολή οδήγησης",
}


SHORT_DESCRIPTIONS = {
    'ru': "🤖 Тесты ПДД для подготовки к экзамену",
    'en': "🤖 Traffic rules tests to prepare for the exam",
    'kk': "🤖 ЖҚЕ емтиханына дайындалуға арналған тесттер",
    'de': "🤖 Verkehrsregeln-Tests zur Vorbereitung auf die Prüfung",
    'fr': "🤖 Tests du code de la route pour préparer l’examen",
    'it': "🤖 Test di teoria per prepararsi all’esame di guida",
    'es': "🤖 Tests de tráfico para prepararte para el examen",
    'nl': "🤖 Verkeersregeltests ter voorbereiding op het examen",
    'sv': "🤖 Trafiktest för att förbereda dig inför provet",
    'fi': "🤖 Liikennesääntötestit kokeeseen valmistautumiseen",
    'no': "🤖 Trafikkprøver for å forberede deg til eksamen",
    'he': "🤖 מבחני חוקי תנועה להכנה למבחן",
    'ko': "🤖 시험 준비를 위한 교통 법규 테스트",
    'ja': "🤖 試験対策のための交通ルールテスト",
    'cs': "🤖 Testy dopravních předpisů pro přípravu na zkoušku",
    'sk': "🤖 Testy z dopravných predpisov na prípravu na skúšku",
    'sl': "🤖 Testi prometnih predpisov za pripravo na izpit",
    'pl': "🤖 Testy przepisów ruchu drogowego do przygotowania do egzaminu",
    'pt': "🤖 Testes de trânsito para se preparar para o exame",
    'hr': "🤖 Testovi prometnih propisa za pripremu za ispit",
    'ar': "🤖 اختبارات قواعد المرور للتحضير للامتحان",
    'be': "🤖 Тэсты ПДР для падрыхтоўкі да экзамену",
    'ca': "🤖 Tests de trànsit per preparar l’examen",
    'hu': "🤖 Közlekedési tesztek a vizsgára való felkészüléshez",
    'id': "🤖 Tes lalu lintas untuk persiapan ujian",
    'ms': "🤖 Ujian trafik untuk persediaan peperiksaan",
    'fa': "🤖 تست‌های قوانین رانندگی برای آمادگی در آزمون",
    'ro': "🤖 Teste de circulație pentru pregătirea examenului",
    'sr': "🤖 Testovi saobraćajnih propisa za pripremu ispita",
    'tr': "🤖 Sınava hazırlanmak için trafik kuralları testleri",
    'uk': "🤖 Тести ПДР для підготовки до іспиту",
    'uz': "🤖 Imtihonga tayyorlanish uchun yo‘l qoidalari testlari",
    'hi': "🤖 परीक्षा की तैयारी के लिए ट्रैफिक नियमों के टेस्ट",
    'vi': "🤖 Bài kiểm tra luật giao thông để chuẩn bị cho kỳ thi",
    'th': "🤖 แบบทดสอบกฎจราจรเพื่อเตรียมสอบ",
    'zh': "🤖 用于备考的交通规则测试",
    'el': "🤖 Τεστ κανόνων κυκλοφορίας για προετοιμασία εξετάσεων",
}


NAMES = {
    'ru': 'ПДД Тесты',
    'en': 'Traffic Rules Tests',
    'kk': 'Жол ережелері тесттері',
    'de': 'Verkehrsregeln Tests',
    'fr': 'Tests du code de la route',
    'it': 'Test del codice della strada',
    'es': 'Tests de normas de tráfico',
    'nl': 'Verkeersregels tests',
    'sv': 'Trafikregler tester',
    'fi': 'Liikennesääntötestit',
    'no': 'Trafikkregler tester',
    'he': 'מבחני חוקי התנועה',
    'ko': '교통법규 시험',
    'ja': '交通ルールテスト',
    'cs': 'Testy dopravních předpisů',
    'sk': 'Testy dopravných predpisov',
    'sl': 'Testi prometnih pravil',
    'pl': 'Testy przepisów ruchu drogowego',
    'pt': 'Testes de regras de trânsito',
    'hr': 'Testovi prometnih propisa',
    'ar': 'اختبارات قواعد المرور',
    'be': 'Тэсты па правілах дарожнага руху',
    'ca': 'Tests de normes de trànsit',
    'hu': 'Közlekedési szabályok tesztjei',
    'id': 'Tes aturan lalu lintas',
    'ms': 'Ujian peraturan lalu lintas',
    'fa': 'آزمون‌های قوانین راهنمایی و رانندگی',
    'ro': 'Teste de reguli de circulație',
    'sr': 'Тестови саобраћајних прописа',
    'tr': 'Trafik kuralları testleri',
    'uk': 'Тести з правил дорожнього руху',
    'uz': 'Yo‘l harakati qoidalari testlari',
    'hi': 'यातायात नियम परीक्षण',
    'vi': 'Bài kiểm tra luật giao thông',
    'th': 'แบบทดสอบกฎจราจร',
    'zh': '交通规则测试',
    'el': 'Τεστ κανόνων κυκλοφορίας'
}


COMMANDS = {
    "ru": [
        BotCommand(command="question", description="Получить вопрос"),
        BotCommand(command="theme", description="Поменять оформление"),
        BotCommand(command="books", description="Получить список книг"),
        BotCommand(command="donate", description="Поддержать проект"),
        BotCommand(command="forum", description="Обсудить вопросы по ПДД"),
        BotCommand(command="error", description="Сообщить об ошибке"),
    ],

    "en": [
        BotCommand(command="question", description="Get a question"),
        BotCommand(command="theme", description="Change theme"),
        BotCommand(command="books", description="Get list of books"),
        BotCommand(command="donate", description="Support the project"),
        BotCommand(command="forum", description="Discuss traffic rules questions"),
        BotCommand(command="error", description="Report an issue"),
    ],

    "kk": [
        BotCommand(command="question", description="Сұрақ алу"),
        BotCommand(command="theme", description="Тақырыпты өзгерту"),
        BotCommand(command="books", description="Кітаптар тізімін алу"),
        BotCommand(command="donate", description="Жобаны қолдау"),
        BotCommand(command="forum", description="Жол ережелері бойынша талқылау"),
        BotCommand(command="error", description="Қате туралы хабарлау"),
    ],

    "de": [
        BotCommand(command="question", description="Frage erhalten"),
        BotCommand(command="theme", description="Design ändern"),
        BotCommand(command="books", description="Bücherliste anzeigen"),
        BotCommand(command="donate", description="Projekt unterstützen"),
        BotCommand(command="forum", description="Verkehrsregeln diskutieren"),
        BotCommand(command="error", description="Fehler melden"),
    ],

    "fr": [
        BotCommand(command="question", description="Obtenir une question"),
        BotCommand(command="theme", description="Changer le thème"),
        BotCommand(command="books", description="Obtenir la liste des livres"),
        BotCommand(command="donate", description="Soutenir le projet"),
        BotCommand(command="forum", description="Discuter du code de la route"),
        BotCommand(command="error", description="Signaler une erreur"),
    ],

    "it": [
        BotCommand(command="question", description="Ricevi una domanda"),
        BotCommand(command="theme", description="Cambia tema"),
        BotCommand(command="books", description="Ottieni elenco libri"),
        BotCommand(command="donate", description="Sostieni il progetto"),
        BotCommand(command="forum", description="Discuti il codice della strada"),
        BotCommand(command="error", description="Segnala un errore"),
    ],

    "es": [
        BotCommand(command="question", description="Obtener una pregunta"),
        BotCommand(command="theme", description="Cambiar tema"),
        BotCommand(command="books", description="Obtener lista de libros"),
        BotCommand(command="donate", description="Apoyar el proyecto"),
        BotCommand(command="forum", description="Discutir normas de tráfico"),
        BotCommand(command="error", description="Reportar un error"),
    ],

    "nl": [
        BotCommand(command="question", description="Vraag ontvangen"),
        BotCommand(command="theme", description="Thema wijzigen"),
        BotCommand(command="books", description="Boekenlijst bekijken"),
        BotCommand(command="donate", description="Project ondersteunen"),
        BotCommand(command="forum", description="Verkeersregels bespreken"),
        BotCommand(command="error", description="Fout melden"),
    ],

    "sv": [
        BotCommand(command="question", description="Hämta en fråga"),
        BotCommand(command="theme", description="Byt tema"),
        BotCommand(command="books", description="Visa boklista"),
        BotCommand(command="donate", description="Stöd projektet"),
        BotCommand(command="forum", description="Diskutera trafikregler"),
        BotCommand(command="error", description="Rapportera fel"),
    ],

    "fi": [
        BotCommand(command="question", description="Hae kysymys"),
        BotCommand(command="theme", description="Vaihda teema"),
        BotCommand(command="books", description="Näytä kirjalista"),
        BotCommand(command="donate", description="Tue projektia"),
        BotCommand(command="forum", description="Keskustele liikennesäännöistä"),
        BotCommand(command="error", description="Ilmoita virheestä"),
    ],

    "no": [
        BotCommand(command="question", description="Få et spørsmål"),
        BotCommand(command="theme", description="Endre tema"),
        BotCommand(command="books", description="Vis bokliste"),
        BotCommand(command="donate", description="Støtt prosjektet"),
        BotCommand(command="forum", description="Diskuter trafikkregler"),
        BotCommand(command="error", description="Rapporter feil"),
    ],

    "he": [
        BotCommand(command="question", description="קבל שאלה"),
        BotCommand(command="theme", description="שנה עיצוב"),
        BotCommand(command="books", description="קבל רשימת ספרים"),
        BotCommand(command="donate", description="תמוך בפרויקט"),
        BotCommand(command="forum", description="דיון בכללי תעבורה"),
        BotCommand(command="error", description="דווח על שגיאה"),
    ],

    "ko": [
        BotCommand(command="question", description="질문 받기"),
        BotCommand(command="theme", description="테마 변경"),
        BotCommand(command="books", description="책 목록 보기"),
        BotCommand(command="donate", description="프로젝트 후원"),
        BotCommand(command="forum", description="교통 규칙 토론"),
        BotCommand(command="error", description="오류 신고"),
    ],

    "ja": [
        BotCommand(command="question", description="問題を取得"),
        BotCommand(command="theme", description="テーマを変更"),
        BotCommand(command="books", description="書籍リストを取得"),
        BotCommand(command="donate", description="プロジェクトを支援"),
        BotCommand(command="forum", description="交通ルールを議論"),
        BotCommand(command="error", description="エラーを報告"),
    ],

    "cs": [
        BotCommand(command="question", description="Získat otázku"),
        BotCommand(command="theme", description="Změnit motiv"),
        BotCommand(command="books", description="Zobrazit seznam knih"),
        BotCommand(command="donate", description="Podpořit projekt"),
        BotCommand(command="forum", description="Diskuze o pravidlech silničního provozu"),
        BotCommand(command="error", description="Nahlásit chybu"),
    ],

    "sk": [
        BotCommand(command="question", description="Získať otázku"),
        BotCommand(command="theme", description="Zmeniť tému"),
        BotCommand(command="books", description="Zobraziť zoznam kníh"),
        BotCommand(command="donate", description="Podporiť projekt"),
        BotCommand(command="forum", description="Diskusia o pravidlách cestnej premávky"),
        BotCommand(command="error", description="Nahlásiť chybu"),
    ],

    "sl": [
        BotCommand(command="question", description="Pridobi vprašanje"),
        BotCommand(command="theme", description="Spremeni temo"),
        BotCommand(command="books", description="Pridobi seznam knjig"),
        BotCommand(command="donate", description="Podpri projekt"),
        BotCommand(command="forum", description="Razprava o prometnih pravilih"),
        BotCommand(command="error", description="Prijavi napako"),
    ],

    "pl": [
        BotCommand(command="question", description="Otrzymaj pytanie"),
        BotCommand(command="theme", description="Zmień motyw"),
        BotCommand(command="books", description="Pokaż listę książek"),
        BotCommand(command="donate", description="Wesprzyj projekt"),
        BotCommand(command="forum", description="Dyskusja o przepisach ruchu drogowego"),
        BotCommand(command="error", description="Zgłoś błąd"),
    ],

    "pt": [
        BotCommand(command="question", description="Obter pergunta"),
        BotCommand(command="theme", description="Alterar tema"),
        BotCommand(command="books", description="Obter lista de livros"),
        BotCommand(command="donate", description="Apoiar o projeto"),
        BotCommand(command="forum", description="Discutir regras de trânsito"),
        BotCommand(command="error", description="Reportar erro"),
    ],

    "hr": [
        BotCommand(command="question", description="Dohvati pitanje"),
        BotCommand(command="theme", description="Promijeni temu"),
        BotCommand(command="books", description="Prikaži popis knjiga"),
        BotCommand(command="donate", description="Podrži projekt"),
        BotCommand(command="forum", description="Rasprava o prometnim pravilima"),
        BotCommand(command="error", description="Prijavi pogrešku"),
    ],

    "ar": [
        BotCommand(command="question", description="الحصول على سؤال"),
        BotCommand(command="theme", description="تغيير المظهر"),
        BotCommand(command="books", description="عرض قائمة الكتب"),
        BotCommand(command="donate", description="دعم المشروع"),
        BotCommand(command="forum", description="مناقشة قواعد المرور"),
        BotCommand(command="error", description="الإبلاغ عن خطأ"),
    ],

    "be": [
        BotCommand(command="question", description="Атрымаць пытанне"),
        BotCommand(command="theme", description="Змяніць афармленне"),
        BotCommand(command="books", description="Атрымаць спіс кніг"),
        BotCommand(command="donate", description="Падтрымаць праект"),
        BotCommand(command="forum", description="Абмеркаванне ПДР"),
        BotCommand(command="error", description="Паведаміць пра памылку"),
    ],

    "ca": [
        BotCommand(command="question", description="Obtenir una pregunta"),
        BotCommand(command="theme", description="Canviar tema"),
        BotCommand(command="books", description="Obtenir llista de llibres"),
        BotCommand(command="donate", description="Donar suport al projecte"),
        BotCommand(command="forum", description="Debatre normes de trànsit"),
        BotCommand(command="error", description="Informar d’un error"),
    ],

    "hu": [
        BotCommand(command="question", description="Kérdés kapása"),
        BotCommand(command="theme", description="Téma váltása"),
        BotCommand(command="books", description="Könyvlista megtekintése"),
        BotCommand(command="donate", description="Projekt támogatása"),
        BotCommand(command="forum", description="KRESZ szabályok megvitatása"),
        BotCommand(command="error", description="Hiba jelentése"),
    ],

    "id": [
        BotCommand(command="question", description="Dapatkan pertanyaan"),
        BotCommand(command="theme", description="Ubah tema"),
        BotCommand(command="books", description="Dapatkan daftar buku"),
        BotCommand(command="donate", description="Dukung proyek"),
        BotCommand(command="forum", description="Diskusi aturan lalu lintas"),
        BotCommand(command="error", description="Laporkan kesalahan"),
    ],

    "ms": [
        BotCommand(command="question", description="Dapatkan soalan"),
        BotCommand(command="theme", description="Tukar tema"),
        BotCommand(command="books", description="Dapatkan senarai buku"),
        BotCommand(command="donate", description="Sokong projek"),
        BotCommand(command="forum", description="Perbincangan peraturan jalan raya"),
        BotCommand(command="error", description="Laporkan ralat"),
    ],

    "fa": [
        BotCommand(command="question", description="دریافت سؤال"),
        BotCommand(command="theme", description="تغییر ظاهر"),
        BotCommand(command="books", description="دریافت لیست کتاب‌ها"),
        BotCommand(command="donate", description="حمایت از پروژه"),
        BotCommand(command="forum", description="بحث قوانین راهنمایی و رانندگی"),
        BotCommand(command="error", description="گزارش خطا"),
    ],

    "ro": [
        BotCommand(command="question", description="Obține o întrebare"),
        BotCommand(command="theme", description="Schimbă tema"),
        BotCommand(command="books", description="Obține lista de cărți"),
        BotCommand(command="donate", description="Susține proiectul"),
        BotCommand(command="forum", description="Discută reguli de circulație"),
        BotCommand(command="error", description="Raportează o eroare"),
    ],

    "sr": [
        BotCommand(command="question", description="Добиј питање"),
        BotCommand(command="theme", description="Промени тему"),
        BotCommand(command="books", description="Прикажи списак књига"),
        BotCommand(command="donate", description="Подржи пројекат"),
        BotCommand(command="forum", description="Дискусија о саобраћајним правилима"),
        BotCommand(command="error", description="Пријави грешку"),
    ],

    "tr": [
        BotCommand(command="question", description="Soru al"),
        BotCommand(command="theme", description="Temayı değiştir"),
        BotCommand(command="books", description="Kitap listesini al"),
        BotCommand(command="donate", description="Projeyi destekle"),
        BotCommand(command="forum", description="Trafik kurallarını tartış"),
        BotCommand(command="error", description="Hata bildir"),
    ],

    "uk": [
        BotCommand(command="question", description="Отримати запитання"),
        BotCommand(command="theme", description="Змінити оформлення"),
        BotCommand(command="books", description="Отримати список книг"),
        BotCommand(command="donate", description="Підтримати проєкт"),
        BotCommand(command="forum", description="Обговорення ПДР"),
        BotCommand(command="error", description="Повідомити про помилку"),
    ],

    "uz": [
        BotCommand(command="question", description="Savol olish"),
        BotCommand(command="theme", description="Mavzuni o‘zgartirish"),
        BotCommand(command="books", description="Kitoblar ro‘yxatini olish"),
        BotCommand(command="donate", description="Loyihani qo‘llab-quvvatlash"),
        BotCommand(command="forum", description="Yo‘l harakati qoidalarini muhokama qilish"),
        BotCommand(command="error", description="Xatolik haqida xabar berish"),
    ],

    "hi": [
        BotCommand(command="question", description="प्रश्न प्राप्त करें"),
        BotCommand(command="theme", description="थीम बदलें"),
        BotCommand(command="books", description="पुस्तक सूची प्राप्त करें"),
        BotCommand(command="donate", description="परियोजना का समर्थन करें"),
        BotCommand(command="forum", description="यातायात नियमों पर चर्चा"),
        BotCommand(command="error", description="त्रुटि रिपोर्ट करें"),
    ],

    "vi": [
        BotCommand(command="question", description="Nhận câu hỏi"),
        BotCommand(command="theme", description="Đổi giao diện"),
        BotCommand(command="books", description="Nhận danh sách sách"),
        BotCommand(command="donate", description="Ủng hộ dự án"),
        BotCommand(command="forum", description="Thảo luận luật giao thông"),
        BotCommand(command="error", description="Báo lỗi"),
    ],

    "th": [
        BotCommand(command="question", description="รับคำถาม"),
        BotCommand(command="theme", description="เปลี่ยนธีม"),
        BotCommand(command="books", description="ดูรายการหนังสือ"),
        BotCommand(command="donate", description="สนับสนุนโครงการ"),
        BotCommand(command="forum", description="อภิปรายกฎจราจร"),
        BotCommand(command="error", description="รายงานข้อผิดพลาด"),
    ],

    "zh": [
        BotCommand(command="question", description="获取题目"),
        BotCommand(command="theme", description="更换主题"),
        BotCommand(command="books", description="获取书籍列表"),
        BotCommand(command="donate", description="支持项目"),
        BotCommand(command="forum", description="讨论交通规则"),
        BotCommand(command="error", description="报告错误"),
    ],

    "el": [
        BotCommand(command="question", description="Λήψη ερώτησης"),
        BotCommand(command="theme", description="Αλλαγή θέματος"),
        BotCommand(command="books", description="Λήψη λίστας βιβλίων"),
        BotCommand(command="donate", description="Υποστήριξη έργου"),
        BotCommand(command="forum", description="Συζήτηση ΚΟΚ"),
        BotCommand(command="error", description="Αναφορά σφάλματος"),
    ],
}
