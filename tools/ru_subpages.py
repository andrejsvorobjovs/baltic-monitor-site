# -*- coding: utf-8 -*-
"""Build ru/privacy/ and ru/funding/ from their Latvian originals.

Same approach as ru_index.py and for the same reason: the Latvian pages are
the ones written for a reader inside the region. These two are mostly static
prose with no JavaScript strings, so the whole job is one whitespace-tolerant
pass per page plus the head metadata and the link rewiring.

A privacy page that is wrong is worse than no privacy page, so nothing here
is paraphrased: every GDPR clause, retention period, legal basis and
supervisory-authority name is carried over exactly as the Latvian page states
it. Any pair that fails to match fails the build.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_QUOTES = '"„“”'
_QUOTE_CLASS = '["„“”]'


def flexible(s):
    words = []
    for word in s.split():
        words.append("".join(_QUOTE_CLASS if ch in _QUOTES else re.escape(ch)
                             for ch in word))
    return re.compile(r"\s+".join(words))


PRIVACY = [
    ("Privātums — Baltic Signal Monitor", "Приватность — Baltic Signal Monitor"),
    ("Ko Baltic Signal Monitor vāc, ko nevāc un kas ko redz — izskaidrots vienkārši, nevis juridiskā valodā.",
     "Что Baltic Signal Monitor собирает, чего не собирает и кто что видит — объяснено простым языком, а не юридическим."),
    ("Metode", "Метод"),
    ("Statuss", "Статус"),
    ("BUJ", "Вопросы"),
    ("Privātums", "Приватность"),
    ("Ko šis projekts vāc — un ko nevāc",
     "Что этот проект собирает — и чего не собирает"),
    ("Aiz šī nestāv juridiska komanda — to veido un uztur viena persona. Tāpēc standarta juridiska teksta vietā šeit ir tiešs skaidrojums par to, kādus datus šis projekts skar un ko tas apzināti nekad nedara.",
     "За этим не стоит юридическая команда — проект создаёт и ведёт один человек. Поэтому вместо стандартного юридического текста здесь прямое объяснение того, каких данных этот проект касается и чего он сознательно никогда не делает."),
    ("Īsā versija:", "Коротко:"),
    ("nav reklāmu, analītikas, izsekošanas skriptu vai sīkdatņu. Nekas netiek pārdots vai kopīgots ar kādu. Tiek vākti tikai minimāli dati, kas nepieciešami paziņojuma piegādei — nekas cits.",
     "нет рекламы, аналитики, скриптов слежения и файлов cookie. Ничего не продаётся и ни с кем не передаётся. Собираются только минимальные данные, необходимые для доставки уведомления — ничего больше."),
    ("Ja seko līdzi Telegram", "Если следишь через Telegram"),
    ("Pievienošanās Telegram kanālam ir parasta Telegram abonēšana — tāda pati attiecība, kāda tev būtu ar jebkuru publisku kanālu. Kā kanāla administrators, es redzu, kas ir abonējis; tā ir standarta Telegram funkcionalitāte, nevis kaut kas, kas veidots tieši šim projektam, un kaut kas, ko es nevaru izslēgt. Citi abonenti nevar redzēt viens otru, un abonentu saraksts nekad netiek eksportēts, glabāts citur, pārdots vai kopīgots vairāk, nekā Telegram pats jau nodrošina jebkuram kanāla īpašniekam. Lai pārtrauktu, vienkārši pamet vai apklusini kanālu Telegram — ārpus Telegram nekas netiek glabāts, ko atsevišķi dzēst.",
     "Подписка на Telegram-канал — это обычная подписка в Telegram, такие же отношения, какие были бы у тебя с любым публичным каналом. Как администратор канала я вижу, кто подписался; это стандартная функция Telegram, а не что-то сделанное специально для этого проекта, и что-то, что я не могу отключить. Другие подписчики не видят друг друга, а список подписчиков никогда не экспортируется, не хранится где-либо ещё, не продаётся и не передаётся дальше того, что сам Telegram уже даёт любому владельцу канала. Чтобы прекратить, просто покинь или заглуши канал в Telegram — за пределами Telegram ничего не хранится, что нужно было бы удалять отдельно."),
    ("Ja seko līdzi Mastodon", "Если следишь через Mastodon"),
    ("Sekošana Mastodon kontam ir parasta Mastodon sekošana — tādas pašas attiecības, kādas tev būtu ar jebkuru publisku kontu. Kā konta īpašnieks, es redzu, kas seko; tā ir standarta Mastodon funkcionalitāte, nevis kaut kas, kas veidots tieši šim projektam, un kaut kas, ko es nevaru izslēgt. Sekotāju saraksts nekad netiek eksportēts, glabāts citur, pārdots vai kopīgots vairāk, nekā Mastodon pats jau nodrošina jebkuram konta īpašniekam. Kurš serveris mitina tavu Mastodon kontu, ir tavs, nevis šī projekta izvēle, un uz to attiecas šī servera privātuma politika. Lai pārtrauktu, vienkārši pārtrauc sekot — ārpus Mastodon nekas netiek glabāts, ko atsevišķi dzēst.",
     "Подписка на аккаунт в Mastodon — это обычная подписка в Mastodon, такие же отношения, какие были бы у тебя с любым публичным аккаунтом. Как владелец аккаунта я вижу, кто подписан; это стандартная функция Mastodon, а не что-то сделанное специально для этого проекта, и что-то, что я не могу отключить. Список подписчиков никогда не экспортируется, не хранится где-либо ещё, не продаётся и не передаётся дальше того, что сам Mastodon уже даёт любому владельцу аккаунта. Какой сервер размещает твой аккаунт в Mastodon — твой выбор, а не этого проекта, и на него распространяется политика приватности того сервера. Чтобы прекратить, просто отпишись — за пределами Mastodon ничего не хранится, что нужно было бы удалять отдельно."),
    ("Ja izmanto pārlūka push paziņojumus",
     "Если используешь push-уведомления браузера"),
    ("Nospiežot pogu „Iespējot pārlūka paziņojumus“, tiek izveidots anonīms abonements: nejauši ģenerēta tīmekļa adrese un šifrēšanas atslēga, ko izveido tavs pārlūks (Chrome, Firefox, Safari u.c.) — nevis šis projekts. Tam nav pievienots ne vārds, ne e-pasts, ne jebkāda veida konts; šim projektam nav iespējas noteikt, kas ir aiz konkrētā abonementa.",
     "При нажатии кнопки «Включить уведомления браузера» создаётся анонимная подписка: случайно сгенерированный веб-адрес и ключ шифрования, которые создаёт твой браузер (Chrome, Firefox, Safari и т. д.) — а не этот проект. К ней не привязано ни имя, ни адрес электронной почты, ни какая-либо учётная запись; у этого проекта нет возможности определить, кто стоит за конкретной подпиской."),
    ("Šis abonements tiek glabāts nelielā datubāzē (Upstash Redis, pieejama caur Vercel) tieši viena iemesla dēļ: lai zinātu, kur piegādāt paziņojumu. Tas tiek automātiski dzēsts — atkarībā no tā, kas notiek pirmais: piegāde tam galīgi neizdodas (pārlūks atinstalēts, atļauja atsaukta, ierīce pazudusi), vai tas vienkārši kļūst gadu vecs, neatkarīgi no tā, vai tas joprojām darbojas. Nekas netiek glabāts bezgalīgi. Lai ātrāk pārtrauktu saņemt paziņojumus, atspējo šīs vietnes paziņojumus sava pārlūka iestatījumos; abonements kļūst nederīgs mūsu pusē un tiek iztīrīts automātiski tādā pašā veidā.",
     "Эта подписка хранится в небольшой базе данных (Upstash Redis, доступной через Vercel) ровно по одной причине: чтобы знать, куда доставить уведомление. Она удаляется автоматически — в зависимости от того, что произойдёт раньше: доставка к ней окончательно перестаёт удаваться (браузер удалён, разрешение отозвано, устройство потеряно), либо ей просто исполняется год, независимо от того, работает она ещё или нет. Ничего не хранится бесконечно. Чтобы перестать получать уведомления быстрее, отключи уведомления этого сайта в настройках своего браузера; подписка становится недействительной на нашей стороне и вычищается автоматически тем же образом."),
    ("Projekta pārzinis var arī redzēt, cik abonementu pašlaik ir saglabāti, un tos dzēst, izmantojot ar paroli aizsargātu administrēšanas lapu — tur netiek atklāta nekāda papildu identificējoša informācija, kas nebūtu jau aprakstīta šajā lapā.",
     "Ответственный за проект также может видеть, сколько подписок хранится в данный момент, и удалять их через защищённую паролем административную страницу — там не раскрывается никакая дополнительная идентифицирующая информация, не описанная уже на этой странице."),
    ("Abonēšanas brīdī notiek vēl kaut kas, ko ir vērts nosaukt: serveris saskaita, cik abonēšanas mēģinājumu pēdējās stundas laikā nākuši no tavas IP adreses, lai neviens nevarētu pārpludināt sarakstu. Šis skaitītājs ir vienīgais, kas tiek glabāts pie adreses, tas nekad netiek piesaistīts tavam abonementam, un pēc stundas tiek automātiski dzēsts.",
     "В момент подписки происходит ещё одно, о чём стоит сказать прямо: сервер считает, сколько попыток подписки за последний час пришло с твоего IP-адреса, чтобы никто не мог затопить список. Этот счётчик — единственное, что хранится рядом с адресом, он никогда не связывается с твоей подпиской и через час удаляется автоматически."),
    ("Pati vietne", "Сам сайт"),
    ("balticsignalmonitor.com apmeklēšana neuzstāda sīkdatnes, nedarbina analītiku un nekādā veidā neizseko apmeklētājus. Lapā redzamie reāllaika skaitļi rodas no tā, ka tavs pārlūks ielādē nelielu publisku statusa failu (",
     "Посещение balticsignalmonitor.com не устанавливает файлов cookie, не запускает аналитику и никак не отслеживает посетителей. Цифры в реальном времени на странице появляются потому, что твой браузер загружает небольшой публичный файл статуса ("),
    (") — parasts faila pieprasījums, kas neatšķiras no attēla ielādes.",
     ") — обычный запрос файла, ничем не отличающийся от загрузки изображения."),
    ("Trešās puses, no kurām šis projekts ir atkarīgs",
     "Третьи стороны, от которых зависит этот проект"),
    ("— mitina šo vietni.", "— размещает этот сайт."),
    ("— nodrošina iepriekš aprakstīto kanālu.",
     "— обеспечивает описанный выше канал."),
    ("— nodrošina iepriekš aprakstīto izvēles kontu, ko mitina serveris, kuru izmanto tā sekošanai, nevis šis projekts.",
     "— обеспечивает описанный выше необязательный аккаунт, размещённый на сервере, который выбирает тот, кто подписывается, а не этот проект."),
    ("— mitina un glabā pārlūka push abonementus tieši tā, kā aprakstīts iepriekš.",
     "— размещает и хранит push-подписки браузера ровно так, как описано выше."),
    ("— izvēles poga „Atbalsti šo projektu“. Ko-fi redz kaut ko tikai tad, ja izvēlies to nospiest un izmantot; šis darījums ir pakļauts Ko-fi pašas privātuma politikai, nevis šī projekta politikai.",
     "— необязательная кнопка «Поддержать проект». Ko-fi видит что-либо только в том случае, если ты решишь на неё нажать и ею воспользоваться; эта операция подчиняется собственной политике приватности Ko-fi, а не политике этого проекта."),
    ("Neviena no tām nesaņem vairāk datu, kā aprakstīts šajā lapā, un šis projekts nepievieno nekādu papildu izsekošanu tam, ko katra no tām jau dara pati par sevi.",
     "Ни одна из них не получает больше данных, чем описано на этой странице, и этот проект не добавляет никакого дополнительного отслеживания к тому, что каждая из них уже делает сама по себе."),
    ("Tavas tiesības un kas par to atbild", "Твои права и кто за это отвечает"),
    ("Šo projektu uztur viens privāts cilvēks, nevis uzņēmums, un tieši šis cilvēks ir datu pārzinis visam, kas aprakstīts augstāk. Nav neviena cita operatora un neviena trešās puses, kas rīkotos viņa vārdā, izņemot iepriekšējā sadaļā nosauktos pakalpojumus. Sazinies:",
     "Этот проект ведёт один частный человек, а не компания, и именно этот человек является контролёром данных для всего описанного выше. Нет никакого другого оператора и никакой третьей стороны, действующей от его имени, кроме сервисов, названных в предыдущем разделе. Для связи:"),
    ("Tiek apstrādātas divas lietas, un katrai ir savs pamats. Pārlūka push darbojas uz",
     "Обрабатываются две вещи, и у каждой своё основание. Push в браузере работает на основании"),
    ("tavas piekrišanas", "твоего согласия"),
    ("pamata, ko dod, nospiežot „Ieslēgt pārlūka brīdinājumus“, un ko jebkurā brīdī vari atsaukt, izslēdzot paziņojumus pārlūkā — iemesls nav jānorāda, un nekas netiek saglabāts, tiklīdz abonements pārstāj darboties. Stundas IP skaitītājs darbojas uz",
     ", которое даётся нажатием «Включить предупреждения в браузере» и которое в любой момент можно отозвать, отключив уведомления в браузере — причину указывать не нужно, и ничего не сохраняется с того момента, как подписка перестаёт работать. Часовой счётчик IP работает на основании"),
    ("leģitīmo interešu", "законных интересов"),
    ("pamata: uzturēt sarakstu lietojamu pārējiem.",
     ": сохранять список пригодным для остальных."),
    ("Saskaņā ar VDAR tu vari jautāt, kas par tevi tiek glabāts, pieprasīt to dzēst, iebilst pret apstrādi vai lūgt kopiju. Raksti uz augstāk norādīto adresi, un saņemsi atbildi. Praksē nodot ir ļoti maz — push abonementam nav pievienots ne vārds, ne e-pasts, ne konts, tāpēc parasti to nemaz nevar sasaistīt ar cilvēku bez tieši tā abonementa, kas ir tavā pārlūkā.",
     "Согласно GDPR ты можешь спросить, что о тебе хранится, потребовать это удалить, возразить против обработки или попросить копию. Напиши на указанный выше адрес, и получишь ответ. На практике передавать почти нечего — к push-подписке не привязано ни имя, ни адрес электронной почты, ни учётная запись, поэтому обычно её вообще нельзя связать с человеком без именно той подписки, которая находится в твоём браузере."),
    ("Ja atbilde tevi neapmierina, vari iesniegt sūdzību savas valsts datu aizsardzības iestādē: Igaunijā",
     "Если ответ тебя не устроит, можешь подать жалобу в орган по защите данных своей страны: в Эстонии"),
    ("Latvijā", "в Латвии"),
    ("Lietuvā", "в Литве"),
    ("Jautājumi", "Вопросы"),
    ("Šis ir vienas personas, nekomerciāls projekts — ja tev ir jautājums par kaut ko šajā lapā vai vēlies, lai kaut kas tiktu pārbaudīts, raksti uz",
     "Это некоммерческий проект одного человека — если у тебя есть вопрос о чём-то на этой странице или ты хочешь, чтобы что-то проверили, напиши на"),
    ("← Atpakaļ uz sākumlapu", "← Назад на главную"),
    ("Baltic Signal Monitor ir neatkarīgs, personīgi veidots pārraudzības rīks — nevis oficiāls valdības, NATO vai izlūkošanas avots, un nav saistīts ar nevienu no tiem.",
     "Baltic Signal Monitor — независимый инструмент наблюдения, созданный частным лицом, а не официальный источник правительства, НАТО или разведки, и не связан ни с одним из них."),
    ("Atklāji drošības problēmu?", "Нашёл проблему безопасности?"),
    ("Finansējums", "Финансирование"),
    ("Baltic Signal Monitor — sākumlapa", "Baltic Signal Monitor — главная"),
]

FUNDING = [
    ("Finansējums — Baltic Signal Monitor", "Финансирование — Baltic Signal Monitor"),
    ("Kas maksā par Baltic Signal Monitor, kas nemaksā un kas nekad nemaksās. Pašlaik: neviens.",
     "Кто платит за Baltic Signal Monitor, кто не платит и кто никогда платить не будет. Сейчас: никто."),
    ("Metode", "Метод"),
    ("Statuss", "Статус"),
    ("BUJ", "Вопросы"),
    ("Kas par to maksā", "Кто за это платит"),
    ("Pašlaik neviens. Šī lapa pastāv tāpēc, ka, ja tas jebkad mainīsies, tu to izlasīsi vispirms šeit — pirms kāds cits tev par to paspēj pastāstīt.",
     "Пока никто. Эта страница существует потому, что, если это когда-нибудь изменится, ты прочитаешь об этом сначала здесь — раньше, чем кто-то другой успеет тебе рассказать."),
    ("Kopējais saņemtais finansējums no visiem avotiem kopš projekta sākuma.",
     "Всего получено финансирования из всех источников с начала проекта."),
    ("Nav grantu. Nav sponsoru. Nav reklāmas. Nav valsts naudas — ne no vienas valsts.",
     "Нет грантов. Нет спонсоров. Нет рекламы. Нет государственных денег — ни от одного государства."),
    ("Uzturēšanas izmaksas sedz personīgi tas cilvēks, kas projektu uztur. Neviens šeit neko nav nopircis, jo nekas nav bijis pārdošanā.",
     "Расходы на поддержание покрывает лично тот человек, который ведёт проект. Никто здесь ничего не купил, потому что ничего не было на продажу."),
    ("Pēdējo reizi pārbaudīts:", "Последняя проверка:"),
    ("Kāpēc šī lapa pastāv, pirms tajā kaut kas ir",
     "Почему эта страница существует раньше, чем в ней что-то появилось"),
    ("Projekts, kas brīdina cilvēkus par draudiem, ir vērts tieši tik, cik vērta ir tā neatkarība. Brīdī, kad parādās nauda, kāds pamatoti jautās, kas samaksāja un ko par to saņēma.",
     "Проект, который предупреждает людей об угрозах, стоит ровно столько, сколько стоит его независимость. В тот момент, когда появляются деньги, кто-то обоснованно спросит, кто заплатил и что за это получил."),
    ("Publiskot šo lapu, kamēr atbilde vēl ir “neviens un neko”, nozīmē, ka ieraksts sākas tīrs. To var lasīt atpakaļejoši un pārbaudīt, nevis uzrakstīt vēlāk, lai izskaidrotu jau notikušo. Caurspīdīguma lapa, kas parādās tā pašā dienā ar pirmo maksājumu, nav caurspīdīgums.",
     "Опубликовать эту страницу, пока ответ всё ещё «никто и ничего», значит, что запись начинается с чистого листа. Её можно читать назад и проверять, а не написать позже, чтобы объяснить уже случившееся. Страница прозрачности, появляющаяся в один день с первым платежом, — это не прозрачность."),
    ("Cik tas patiesībā maksā", "Сколько это на самом деле стоит"),
    ("Domēna vārds un visa pārējā bezmaksas pakalpojumu līmeņi — mājaslapas mitināšana, skenēšanas grafiks, paziņojumu aizmugursistēma. Kopā tie ir desmiti eiro gadā, nevis tūkstoši.",
     "Доменное имя, а всё остальное — бесплатные тарифы сервисов: размещение сайта, расписание сканирований, бэкенд уведомлений. Вместе это десятки евро в год, а не тысячи."),
    ("Dārgākais ieguldījums šajā projektā nekad nav bijusi nauda. Tas ir laiks.",
     "Самым дорогим вложением в этот проект никогда не были деньги. Это время."),
    ("Ko nauda mainītu — un ko ne", "Что деньги изменили бы — а что нет"),
    ("Tā nopirktu avotus, kas šobrīd maksā, ātrāku un plašāku skenēšanu un laiku, lai sistēma turpinātu strādāt kā nākas.",
     "Они купили бы источники, которые сейчас платные, более быстрое и широкое сканирование и время на то, чтобы система продолжала работать как следует."),
    ("Šis nemainās neatkarīgi no tā, kas pienāk:",
     "Это не меняется независимо от того, что придёт:"),
    ("Brīdinājumi paliek bez maksas.", "Предупреждения остаются бесплатными."),
    ("Visi saņem vienu un to pašu brīdinājumu vienā un tajā pašā laikā. Nekad nebūs maksas līmeņa, agrākas piekļuves vai premium versijas.",
     "Все получают одно и то же предупреждение в одно и то же время. Никогда не будет платного уровня, более раннего доступа или премиум-версии."),
    ("Nekādas reklāmas šajā vietnē, brīdinājumos vai kanālā.",
     "Никакой рекламы на этом сайте, в предупреждениях или в канале."),
    ("Neviens finansētājs neredz brīdinājumu pirms sabiedrības.",
     "Ни один финансирующий не видит предупреждение раньше общества."),
    ("Neviens finansētājs nevar pievienot, noņemt vai mainīt to, kas tiek uzraudzīts, vai kā tas tiek novērtēts.",
     "Ни один финансирующий не может добавить, убрать или изменить то, что отслеживается, или то, как это оценивается."),
    ("Naudu, ko šis projekts nepieņems", "Деньги, которые этот проект не примет"),
    ("Daža nauda izmaksā vairāk nekā dod. Šī tiek atteikta uzreiz:",
     "Некоторые деньги стоят дороже, чем дают. Эти отклоняются сразу:"),
    ("Jebkuras valsts valdība, ko šis projekts uzrauga",
     "Правительство любого государства, которое этот проект отслеживает"),
    ("— Igaunijas, Latvijas, Lietuvas, Krievijas, Baltkrievijas — arī caur aģentūru, ministriju vai valsts finansētu starpnieku. Ja maksātu viena no uzraudzītajām pusēm, katrs brīdinājums būtu vērts mazāk — neatkarīgi no tā, kura puse maksātu.",
     "— Эстонии, Латвии, Литвы, России, Беларуси — в том числе через агентство, министерство или финансируемого государством посредника. Если бы платила одна из отслеживаемых сторон, каждое предупреждение стоило бы меньше — независимо от того, какая именно сторона платит."),
    ("Aizsardzības ministrijas, bruņotie spēki un izlūkdienesti jebkurā valstī",
     "Министерства обороны, вооружённые силы и спецслужбы в любой стране"),
    ("vai jebkas, kas tiek novirzīts caur tiem.",
     "или что-либо, направляемое через них."),
    ("Politiskās partijas, kampaņas un kandidāti.",
     "Политические партии, кампании и кандидаты."),
    ("Ieroču ražotāji un aizsardzības uzņēmēji.",
     "Производители оружия и оборонные подрядчики."),
    ("Jebkurus, kas lūdz ietekmi", "Любых, кто просит влияния"),
    ("— pievienot tēmu, noņemt ziņu, mainīt formulējumu vai redzēt brīdinājumu pirms tā publiskošanas.",
     "— добавить тему, убрать сообщение, изменить формулировку или увидеть предупреждение до его публикации."),
    ("Anonīmu naudu virs €500", "Анонимные деньги свыше €500"),
    ("no viena avota. Virs tā tas tiek šeit nosaukts vārdā vai atgriezts.",
     "из одного источника. Выше этого они называются здесь по имени или возвращаются."),
    ("Kas paliek iespējams: grants no neatkarīga fonda vai publiska pētniecības fonda, kam nav interešu šajā reģionā un nav teikšanas par darbu. Ja tāds jebkad tiks pieņemts, tas parādīsies zemāk esošajā tabulā ar visiem tam pievienotajiem nosacījumiem, un neviens no augstāk minētajiem noteikumiem tā dēļ netiks lauzts.",
     "Что остаётся возможным: грант от независимого фонда или публичного исследовательского фонда, у которого нет интересов в этом регионе и нет права голоса в работе. Если такой когда-нибудь будет принят, он появится в таблице ниже со всеми приложенными к нему условиями, и ни одно из перечисленных выше правил из-за него нарушено не будет."),
    ("Šīs vietnes sākumlapā rakstīts, ka tā nav saistīta ne ar vienu valdību. Publiskots, distancēts grants nav saistība — bet šī atšķirība ir kaut ko vērta tikai tad, ja to vari pārbaudīt pats. Tieši tāpēc ir šī tabula.",
     "На главной странице этого сайта написано, что он не связан ни с одним правительством. Публично объявленный, дистанцированный грант — не связь, но эта разница чего-то стоит только тогда, когда ты можешь проверить её сам. Именно для этого и есть эта таблица."),
    ("Kas tiks publiskots, ja finansējums jebkad pienāks",
     "Что будет опубликовано, если финансирование когда-нибудь придёт"),
    ("Septiņu dienu laikā, zemāk esošajā tabulā: kas to deva, cik daudz, kad, kam tas paredzēts, cik ilgi tas darbojas un katrs pievienotais nosacījums. Ja ir līgums — būtiskākie noteikumi vienkāršā valodā.",
     "В течение семи дней, в таблице ниже: кто дал, сколько, когда, на что это предназначено, как долго действует и каждое приложенное условие. Если есть договор — его главные положения простым языком."),
    ("Nauda, kas tiek", "Деньги, от которых"),
    ("atteikta", "отказались"),
    (", arī tiek uzskaitīta, ja par atteikumu ir vērts zināt. Noraidīts piedāvājums par projektu pasaka tikpat daudz, cik pieņemts.",
     ", тоже перечисляются, если об отказе стоит знать. Отклонённое предложение говорит о проекте столько же, сколько принятое."),
    ("Uzskaite", "Учёт"),
    ("Datums", "Дата"),
    ("Avots", "Источник"),
    ("Summa", "Сумма"),
    ("Mērķis", "Назначение"),
    ("Nosacījumi", "Условия"),
    ("Nav ierakstu. Nekas nav saņemts — ne no viena, ne par ko.",
     "Записей нет. Ничего не получено — ни от кого и ни за что."),
    ("Nelieli ziedojumi", "Небольшие донаты"),
    ("Galvenajā lapā ir neobligāta ziedojuma poga (Ko-fi). Ziedojumi tiek ieskaitīti kopējā summā augstāk, nevis uzskaitīti pa vienam — dažu eiro nosūtīšana nedrīkst likt tavu vārdu publiskā lapā.",
     "На главной странице есть необязательная кнопка доната (Ko-fi). Донаты учитываются в общей сумме выше, а не перечисляются по одному — отправка нескольких евро не должна приводить твоё имя на публичную страницу."),
    ("Ziedojums nepērk neko. Ne ietekmi, ne prioritāti, ne citādu brīdinājumu. Tas ir ziedojums. Viss, kas pārsniedz €500 no viena avota, vairs nav ziedojums un pakļaujas augstāk minētajam noteikumam: nosaukts šeit vai atgriezts.",
     "Донат не покупает ничего. Ни влияния, ни приоритета, ни другого предупреждения. Это донат. Всё, что превышает €500 из одного источника, уже не донат и подчиняется указанному выше правилу: названо здесь или возвращено."),
    ("Jautājumi", "Вопросы"),
    ("Šis ir viena cilvēka, nekomerciāls projekts. Ja kaut kas šajā lapā nesaskan, jautā:",
     "Это некоммерческий проект одного человека. Если что-то на этой странице не сходится, спроси:"),
    ("← Atpakaļ uz galveno lapu", "← Назад на главную"),
    ("Baltic Signal Monitor ir neatkarīgs, personīgi veidots uzraudzības rīks — nevis oficiāls valdības, NATO vai izlūkdienestu avots, un nav ar tiem saistīts.",
     "Baltic Signal Monitor — независимый инструмент наблюдения, созданный частным лицом, а не официальный источник правительства, НАТО или спецслужб, и с ними не связан."),
    ("Atradi drošības problēmu?", "Нашёл проблему безопасности?"),
    ("Privātums", "Приватность"),
    ("Finansējums", "Финансирование"),
]


def build(slug, pairs, title_ru):
    src = os.path.join(ROOT, "lv", slug, "index.html")
    dst_dir = os.path.join(ROOT, "ru", slug)
    dst = os.path.join(dst_dir, "index.html")
    t = io.open(src, encoding="utf-8").read()
    missed = []
    for lv, ru in sorted(pairs, key=lambda p: -len(p[0])):
        pat = flexible(lv)
        if not pat.search(t):
            missed.append(lv)
            continue
        t = pat.sub(lambda m, r=ru: r, t)

    t = t.replace('<html lang="lv"', '<html lang="ru"')
    # This page's own address.
    t = t.replace("https://balticsignalmonitor.com/lv/%s/\">" % slug,
                  "https://balticsignalmonitor.com/ru/%s/\">" % slug)
    # ...except in the hreflang set, which must still point at Latvian, and
    # gains a Russian entry of its own.
    t = t.replace(
        '<link rel="alternate" hreflang="lv" href="https://balticsignalmonitor.com/ru/%s/">' % slug,
        '<link rel="alternate" hreflang="lv" href="https://balticsignalmonitor.com/lv/%s/">' % slug)
    lt_alt = '<link rel="alternate" hreflang="lt" href="https://balticsignalmonitor.com/lt/%s/">' % slug
    ru_alt = '<link rel="alternate" hreflang="ru" href="https://balticsignalmonitor.com/ru/%s/">' % slug
    if ru_alt not in t:
        t = t.replace(lt_alt, lt_alt + "\n" + ru_alt)
    # Nav, wordmark and footer links stay inside this language.
    for href in ('href="/lv/"', 'href="/lv/#how"', 'href="/lv/#status"',
                 'href="/lv/#faq"', 'href="/lv/privacy/"', 'href="/lv/funding/"'):
        t = t.replace(href, href.replace("/lv/", "/ru/"))
    # Language switcher: RU active, and RU added to the row.
    t = re.sub(
        r'<span class="lang-switch">.*?</span>',
        '<span class="lang-switch">\n'
        '        <a href="/%s/">EN</a> · <a href="/et/%s/">ET</a> · '
        '<a href="/lv/%s/">LV</a> · <a href="/lt/%s/">LT</a> · '
        '<a href="/ru/%s/" class="active">RU</a>\n      </span>'
        % (slug, slug, slug, slug, slug),
        t, flags=re.S, count=1)

    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    io.open(dst, "w", encoding="utf-8").write(t)
    print("%s: %d/%d pairs, %d bytes" % (dst, len(pairs) - len(missed), len(pairs), len(t)))
    for m in missed:
        print("  MISSED: %r" % m[:90])
    return missed


def main():
    bad = []
    bad += build("privacy", PRIVACY, "Приватность")
    bad += build("funding", FUNDING, "Финансирование")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
