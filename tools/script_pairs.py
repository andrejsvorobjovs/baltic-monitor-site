# -*- coding: utf-8 -*-
"""Russian for every user-facing string the Latvian page builds in JavaScript.

The visible-text pass cannot touch these: they live inside <script> blocks as
string literals, and several are sentence FRAGMENTS concatenated around a
number, so each one has to be translated with the join in mind rather than on
its own. They are applied longest-first — ' vienība(s)' is a suffix of
' baumu/dezinformācijas vienība(s) izsekota(s)', and replacing the short one
first would corrupt the long one.
"""
SCRIPT_PAIRS = [
    # --- liveness banner ---
    ("Neviens to nav darbinājis vairāk nekā 10 dienas",
     "Никто не запускал это более 10 дней"),
    ("Pēdējā skenēšana pabeigta {age}. Kopš tā laika nekas nav pārbaudīts. "
     "Šo projektu uztur viens cilvēks. Tik ilgs klusums visticamāk nozīmē, "
     "ka šī persona to vairs nevar darbināt — tostarp iespēju, ka šī persona "
     "ir mirusi. <strong>Neuzskatiet brīdinājumu trūkumu par drošības "
     "apliecinājumu.</strong>",
     "Последнее сканирование завершено {age}. С тех пор ничего не "
     "проверялось. Этот проект ведёт один человек. Такое долгое молчание "
     "скорее всего означает, что этот человек больше не может его запускать "
     "— включая возможность, что этого человека нет в живых. <strong>Не "
     "принимай отсутствие предупреждений за подтверждение "
     "безопасности.</strong>"),
    ("Neizdevās pārbaudīt datu svaigumu",
     "Не удалось проверить свежесть данных"),
    ("Lapa nevarēja noteikt, kad tā pēdējoreiz atjaunināta. Izturieties pret "
     "zemāk redzamo statusu piesardzīgi.",
     "Страница не смогла определить, когда она обновлялась в последний раз. "
     "Относись к статусу ниже с осторожностью."),
    ("Netiek atjaunināts", "Не обновляется"),
    ("(pēdējais zināmais)", "(последнее известное)"),
    # --- status row ---
    ("Darbojas normāli", "Работает нормально"),
    ("Nepieciešama uzmanība", "Требуется внимание"),
    # --- held-back reasons ---
    ("Izsludinātas sabiedroto mācības", "Объявленные учения союзников"),
    ("Analīzes vai scenārija raksts", "Аналитическая или сценарная статья"),
    ("Par šo stāstu jau brīdināts", "Об этой истории уже предупреждали"),
    (" būtiski ieraksti apturēti ", " значимых записей задержано в "),
    (" skenēšanās, no kurām ", " сканированиях, из которых "),
    (" paaugstināja līmeni.", " повысили уровень."),
    (" vecākas skenēšanas šajā logā notika pirms apturējumu reģistrēšanas un "
     "šajos skaitļos neietilpst.",
     " более ранних сканирований в этом окне прошли до того, как задержки "
     "стали регистрироваться, и в эти числа не входят."),
    # --- live data footer ---
    ("Dzīvie dati ģenerēti ", "Живые данные сгенерированы "),
    (", seko kopš ", ", отслеживание с "),
    # --- scan history rows ---
    ("Vēl nav reģistrēts neviens skenējums.",
     "Пока не зарегистрировано ни одного сканирования."),
    (" atzīmēti)", " отмечено)"),
    ("Kāpēc avoti dažreiz neizdodas visi vienlaikus — skatiet BUJ zemāk",
     "Почему источники иногда отказывают все сразу — смотри вопросы ниже"),
    ("šim vecākajam skenējumam avotu skaits nav reģistrēts",
     "для этого более старого сканирования количество источников не записано"),
    (" tiešās izdevumu plūsmas — ātrā agrīnās brīdināšanas pārbaude starp "
     "pilnajiem skenējumiem",
     " прямых потоков изданий — быстрая проверка раннего предупреждения "
     "между полными сканированиями"),
    (" avoti pārbaudīti (1./2./3. līmenis + GDELT)",
     " источников проверено (уровень 1/2/3 + GDELT)"),
    (" avoti pārbaudīti (1./2./3. līmenis)",
     " источников проверено (уровень 1/2/3)"),
    (" baumu/dezinformācijas vienība(s) izsekota(s)",
     " единиц слухов/дезинформации отслежено"),
    (" jauns vienums(-i) pārskatīts(-i)", " новых материалов рассмотрено"),
    (" novecojis(-ši) vienums(-i) izslēgts(-i)",
     " устаревших материалов исключено"),
    ("brīdinājuma ID ", "ID предупреждения "),
    ("Marķieri: ", "Маркеры: "),
    # --- corrections / updates ---
    ("Līdz šim neviens nav izdots — pagaidām tīra vēsture.",
     "До сих пор ни одного не выпущено — пока чистая история."),
    ("Pagaidām nekas nav reģistrēts.", "Пока ничего не зарегистрировано."),
    # --- charts ---
    ("Vēl nav pietiekami daudz vēstures — tas veidojas laika gaitā.",
     "Пока недостаточно истории — она накапливается со временем."),
    ("Eskalācijas intensitāte laika gaitā", "Интенсивность эскалации во времени"),
    ("0 (neitrāls tonis)", "0 (нейтральный тон)"),
    (" toņa diapazons", " диапазон тона"),
    ("Signāla novirzes indekss laika gaitā", "Индекс отклонения сигнала во времени"),
    ("WATCH un WARN brīdinājumi laika gaitā",
     "Предупреждения WATCH и WARN во времени"),
    ("Baumu/dezinformācijas izsekošana laika gaitā",
     "Отслеживание слухов/дезинформации во времени"),
    ("GPS traucēšanas intensitāte laika gaitā",
     "Интенсивность глушения GPS во времени"),
    ("AIS kuģu skaits laika gaitā", "Количество судов AIS во времени"),
    ("Militāro gaisa kuģu skaits laika gaitā",
     "Количество военных воздушных судов во времени"),
    ("Termiskie karstuma punkti laika gaitā", "Тепловые точки во времени"),
    ("Elektrotīkla pārtraukumi laika gaitā", "Перерывы в электросети во времени"),
    ("Diagrammas dati īslaicīgi nav pieejami.",
     "Данные диаграммы временно недоступны."),
    ("baumu/dezinformācijas vienība(s)", "единиц слухов/дезинформации"),
    ("augsta traucējuma šūna(-s)", "ячеек сильного глушения"),
    ("novēroti kuģi", "судов наблюдалось"),
    ("gaisa kuģi ar ADS-B", "воздушных судов с ADS-B"),
    ("piespiedu pārtraukumi", "принудительных отключений"),
    (" vienība(s)", " единиц"),
    ("vienība(s)", "единиц"),
    # --- signal-deviation index wording ---
    ("% vs. bāzes līmenis (", "% к базовому уровню ("),
    ("/4 signāli)", "/4 сигнала)"),
    ("GPS traucēšana", "Глушение GPS"),
    ("AIS kuģu satiksme", "Судовой трафик AIS"),
    ("militārie lidaparāti", "военные воздушные суда"),
    ("termiskie punkti", "тепловые точки"),
    ("stipri paaugstināts", "сильно повышен"),
    ("mēreni paaugstināts", "умеренно повышен"),
    ("normas robežās", "в пределах нормы"),
    ("mēreni zem normas", "умеренно ниже нормы"),
    ("krietni zem normas", "значительно ниже нормы"),
    ("{s} {p}% virs bāzes līmeņa", "{s} {p}% выше базового уровня"),
    ("{s} {p}% zem bāzes līmeņa", "{s} {p}% ниже базового уровня"),
    ("{list} bez izmaiņām", "{list} без изменений"),
    ("augstākais {n} skenējumu laikā", "максимум за {n} сканирований"),
    ("Datu vēl nav", "Данных пока нет"),
    ("Vēl nav pietiekami daudz datu", "Пока недостаточно данных"),
    (" / 4 uzraudzīti", " / 4 отслеживается"),
    # Latvian without diacritics — invisible to the diacritic sweep, so
    # these are listed explicitly.
    ("Noliegums / nav draudu ietvars", "Опровержение / рамка «угрозы нет»"),
    ("(bez nosaukuma)", "(без названия)"),
    ("Statuss nav pieejams", "Статус недоступен"),
    ("termiskie karstuma punkti", "тепловые точки"),
]

