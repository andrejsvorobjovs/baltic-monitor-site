# -*- coding: utf-8 -*-
"""Build ru/index.html from lv/index.html.

Latvian is the base rather than English because the Latvian page is
already written for a reader inside the region rather than outside it,
and because the audience for the Russian page overlaps with it almost
exactly: Russian-speaking residents of Latvia and Estonia, roughly a
quarter of each country's population, who are the single group most
targeted by Russian-state disinformation and least served by
Latvian-or-Estonian-only sources.

Matching is whitespace-tolerant: the extracted strings are normalised but
the file holds real newlines and indentation, so every pattern turns runs
of whitespace into \\s+. Anything that fails to match is reported rather
than silently skipped, and a final sweep fails the build if Latvian
diacritics survive in any text node.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_pairs import SCRIPT_PAIRS, SCRIPT_REWRITES

# Repo root, so this runs from anywhere without editing paths.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "lv", "index.html")
DST = os.path.join(ROOT, "ru", "index.html")

# Level names (QUIET/WATCH/WARN) stay English throughout: they are the
# system's own labels, they appear that way in the Telegram digests, and a
# reader comparing the two must see the same word.
PAIRS = [
# --- nav / chrome -----------------------------------------------------------
("Metode", "Метод"),
("Statuss", "Статус"),
("Karte", "Карта"),
("BUJ", "Вопросы"),
("Baltic Signal Monitor — sākumlapa", "Baltic Signal Monitor — главная"),
("Neatkarīgs · Bezmaksas · Nav saistīts ar nevienu valdību",
 "Независимый · Бесплатный · Не связан ни с одним правительством"),
("Signāls, nevis trauksme, Baltijas pierobežā",
 "Сигнал, а не тревога, на балтийском рубеже"),
("Automatizēta atklātā pirmkoda izlūkošana (OSINT), kas seko Krievijas/Baltijas drošības signāliem, izmantojot",
 "Автоматизированная разведка по открытым источникам (OSINT), отслеживающая сигналы безопасности по линии Россия — Балтия по"),
("avotus — valsts drošības dienestus, ziņu aģentūras un dezinformācijas izsekotājus — un vērtē rezultātus pēc neatkarīga apstiprinājuma, pirms kaut kas tiek atzīmēts.",
 "источникам — государственным службам безопасности, информационным агентствам и трекерам дезинформации — и оценивающая результаты по независимому подтверждению, прежде чем что-либо будет отмечено."),
("Pievienojies Telegram", "Присоединиться в Telegram"),
("Seko Mastodon", "Читать в Mastodon"),
("Ielāde…", "Загрузка…"),
("Ielādē…", "Загрузка…"),
("Lasīt metodi", "Читать о методе"),
("Atbalsti šo projektu", "Поддержать проект"),
("Nevēlies izmantot Telegram kontu? Pārlūkprogrammas paziņojumi izmanto tikai tavu pašu pārlūkprogrammu — bez lietotnes, bez konta, bez trešās puses iesaistes.",
 "Не хочешь заводить Telegram? Уведомления в браузере используют только твой собственный браузер — без приложения, без аккаунта, без участия третьих сторон."),
("Statusa lasīšana…", "Чтение статуса…"),
("Pēdējais skenējums", "Последнее сканирование"),
("Rezultāts", "Результат"),
("Kopš", "С"),
("Labojumi", "Исправления"),
# --- safety notice ----------------------------------------------------------
("Šis nav ārkārtas dienests", "Это не служба экстренной помощи"),
("Ārkārtas situācijā zvani 112.", "В экстренной ситуации звони 112."),
("Oficiālie brīdinājumi nāk no tavas valsts iestādēm — Igaunijā",
 "Официальные предупреждения поступают от государственных органов твоей страны — в Эстонии"),
(", Latvijā", ", в Латвии"),
(", Lietuvā", ", в Литве"),
(". Šī vietne nav viena no tām un nerunā nevienas valdības vārdā.",
 ". Этот сайт не является одним из них и не говорит от имени какого-либо правительства."),
("Šis ir automatizēts monitors. Tas var kļūdīties, un ir kļūdījies — katra publicētā kļūda ir uzskaitīta",
 "Это автоматический монитор. Он может ошибаться и ошибался — каждая опубликованная ошибка перечислена в"),
("labojumos", "исправлениях"),
(". Tas var arī klusēt, kamēr kaut kas notiek, jo skenēšana var neizdoties vai aizkavēties.",
 ". Он также может молчать, пока что-то происходит, потому что сканирование может не сработать или задержаться."),
("Klusums šeit nenozīmē, ka viss ir kārtībā.",
 "Молчание здесь не означает, что всё в порядке."),
("Sniegts tāds, kāds tas ir, bez garantijas par precizitāti, pilnīgumu vai pieejamību. Izmanto to kā vienu no vairākiem avotiem, nekad kā vienīgo.",
 "Предоставляется как есть, без гарантий точности, полноты или доступности. Используй его как один из нескольких источников, никогда как единственный."),
# --- escalation index -------------------------------------------------------
("Signāla novirzes indekss", "Индекс отклонения сигнала"),
("Cik tālu šodiena atrodas no ierastā", "Насколько сегодняшний день далёк от обычного"),
("Aprēķina vidējo no četriem neatkarīgi uzraudzītiem jēlsignāliem — GPS traucējumiem, AIS kuģu aktivitātes, militārajiem gaisa kuģiem un termiskajiem karstuma punktiem — salīdzinot ar katra signāla paša nesenā laika bāzes līmeni. Šis ir pašreizējās novirzes mērījums, nevis prognoze: tas nekad neietekmē augstāk redzamo WARN/WATCH/QUIET rezultātu un var rādīt paaugstinātu līmeni pat dienā, kad šis rezultāts paliek QUIET.",
 "Вычисляет среднее из четырёх независимо отслеживаемых исходных сигналов — помех GPS, судовой активности AIS, военных воздушных судов и термических очагов — по сравнению с собственным недавним базовым уровнем каждого сигнала. Это измерение текущего отклонения, а не прогноз: оно никогда не влияет на результат WARN/WATCH/QUIET выше и может показывать повышенный уровень даже в день, когда этот результат остаётся QUIET."),
("Pilns pārskats ↓", "Полный обзор ↓"),
("vs. 30 dienu bāzes līmenis", "против 30-дневного базового уровня"),
("signāli sniedza datus", "сигналов предоставили данные"),
# --- what it is -------------------------------------------------------------
("Izlasi vispirms", "Прочти сначала"),
("Kas tas ir — un kas nav", "Что это — и чем оно не является"),
("OSINT rīks — nav pārbaudīta izlūkinformācija un nav oficiāls avots",
 "Инструмент OSINT — не проверенные разведданные и не официальный источник"),
("Skenē publiskus avotus un vērtē tos pēc neatkarīga apstiprinājuma. Veidojis un uztur viens cilvēks; tas var kaut ko palaist garām un var kļūdīties.",
 "Сканирует публичные источники и оценивает их по независимому подтверждению. Создан и поддерживается одним человеком; он может что-то пропустить и может ошибиться."),
("Ko tas dara", "Что он делает"),
("OSINT (atklātā pirmkoda izlūkošanas) rīks: skenē publiskās ziņas, oficiālus valdības avotus un strukturētus notikumu datus, meklējot Baltijas/Krievijas drošības signālus, un vērtē rezultātus pēc tā, cik daudz neatkarīgu avotu apstiprina to pašu stāstu, pirms kaut kas tiek atzīmēts kā reāls brīdinājums. Viss šeit nāk no publiski pieejamiem avotiem — nekas slepens, nekas slēpts.",
 "Инструмент OSINT (разведки по открытым источникам): сканирует публичные новости, официальные государственные источники и структурированные данные о событиях в поисках сигналов безопасности по линии Балтия/Россия и оценивает результаты по тому, сколько независимых источников подтверждают одну и ту же историю, прежде чем что-либо будет отмечено как реальное предупреждение. Всё здесь берётся из общедоступных источников — ничего секретного, ничего скрытого."),
("Kas tas nav", "Чем он не является"),
("Nav oficiāls valdības, NATO vai izlūkošanas avots un nav ar tiem saistīts. Nav pārbaudīta izlūkinformācija vai nākotnes prognoze — tas ir viena cilvēka veidots un uzturēts atslēgvārdu un apstiprinājuma vērtēšanas rīks. Tas var kaut ko palaist garām un dažkārt kļūdīties.",
 "Не является официальным источником правительства, НАТО или разведки и не связан с ними. Это не проверенные разведданные и не прогноз будущего — это инструмент оценки по ключевым словам и подтверждению, созданный и поддерживаемый одним человеком. Он может что-то пропустить и иногда ошибаться."),
# --- method -----------------------------------------------------------------
("Kā signāls tiek vērtēts", "Как оценивается сигнал"),
("Katrs avots pieder uzticamības līmenim. Neviens atsevišķs avots nevar viens pats izraisīt reālu brīdinājumu — to dara tikai neatkarīgs apstiprinājums starp līmeņiem.",
 "Каждый источник принадлежит к уровню доверия. Ни один отдельный источник не может сам вызвать реальное предупреждение — это делает только независимое подтверждение между уровнями."),
("Avotu līmeņi un kā tie tiek sasniegti", "Уровни источников и как они достигаются"),
("Kuri avoti atrodas kurā uzticamības līmenī, cik to ir un kāpēc lielākā daļa nonāk caur vienu apkopotāju.",
 "Какие источники на каком уровне доверия, сколько их и почему большинство приходит через один агрегатор."),
("Līmenis", "Уровень"),
("Kas kvalificējas", "Что подходит"),
("Skaits", "Количество"),
("1. līmenis", "Уровень 1"),
("2. līmenis", "Уровень 2"),
("3. līmenis", "Уровень 3"),
("avoti", "источников"),
("Valsts drošības/izlūkošanas dienesti (Igaunija, Latvija, Lietuva, Somija, Zviedrija, Polija), NATO, ISW, ziņu aģentūras.",
 "Государственные службы безопасности/разведки (Эстония, Латвия, Литва, Финляндия, Швеция, Польша), НАТО, ISW, информационные агентства."),
("Valsts raidorganizācijas, drošības domnīcas, izmeklējošās žurnālistikas izdevumi.",
 "Общественные вещатели, аналитические центры по безопасности, издания расследовательской журналистики."),
("Dezinformācijas faktu pārbaudītāji, kā arī Krievijas valsts plašsaziņas līdzekļi/amatpersonas pašas — tiek sekots, lai redzētu naratīvu, nekad netiek uzskatīts par pierādījumu, nekad nevar izraisīt brīdinājumu.",
 "Фактчекеры дезинформации, а также сами российские государственные СМИ/официальные лица — отслеживаются, чтобы видеть нарратив, никогда не считаются доказательством, никогда не могут вызвать предупреждение."),
("Lielākā daļa avotu tiek sasniegti caur vienu ziņu apkopotāju, kas reizēm ir bloķējis visu skenēšanu uzreiz. Lai viens pārtraukums neatstātu monitoru aklu, papildus",
 "Большинство источников достигается через один новостной агрегатор, который иногда блокировал всё сканирование сразу. Чтобы один сбой не оставил монитор слепым, дополнительно"),
("plūsmas", "потоков"),
("tiek lasītas tieši no pašiem izdevumiem &mdash; to vidū Baltijas sabiedriskie mediji gan angļu, gan vietējā valodā un, tikpat svarīgi, primārie avoti, kas paši ziņotu par incidentu: aizsardzības ministrijas, zemessardzes, nacionālās kiberdrošības komandas un elektrības un gāzes pārvades operatori. Izdevums, kas sasniegts pa abiem ceļiem, joprojām skaitās viens avots, nevis pats savs apstiprinājums.",
 "читаются напрямую у самих изданий &mdash; среди них балтийские общественные СМИ на английском и на местных языках и, что не менее важно, первичные источники, которые сами сообщили бы об инциденте: министерства обороны, силы территориальной обороны, национальные команды кибербезопасности и операторы передачи электроэнергии и газа. Издание, достигнутое обоими путями, по-прежнему считается одним источником, а не собственным подтверждением."),
("Ko nozīmē QUIET, WATCH un WARN", "Что означают QUIET, WATCH и WARN"),
("Trīs līmeņi un kam jābūt patiesam, pirms katrs no tiem tiek izmantots.",
 "Три уровня и что должно быть верным, прежде чем будет использован каждый из них."),
("Šajā skenējumā netika atrasts nekas atbilstošs.",
 "В этом сканировании не найдено ничего релевантного."),
("Atbilstošs, bet vēl nav apstiprināts no neatkarīga avota.",
 "Релевантно, но ещё не подтверждено независимым источником."),
("Tas pats stāsts, kas apstiprināts neatkarīgi &mdash; vai nu no diviem dažādu uzticamības līmeņu avotiem, vai no trim atsevišķām redakcijām. Vārds vārdā pārpublicēts aģentūras ziņojums skaitās vienreiz.",
 "Та же история, подтверждённая независимо &mdash; либо двумя источниками разных уровней доверия, либо тремя отдельными редакциями. Дословно перепечатанное сообщение агентства считается один раз."),
("Kas tiek reģistrēts, bet", "Что регистрируется, но"),
("nepaaugstina", "не повышает"),
("līmeni", "уровень"),
("Kāpēc daļa būtiskā materiāla tiek reģistrēta kā konteksts, nevis sūtīta kā brīdinājums.",
 "Почему часть существенного материала регистрируется как контекст, а не отправляется как предупреждение."),
("Ne viss būtiskais kļūst par brīdinājumu. Ikdienišķs, iepriekš izsludināts, spekulatīvs vai jau atspoguļots materiāls tiek reģistrēts kā konteksts. Krievijas vai Baltkrievijas darbības nekad netiek uzskatītas par ikdienišķām.",
 "Не всё существенное становится предупреждением. Рутинный, заранее объявленный, спекулятивный или уже освещённый материал регистрируется как контекст. Действия России или Беларуси никогда не считаются рутинными."),
("Ko filtri patiešām apturēja", "Что фильтры действительно остановили"),
("Šie ieraksti paliek skenēšanas reģistrā kā konteksts. Iemesls ir vienkāršs: kanāls, kas ceļ trauksmi par visu, māca cilvēkus to ignorēt &mdash; un tad tiek ignorēts arī tas viens brīdinājums, kas patiešām ir svarīgs. Konkrēts ziņots incidents &mdash; pārrauts kabelis, robežu šķērsojošs drons &mdash; nekad netiek šādi atfiltrēts, pat ja tiek citēti amatpersonu mēģinājumi to mazināt.",
 "Эти записи остаются в журнале сканирования как контекст. Причина проста: канал, который поднимает тревогу по любому поводу, учит людей его игнорировать &mdash; и тогда игнорируется и то единственное предупреждение, которое действительно важно. Конкретный сообщённый инцидент &mdash; перебитый кабель, пересёкший границу дрон &mdash; никогда не отфильтровывается таким образом, даже если цитируются попытки официальных лиц его преуменьшить."),
# --- track record -----------------------------------------------------------
("Darbības vēsture", "История работы"),
("Dzīvs, nevis kurēts", "Живое, а не отобранное вручную"),
("Automātiski iegūts no tiem pašiem datiem, ko izmanto Telegram kanāls — nekas šeit netiek sagatavots atsevišķi šai lapai. Pilna pārbaude ir plānota 4x dienā, un ātrāka izdevēju plūsmu pārbaude notiek ik pēc 2 stundām; augstāk redzamais laiks nāk no pilnās pārbaudes. Neviena no tām nav nepārtraukta — lai gan GitHub bezmaksas plānotājs darbojas pēc labākās iespējas principa un lielas noslodzes laikā var palaist skenējumu vēlāk nekā plānots, dažkārt par vairākām stundām.",
 "Автоматически получено из тех же данных, что использует Telegram-канал — ничто здесь не готовится отдельно для этой страницы. Полная проверка запланирована 4 раза в день, а более быстрая проверка потоков изданий — каждые 2 часа; время выше берётся из полной проверки. Ни одна из них не является непрерывной — бесплатный планировщик GitHub работает по принципу максимальных усилий и при высокой нагрузке может запустить сканирование позже запланированного, иногда на несколько часов."),
("Reģistrētie skenējumi", "Зарегистрированные сканирования"),
("Klusums", "Тишина"),
("Novērošana", "Наблюдение"),
("Brīdinājums", "Предупреждение"),
("Labojumu īpatsvars", "Доля исправлений"),
("Signāla novirzes indekss laika gaitā", "Индекс отклонения сигнала во времени"),
("Vidējā novirze no bāzes līmeņa GPS traucējumiem, AIS, militārajiem gaisa kuģiem un termiskajiem karstuma punktiem (tiem, kuriem jau ir pietiekami daudz vēstures). Mērījums par to, cik tālu katrs skenējums atrodas no ierastā — nekad prognoze un nošķirts no WARN/WATCH/QUIET rezultāta.",
 "Среднее отклонение от базового уровня по помехам GPS, AIS, военным воздушным судам и термическим очагам (по тем, у кого уже достаточно истории). Измерение того, насколько каждое сканирование далеко от обычного — никогда не прогноз и отделено от результата WARN/WATCH/QUIET."),
("WATCH/WARN brīdinājumi laika gaitā", "Предупреждения WATCH/WARN во времени"),
("Katrs stabiņš ir viens skenējums, kas sasniedza WATCH (dzeltens) vai WARN (sarkans) līmeni; QUIET skenējumi stabiņu nerāda. Stabiņa augstums rāda, cik daudz atbilstošu vienību izraisīja šo skenējumu, nevis smaguma pakāpi.",
 "Каждый столбец — одно сканирование, достигшее уровня WATCH (жёлтый) или WARN (красный); сканирования QUIET столбца не показывают. Высота столбца показывает, сколько релевантных единиц вызвали это сканирование, а не степень серьёзности."),
("Eskalācijas intensitāte laika gaitā", "Интенсивность эскалации во времени"),
("Katrs punkts ir viens skenējums, iekrāsots pēc rezultāta (zaļš = klusums, dzeltens = novērošana, sarkans = brīdinājums). Līnija rāda GDELT vidējo ziņu toni, kur pieejams — jo augstāk līnija, jo satrauktāka/naidīgāka mediju atspoguļojums; nevis prognoze. Punktētā līnija ir 0 (neitrāls tonis), nevis diagrammas apakša — skenējumi, kuriem tajā reizē nav GDELT datu, pēc noklusējuma atrodas uz tās, nevis tāpēc, ka atspoguļojums patiešām būtu bijis neitrāls.",
 "Каждая точка — одно сканирование, окрашенное по результату (зелёный = тишина, жёлтый = наблюдение, красный = предупреждение). Линия показывает средний новостной тон GDELT, где он доступен — чем выше линия, тем тревожнее/враждебнее освещение в СМИ; это не прогноз. Пунктирная линия — это 0 (нейтральный тон), а не низ графика: сканирования, у которых в тот раз нет данных GDELT, по умолчанию оказываются на ней, а не потому, что освещение действительно было нейтральным."),
("Baumu/dezinformācijas izsekošana laika gaitā", "Отслеживание слухов/дезинформации во времени"),
("Cik baumu/dezinformācijas vienību (3. līmenis — nekad nevar pats izraisīt reālu brīdinājumu) tika izsekots katrā skenējumā.",
 "Сколько единиц слухов/дезинформации (уровень 3 — никогда не может сам вызвать реальное предупреждение) было отслежено в каждом сканировании."),
("GPS traucēšanas intensitāte laika gaitā", "Интенсивность помех GPS во времени"),
("Augsta traucējuma GPSJam šūnas, kas dienā atklātas Baltijas reģionā. Apkopotas no lidmašīnu ziņotās GPS precizitātes — korelē ar apzinātu traucēšanu, bet to neapstiprina.",
 "Ячейки GPSJam с высоким уровнем помех, обнаруженные за день в Балтийском регионе. Собраны по точности GPS, сообщаемой самолётами — коррелируют с преднамеренными помехами, но не подтверждают их."),
("AIS kuģu skaits laika gaitā", "Количество судов AIS во времени"),
("Skenējuma laikā īsā tiešraides AIS klausīšanās logā novēroti kuģi. Nav izsmeļošs pārklājums — tikai tie kuģi, kas šajā logā nejauši ziņoja.",
 "Суда, замеченные во время сканирования в коротком окне прямого прослушивания AIS. Это не исчерпывающий охват — только те суда, которые случайно передали сигнал в этом окне."),
("Militāro gaisa kuģu skaits laika gaitā", "Количество военных воздушных судов во времени"),
("Gaisa kuģi, kas skenējuma laikā raida ADS-B Baltijas reģionā. Daudzi militārie lidojumi lido ar izslēgtu vai viltotu signālu, tāpēc šis ir nepilnīgs priekšstats.",
 "Воздушные суда, передающие ADS-B в Балтийском регионе во время сканирования. Многие военные рейсы летают с выключенным или подменённым сигналом, поэтому картина неполная."),
("Termiskie karstuma punkti laika gaitā", "Термические очаги во времени"),
("Satelīta termiskās anomālijas, kas atklātas skenējuma laikā Baltijas reģionā. Neapstrādāti siltuma paraksta dati — meža ugunsgrēki un lauksaimniecības dedzināšana tos izraisa tikpat viegli kā jebkas cits.",
 "Спутниковые термические аномалии, обнаруженные во время сканирования в Балтийском регионе. Необработанные данные теплового следа — лесные пожары и сельскохозяйственные палы вызывают их так же легко, как что угодно другое."),
("Elektrotīkla pārtraukumi laika gaitā", "Отключения электросети во времени"),
("Piespiedu (neplānoti) ražošanas iekārtu pārtraukumi katrā skenējumā Igaunijā, Latvijā un Lietuvā, izmantojot ENTSO-E oficiālo ES pārtraukumu ziņošanas platformu. Gandrīz vienmēr parasta iekārtu kļūme, nevis sabotāža — zemūdens kabeļu/pārvades pārtraukumi vēl netiek aptverti.",
 "Вынужденные (незапланированные) отключения генерирующих мощностей в каждом сканировании в Эстонии, Латвии и Литве по данным ENTSO-E, официальной платформы ЕС для сообщений об отключениях. Почти всегда обычная неисправность оборудования, а не саботаж — подводные кабели и перебои передачи пока не охвачены."),
("Nesenā skenējumu vēsture", "Недавняя история сканирований"),
("Nesenu skenējumu ielāde…", "Загрузка недавних сканирований…"),
("Nesen atzīmētie notikumi — ar avotiem", "Недавно отмеченные события — с источниками"),
("Labojumu vēsture", "История исправлений"),
("Tiek pašu ziņots, kad tiek pamanīta kļūda — tas nav automatizēts audits. Tīra vēsture nozīmē, ka nekas vēl nav pamanīts un ziņots.",
 "Сообщается самостоятельно, когда ошибка замечена — это не автоматический аудит. Чистая история означает, что пока ничего не замечено и не сообщено."),
("Jaunumi", "Что нового"),
("Laika gaitā ieviesto funkciju un labojumu žurnāls vienkāršā valodā.",
 "Журнал внедрённых со временем функций и исправлений простым языком."),
("Dzīvais statuss īslaicīgi nav pieejams — pārbaudi pašreizējo statusu tieši Telegram kanālā.",
 "Живой статус временно недоступен — проверь текущий статус прямо в Telegram-канале."),
# --- FAQ --------------------------------------------------------------------
("Pirms jautā", "Прежде чем спросить"),
("Biežāk uzdotie jautājumi", "Часто задаваемые вопросы"),
("Kas notiek, ja jūs kļūdāties?", "Что происходит, если вы ошибаетесь?"),
("Kļūda tiek reģistrēta un publicēta kā labojums, nevis klusi izlabota — augstāk redzamais saraksts ir pilnīgs pārskats par to, kas tā ziņots. Reizēm kļūdīties un to atklāti atzīt ir uzticamāk nekā aizdomīgi nevainojama vēsture. Viens godīgs ierobežojums: šis nav automatizēts audits — labojums parādās tikai tad, ja kļūda tiešām tiek pamanīta un manuāli ziņota. Tīra vēsture nozīmē, ka nekas vēl nav pamanīts un ziņots, nevis formālu garantiju par nulles kļūdām. Iepriekš redzamais „labojumu īpatsvars“ ir labojumu skaits dalīts ar skenēšanu skaitu, mēroga izpratnei — nevis neatkarīgi pārbaudīts precizitātes rādītājs.",
 "Ошибка регистрируется и публикуется как исправление, а не исправляется молча — список выше является полным обзором того, о чём сообщено. Иногда ошибиться и открыто это признать надёжнее, чем подозрительно безупречная история. Одно честное ограничение: это не автоматический аудит — исправление появляется только тогда, когда ошибка действительно замечена и сообщена вручную. Чистая история означает, что пока ничего не замечено и не сообщено, а не формальную гарантию нулевых ошибок. Показанная выше «доля исправлений» — это количество исправлений, делённое на количество сканирований, для понимания масштаба, а не независимо проверённый показатель точности."),
("Ko nozīmē GDELT klasifikācijas kodi un „Goldsteina“ rādītājs, ko dažkārt redzu?",
 "Что означают коды классификации GDELT и показатель «Гольдштейна», который я иногда вижу?"),
("Ko nozīmē „N avots(i) nav sasniedzami”?", "Что означает «N источник(ов) недоступны»?"),
("Kāpēc jūs neuzskaitāt precīzos avotus?", "Почему вы не перечисляете точные источники?"),
("Vai jūs redzat, kas seko šim kanālam?", "Видите ли вы, кто подписан на этот канал?"),
("Kas notiek, ja pēc iespējošanas nesaņemu pārlūkprogrammas paziņojumus?",
 "Что делать, если после включения я не получаю уведомления браузера?"),
("Vai tas paliks bezmaksas?", "Останется ли это бесплатным?"),
("finansējuma lapā", "на странице финансирования"),
("Vai šī ir oficiāla brīdināšanas sistēma?", "Это официальная система оповещения?"),
("Nē. Ja uztraucaties par reālu ārkārtas situāciju, vienmēr vispirms pārbaudiet savas valsts oficiālos kanālus: Igaunija — kriis.ee · Latvija — vugd.gov.lv · Lietuva — lrv.lt.",
 "Нет. Если вы обеспокоены реальной чрезвычайной ситуацией, всегда сначала проверяйте официальные каналы своей страны: Эстония — kriis.ee · Латвия — vugd.gov.lv · Литва — lrv.lt."),
# --- other ways to follow ---------------------------------------------------
("Citi veidi, kā sekot līdzi", "Другие способы следить"),
("RSS plūsma", "RSS-лента"),
("Dod priekšroku savai lasītājprogrammai, nevis Telegram vai pārlūkprogrammas paziņojumiem?",
 "Предпочитаешь свою читалку Telegram или уведомлениям браузера?"),
("Piesakies RSS plūsmai", "Подпишись на RSS-ленту"),
("— tie paši atzīmētie notikumi, konts nav nepieciešams.",
 "— те же отмеченные события, аккаунт не нужен."),
("Vai veic savu analīzi? Lejupielādē šī projekta paša vēsturi CSV formātā:",
 "Проводишь собственный анализ? Скачай собственную историю этого проекта в формате CSV:"),
("skenēšanas līmeņa vēsture", "история уровней сканирования"),
("(līmenis, avotu skaits katrā skenējumā) un", "(уровень, количество источников в каждом сканировании) и"),
("(novirzes rādītājs katrā skenējumā). Tie paši dati, kas ir aiz iepriekš redzamajiem grafikiem, brīvi izmantojami.",
 "(показатель отклонения в каждом сканировании). Те же данные, что стоят за графиками выше, свободны для использования."),
("Baltic Signal Monitor ir neatkarīgs, personīgi izveidots monitoringa rīks — izveidojis un uztur Latvijas pilsonis visa Baltijas jūras reģiona sirdsmiera labad. Tas nav oficiāls valdības, NATO vai izlūkošanas avots un nav ar tiem saistīts. Labojumi tiek reģistrēti un publicēti atklāti, nevis slēpti.",
 "Baltic Signal Monitor — независимый, созданный частным лицом инструмент мониторинга, созданный и поддерживаемый гражданином Латвии ради спокойствия всего региона Балтийского моря. Он не является официальным источником правительства, НАТО или разведки и не связан с ними. Исправления регистрируются и публикуются открыто, а не скрываются."),
("Dzīvie dati tiek ielādēti automātiski katrā apmeklējumā.",
 "Живые данные загружаются автоматически при каждом посещении."),
("Atradi drošības problēmu?", "Нашёл проблему безопасности?"),
("Privātums", "Приватность"),
("Finansējums", "Финансирование"),
]

# Long FAQ answers, kept out of the list above only for readability.
PAIRS += [
("GDELT ir publiska datubāze, kas automātiski kodē pasaules politiskās un konfliktu ziņas strukturētās kategorijās, ar standarta smaguma novērtējumu, ko sauc par Goldsteina skalu (-10 līdz +10 — jo negatīvāks, jo naidīgāks/konfliktējošāks). Kad atzīmētā vienība nāk no GDELT, tās kategorija un Goldsteina rādītājs tiek parādīti līdzās kā papildu konteksts. Tā ir tikai papildu informācija par vienību, kas jau ir kvalificējusies: jebkura šeit redzamā GDELT vienība jau ir izgājusi tieši tādas pašas atbilstības un apstiprinājuma pārbaudes kā jebkura cita atzīmētā vienība šajā lapā — tie nav neapstrādāti vai nefiltrēti dati. (Kad tiek publicēts WATCH vai WARN, Telegram kanāls automātiski pievieno karti — taču tā parāda tikai konkrētos notikumus, kas izraisīja šo brīdinājumu, nevis vispārēju reģiona momentuzņēmumu.)",
 "GDELT — это публичная база данных, которая автоматически кодирует мировые политические и конфликтные новости в структурированные категории, со стандартной оценкой серьёзности, называемой шкалой Гольдштейна (от -10 до +10 — чем отрицательнее, тем враждебнее/конфликтнее). Когда отмеченная единица приходит из GDELT, её категория и показатель Гольдштейна отображаются рядом как дополнительный контекст. Это лишь дополнительная информация о единице, которая уже прошла отбор: любая видимая здесь единица GDELT уже прошла точно такие же проверки релевантности и подтверждения, как и любая другая отмеченная единица на этой странице — это не сырые и не нефильтрованные данные. (Когда публикуется WATCH или WARN, Telegram-канал автоматически добавляет карту — но она показывает только конкретные события, вызвавшие это предупреждение, а не общий снимок региона.)"),
("Avota plūsma neatbildēja šī skenējuma laikā — parasti tas ir parasts, atsevišķs traucējums. Reizēm uzreiz neizdodas liela avotu grupa: šis projekts darbojas uz bezmaksas, koplietotas mitināšanas (GitHub Actions), un šim koplietotajam serveru klāsteram dažkārt tiek piešķirts serveris, kura IP adresi Google jau ir ierobežojis cita, nesaistīta iemesla dēļ — tas vienlaicīgi bloķē visus Google News avotus vienā skenējumā. Kad tas tiek atklāts, skenējums to tagad atpazīst apmēram minūtes laikā un automātiski mēģina vēlreiz citā serverī, nevis gaida nākamo plānoto skenējumu. Jebkurā gadījumā tas nozīmē, ka šis rezultāts var būt mazāk pilnīgs nekā parasti — nevis ka kaut kas tika slēpts. Mēs labāk to parādām, nekā ļaujam klusuma rezultātam bojāta skenējuma laikā izskatīties identiskam ar reālu \"viss kārtībā\" stāvokli.",
 "Поток источника не ответил во время этого сканирования — обычно это рядовой единичный сбой. Иногда сразу отказывает большая группа источников: этот проект работает на бесплатном, совместно используемом хостинге (GitHub Actions), и этому общему кластеру иногда выделяется сервер, IP-адрес которого Google уже ограничил по другой, не связанной причине — это одновременно блокирует все источники Google News в одном сканировании. Когда это обнаруживается, сканирование теперь распознаёт это примерно за минуту и автоматически повторяет попытку на другом сервере, а не ждёт следующего запланированного сканирования. В любом случае это означает, что данный результат может быть менее полным, чем обычно — а не что что-то было скрыто. Мы лучше это покажем, чем позволим результату тишины при сломанном сканировании выглядеть идентично настоящему состоянию «всё в порядке»."),
("Lai vērtēšanas sistēmu nevarētu izspēlēt — precīza to izdevumu nosaukšana, kas var izraisīt brīdinājumu, ļautu kādam mērķtiecīgi izmantot tieši tos avotus, kas ir svarīgi. Līmenis un skaits ir publiski; brīdī, kad avots tiešām rada reālu WATCH/WARN, tiek parādīts arī tā nosaukums un saite (skatīt „Nesen atzīmētie notikumi“ iepriekš).",
 "Чтобы систему оценки нельзя было обыграть — точное называние изданий, способных вызвать предупреждение, позволило бы кому-то целенаправленно использовать именно те источники, которые имеют значение. Уровень и количество публичны; в момент, когда источник действительно создаёт реальный WATCH/WARN, показываются и его название, и ссылка (см. «Недавно отмеченные события» выше)."),
("Telegram — jā, kā kanāla administrators, tas ir normāli jebkuram Telegram kanāla īpašniekam, nevis kaut kas šim projektam īpaši izveidots. Pārlūkprogrammas push abonenti ir citādi: viņiem nav pievienots vārds vai identitāte, tikai anonīms ierīces marķieris, tāpēc es nevaru redzēt, kas viņi ir. Citi Telegram abonenti neredz cits citu, un nekas netiek eksportēts, glabāts citur, pārdots vai kopīgots ārpus paša Telegram.",
 "Telegram — да, как администратор канала; это нормально для любого владельца Telegram-канала, а не что-то созданное специально для этого проекта. С push-подписчиками браузера иначе: к ним не привязаны имя или личность, только анонимный маркер устройства, поэтому я не могу видеть, кто они. Другие подписчики Telegram не видят друг друга, и ничто не экспортируется, не хранится где-то ещё, не продаётся и не передаётся за пределы самого Telegram."),
("Mobilās pārlūkprogrammas šeit var būt nekonsekventas — tālruņa akumulatora optimizācija vai pārlūkprogrammas pašas vietnes paziņojumu iestatījums var klusi apslāpēt paziņojumus bez jebkādas kļūdas parādīšanas. Visbiežākais iemesls: pārbaudi, vai šīs vietnes paziņojumi nav apklusināti tieši tavas pārlūkprogrammas iestatījumos (nevis tikai tālruņa sistēmas iestatījumos) — parasti tas ir tas.",
 "Мобильные браузеры здесь могут вести себя непоследовательно — оптимизация батареи телефона или собственная настройка уведомлений сайта в браузере могут молча заглушить уведомления, не показав никакой ошибки. Самая частая причина: проверь, не отключены ли уведомления этого сайта именно в настройках твоего браузера (а не только в системных настройках телефона) — обычно дело в этом."),
("Jā. Ir pieejama brīvprātīga atbalsta poga (Ko-fi) tiem, kas vēlas atbalstīt projektu — tā nedod nevienam ātrākus vai labākus brīdinājumus; visi saņem tieši to pašu, tajā pašā laikā, neatkarīgi no tā. Kas projektu finansē — pašlaik neviens — ir pilnībā uzskaitīts",
 "Да. Есть добровольная кнопка поддержки (Ko-fi) для тех, кто хочет поддержать проект — она никому не даёт более быстрых или более качественных предупреждений; все получают ровно то же самое, в то же время, независимо от неё. Кто финансирует проект — на данный момент никто — полностью перечислено"),
]


# The source mixes straight and typographic quotes for the same role, and the
# extracted strings normalised them. Treat any of them as interchangeable so a
# quote style mismatch cannot silently drop a whole paragraph.
_QUOTES = '"\u201e\u201c\u201d'
_QUOTE_CLASS = '["\u201e\u201c\u201d]'


# Head metadata and anything else outside a rendered text node. Plain
# substring replacement: these are single-line attribute values.
HEAD_PAIRS = [
    ("Neatkar\u012bgi Baltijas dro\u0161\u012bbas sign\u0101li",
     "\u041d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u044b\u0435 \u0441\u0438\u0433\u043d\u0430\u043b\u044b \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u0438 \u0411\u0430\u043b\u0442\u0438\u0438"),
    ('Bezmaksas, neatkarīgs OSINT (atklātā pirmkoda izlūkošana) agrīnās brīdināšanas kanāls, kas seko Baltijas jūras reģiona un Krievijas drošības signāliem, izmantojot desmitiem uzticamu avotu — oficiālus dienestus, ziņu aģentūras un dezinformācijas izsekotājus. Nav saistīts ar nevienu valdību.',
     'Бесплатный независимый канал раннего предупреждения на основе OSINT (разведка по открытым источникам), который отслеживает сигналы безопасности в регионе Балтийского моря и в России по десяткам надёжных источников — официальным службам, новостным агентствам и трекерам дезинформации. Не связан ни с одним правительством.'),
    ('Bezmaksas, neatkarīgs OSINT agrīnās brīdināšanas kanāls, kas seko Baltijas jūras reģiona un Krievijas drošības signāliem, izmantojot desmitiem uzticamu avotu.',
     'Бесплатный независимый канал раннего предупреждения на основе OSINT, который отслеживает сигналы безопасности в регионе Балтийского моря и в России по десяткам надёжных источников.'),
    # An inline link label the text pass missed because it sits inside a
    # sentence that was translated around it.
    ("sign\u0101la novirzes indekss",
     "\u0438\u043d\u0434\u0435\u043a\u0441 \u043e\u0442\u043a\u043b\u043e\u043d\u0435\u043d\u0438\u044f \u0441\u0438\u0433\u043d\u0430\u043b\u0430"),
]


def flexible(s):
    """Pattern matching the string with any whitespace run between words."""
    words = []
    for word in s.split():
        words.append("".join(_QUOTE_CLASS if ch in _QUOTES else re.escape(ch)
                             for ch in word))
    return re.compile(r"\s+".join(words))


# <script> and <style> blocks, so the prose pass can be kept out of them.
_CODE_RE = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)


def split_code(text):
    """[(is_code, chunk), ...] covering the whole document in order.

    The prose pass must not run inside JavaScript. Several prose strings are
    substrings of JS literals, and a partial hit there produces a half-Latvian
    half-Russian sentence at runtime — worse than leaving it alone, because
    nothing in the source looks wrong."""
    out, pos = [], 0
    for m in _CODE_RE.finditer(text):
        if m.start() > pos:
            out.append((False, text[pos:m.start()]))
        out.append((True, m.group(0)))
        pos = m.end()
    out.append((False, text[pos:]))
    return out


def main():
    source = io.open(SRC, encoding="utf-8").read()
    missed = []

    chunks = split_code(source)
    prose = "".join(c for is_code, c in chunks if not is_code)

    # Longest first. Several pairs are prefixes or substrings of longer ones
    # (a heading repeated inside a caption); replacing the short one first
    # would leave the long one unmatchable and silently untranslated.
    ordered = sorted(PAIRS, key=lambda pair: -len(pair[0]))
    for lv, ru in ordered:
        if not flexible(lv).search(prose):
            missed.append(lv)
    rebuilt = []
    for is_code, chunk in chunks:
        if is_code:
            for lv, ru in sorted(SCRIPT_PAIRS, key=lambda pair: -len(pair[0])):
                chunk = chunk.replace(lv, ru)
            for lv, ru in SCRIPT_REWRITES:
                chunk = chunk.replace(lv, ru)
        else:
            for lv, ru in ordered:
                chunk = flexible(lv).sub(lambda m, r=ru: r, chunk)
        rebuilt.append(chunk)
    t = "".join(rebuilt)

    # The script table is checked against the original, not the rebuilt text:
    # once applied, a pair is gone by construction.
    code = "".join(c for is_code, c in chunks if is_code)
    for lv, ru in SCRIPT_PAIRS + SCRIPT_REWRITES:
        if lv not in code:
            missed.append("[script] " + lv)

    # Language switcher: mark RU active, and add RU to the list.
    t = re.sub(r'<span class="lang-switch">.*?</span>',
               '<span class="lang-switch">\n        <a href="/">EN</a> · '
               '<a href="/et/">ET</a> · <a href="/lv/">LV</a> · '
               '<a href="/lt/">LT</a> · <a href="/ru/" class="active">RU</a>\n      </span>',
               t, flags=re.S, count=1)
    t = t.replace('<html lang="lv"', '<html lang="ru"')

    # --- Head metadata -----------------------------------------------------
    # The visible-text pass above cannot reach these: they live in attributes
    # that never render, and a page whose <title>, canonical and hreflang all
    # still say "lv" is a duplicate of the Latvian page as far as any search
    # engine or link preview is concerned.
    for lv, ru in HEAD_PAIRS:
        if lv not in t:
            missed.append("[head] " + lv)
            continue
        t = t.replace(lv, ru)

    # This page's own address, everywhere it is asserted.
    t = t.replace("https://balticsignalmonitor.com/lv/\">",
                  "https://balticsignalmonitor.com/ru/\">")
    t = t.replace('"url": "https://balticsignalmonitor.com/lv/"',
                  '"url": "https://balticsignalmonitor.com/ru/"')
    t = t.replace('"inLanguage": "lv"', '"inLanguage": "ru"')
    # ...but the hreflang set must keep pointing at every language, and gain
    # this one. Restore the lv alternate the blanket rewrite just moved, and
    # add ru beside it.
    t = t.replace(
        '<link rel="alternate" hreflang="lv" href="https://balticsignalmonitor.com/ru/">',
        '<link rel="alternate" hreflang="lv" href="https://balticsignalmonitor.com/lv/">')
    ru_alt = '<link rel="alternate" hreflang="ru" href="https://balticsignalmonitor.com/ru/">'
    if ru_alt not in t:
        t = t.replace(
            '<link rel="alternate" hreflang="lt" href="https://balticsignalmonitor.com/lt/">',
            '<link rel="alternate" hreflang="lt" href="https://balticsignalmonitor.com/lt/">\n'
            + ru_alt)
    # The wordmark is "back to the top of THIS language".
    t = t.replace('<a class="wordmark" href="/lv/"',
                  '<a class="wordmark" href="/ru/"')
    # Sibling links from this page point at siblings of ru/, not lv/.
    t = t.replace('href="/lv/privacy/"', 'href="/ru/privacy/"')
    t = t.replace('href="/lv/funding/"', 'href="/ru/funding/"')

    io.open(DST, "w", encoding="utf-8").write(t)
    print("wrote %s (%d bytes)" % (DST, len(t)))
    total = len(PAIRS) + len(HEAD_PAIRS) + len(SCRIPT_PAIRS) + len(SCRIPT_REWRITES)
    print("pairs applied: %d / %d" % (total - len(missed), total))
    for m in missed:
        print("  MISSED: %r" % m[:88])
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