# Two places need the JavaScript itself rewritten, not a literal swapped:
# Russian needs three plural forms where Latvian needs two, and the
# filter-record window reads naturally only with the noun after the number.
SCRIPT_REWRITES = [
    ("""  hoursAgo: function (n) { return 'pirms ' + n + ' ' + ((n % 10 === 1 && n % 100 !== 11) ? 'stundas' : 'stundām'); },
  daysAgo: function (n) { return 'pirms ' + n + ' ' + ((n % 10 === 1 && n % 100 !== 11) ? 'dienas' : 'dienām'); },""",
     """  // Russian needs three plural forms, not two: 1 час / 2-4 часа /
  // 5+ часов, with the teens (11-14) taking the many-form regardless of
  // their last digit. Getting this wrong is the first thing a native
  // reader notices, so it is spelled out rather than approximated.
  hoursAgo: function (n) {
    var last = n % 10, teen = n % 100;
    var unit = (last === 1 && teen !== 11) ? 'час'
             : (last >= 2 && last <= 4 && (teen < 12 || teen > 14)) ? 'часа'
             : 'часов';
    return n + ' ' + unit + ' назад';
  },
  daysAgo: function (n) {
    var last = n % 10, teen = n % 100;
    var unit = (last === 1 && teen !== 11) ? 'день'
             : (last >= 2 && last <= 4 && (teen < 12 || teen > 14)) ? 'дня'
             : 'дней';
    return n + ' ' + unit + ' назад';
  },"""),
    ("""'pēdējās ' + fr.window_days + ' dienas'""",
     """'последние ' + fr.window_days + ' ' + (function (n) {
          var last = n % 10, teen = n % 100;
          return (last === 1 && teen !== 11) ? 'день'
               : (last >= 2 && last <= 4 && (teen < 12 || teen > 14)) ? 'дня'
               : 'дней';
        })(fr.window_days)"""),
]
