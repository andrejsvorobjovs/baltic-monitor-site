// Browser push alerts — a Telegram-independent channel. No app, no
// account, nothing to trust but your own browser. See api/subscribe.js
// and api/notify.js in the separate baltic-monitor-push project for the
// server side of this.
(function () {
  // Public key only — this identifies the app to the push service, it is
  // not a secret. The matching private key never leaves the backend.
  var VAPID_PUBLIC_KEY = "BPE7HLxOToYIhV0SPgjdwl5LZv3sBsJtb_LdT443sZ9rBkZIQefs7lvR_JWnqcCfci8fw5YizlZYSZQq5QOUONY";
  var SUBSCRIBE_URL = "https://baltic-monitor-push.vercel.app/api/subscribe";

  var btn = document.getElementById("push-btn");
  if (!btn) return;

  // Shared across all four language pages — button text must match
  // whichever page it's running on, not just the initial server-rendered
  // "Loading…" text, or every non-English visitor sees English labels
  // the moment this script takes over.
  var LABELS_BY_LANG = {
    en: {
      unsupported: "Not supported on this browser",
      default: "Enable Browser Alerts",
      subscribing: "Enabling…",
      subscribed: "Alerts Enabled ✓",
      denied: "Notifications blocked in browser settings",
      pushblocked: "Browser blocked push — see below",
      ratelimited: "Too many tries — wait an hour",
      error: "Something went wrong — tap to retry",
    },
    et: {
      unsupported: "Selles brauseris ei toetata",
      default: "Luba brauseri teavitused",
      subscribing: "Lubamine…",
      subscribed: "Teavitused lubatud ✓",
      denied: "Teavitused on brauseri seadetes blokeeritud",
      pushblocked: "Brauser blokeeris teavitused — vaata allpool",
      ratelimited: "Liiga palju katseid — oota tund",
      error: "Midagi läks valesti — proovi uuesti",
    },
    lv: {
      unsupported: "Šajā pārlūkā netiek atbalstīts",
      default: "Iespējot pārlūka paziņojumus",
      subscribing: "Iespējošana…",
      subscribed: "Paziņojumi iespējoti ✓",
      denied: "Paziņojumi bloķēti pārlūka iestatījumos",
      pushblocked: "Pārlūks bloķēja paziņojumus — skati zemāk",
      ratelimited: "Pārāk daudz mēģinājumu — pagaidi stundu",
      error: "Kaut kas nogāja greizi — pieskaries, lai mēģinātu vēlreiz",
    },
    lt: {
      unsupported: "Šioje naršyklėje nepalaikoma",
      default: "Įjungti naršyklės pranešimus",
      subscribing: "Įjungiama…",
      subscribed: "Pranešimai įjungti ✓",
      denied: "Pranešimai užblokuoti naršyklės nustatymuose",
      pushblocked: "Naršyklė užblokavo pranešimus — žr. žemiau",
      ratelimited: "Per daug bandymų — palaukite valandą",
      error: "Kažkas nutiko — bandykite dar kartą",
    },
  };
  var pageLang = (document.documentElement.lang || "en").slice(0, 2).toLowerCase();
  var LABELS = LABELS_BY_LANG[pageLang] || LABELS_BY_LANG.en;

  // Shown under the button when a failure has a specific, actionable
  // cause. Deliberately inline rather than a link: someone who just hit
  // an error is not going to go hunting through an FAQ.
  var HELP_BY_LANG = {
    en: {
      pushblocked:
        "If you use Brave: open brave://settings/privacy, turn on \u201cUse Google services for push messaging\u201d, then restart Brave and try again. " +
        "On iPhone, add this page to your Home Screen first and open it from there \u2014 Apple allows notifications no other way. " +
        "Private/Incognito windows never allow notifications.",
      ratelimited:
        "Too many attempts from your connection in the last hour. Wait an hour and press the button once \u2014 repeated taps keep the block alive.",
      denied:
        "Notifications are blocked for this site. Click the icon to the left of the address bar \u2192 Site settings \u2192 Notifications \u2192 Allow, then reload.",
      error:
        "The alert service did not respond. This is our side, not yours \u2014 please try again in a few minutes.",
    },
    et: {
      pushblocked:
        "Kui kasutad Brave\u2019i: ava brave://settings/privacy, l\u00fclita sisse \u201cUse Google services for push messaging\u201d, taask\u00e4ivita Brave ja proovi uuesti. " +
        "iPhone\u2019is lisa see leht k\u00f5igepealt avaekraanile ja ava sealt \u2014 Apple ei luba teavitusi teisiti. " +
        "Privaatsetes aknates teavitused ei t\u00f6\u00f6ta.",
      ratelimited:
        "Viimase tunni jooksul on sinu \u00fchenduselt tehtud liiga palju katseid. Oota tund ja vajuta nuppu \u00fcks kord \u2014 korduv vajutamine hoiab blokeeringut alles.",
      denied:
        "Teavitused on selle saidi jaoks blokeeritud. Kl\u00f5psa aadressiriba k\u00f5rval oleval ikoonil \u2192 Saidi seaded \u2192 Teavitused \u2192 Luba ja laadi leht uuesti.",
      error:
        "Teenus ei vastanud. See on meie poolel, mitte sinu \u2014 proovi mõne minuti p\u00e4rast uuesti.",
    },
    lv: {
      pushblocked:
        "Ja lieto Brave: atver brave://settings/privacy, iesl\u0113dz \u201cUse Google services for push messaging\u201d, p\u0101rstart\u0113 Brave un m\u0113\u0123ini v\u0113lreiz. " +
        "iPhone: vispirms pievieno \u0161o lapu s\u0101kuma ekr\u0101nam un atver no turienes \u2014 Apple cit\u0101di pazi\u0146ojumus nepie\u013cauj. " +
        "Priv\u0101tajos logos pazi\u0146ojumi nedarbojas.",
      ratelimited:
        "P\u0113d\u0113j\u0101 stund\u0101 no tavas savienojuma bijis p\u0101r\u0101k daudz m\u0113\u0123in\u0101jumu. Pagaidi stundu un nospied pogu vienu reizi \u2014 atk\u0101rtota spie\u0161ana blo\u0137\u0113\u0161anu tikai uztur.",
      denied:
        "Pazi\u0146ojumi \u0161ai vietnei ir blo\u0137\u0113ti. Noklik\u0161\u0137ini uz ikonas pa kreisi no adreses joslas \u2192 Vietnes iestat\u012bjumi \u2192 Pazi\u0146ojumi \u2192 At\u013caut un p\u0101rl\u0101d\u0113.",
      error:
        "Serviss neatbild\u0113ja. Tas ir m\u016bsu, ne tav\u0101 pus\u0113 \u2014 m\u0113\u0123ini v\u0113lreiz p\u0113c da\u017e\u0101m min\u016bt\u0113m.",
    },
    lt: {
      pushblocked:
        "Jei naudojate Brave: atidarykite brave://settings/privacy, \u012fjunkite \u201cUse Google services for push messaging\u201d, paleiskite Brave i\u0161 naujo ir bandykite dar kart\u0105. " +
        "iPhone: pirma prid\u0117kite \u0161\u012f puslap\u012f \u012f pradin\u012f ekran\u0105 ir atidarykite i\u0161 ten \u2014 Apple kitaip pryne\u0161im\u0173 neleid\u017eia. " +
        "Privačiuose languose prane\u0161imai neveikia.",
      ratelimited:
        "Per pastar\u0105j\u0105 valand\u0105 i\u0161 j\u016bs\u0173 ry\u0161io buvo per daug bandym\u0173. Palaukite valand\u0105 ir paspauskite mygtuk\u0105 vien\u0105 kart\u0105 \u2014 pakartotiniai paspaudimai blokavim\u0105 tik pratęsia.",
      denied:
        "Prane\u0161imai \u0161iai svetainei u\u017eblokuoti. Spustel\u0117kite piktogram\u0105 kair\u0117je nuo adreso juostos \u2192 Svetain\u0117s nustatymai \u2192 Prane\u0161imai \u2192 Leisti ir perkraukite.",
      error:
        "Paslauga neatsak\u0117. Tai m\u016bs\u0173, o ne j\u016bs\u0173 pus\u0117je \u2014 pabandykite po keli\u0173 minu\u010di\u0173.",
    },
  };
  var HELP = HELP_BY_LANG[pageLang] || HELP_BY_LANG.en;

  function showHelp(state) {
    var el = document.getElementById("push-help");
    if (!el) return;
    var text = HELP[state];
    if (!text) {
      el.hidden = true;
      return;
    }
    el.textContent = text;
    el.hidden = false;
  }

  function setState(state) {
    btn.dataset.state = state;
    btn.textContent = LABELS[state] || LABELS.default;
    btn.disabled = state === "subscribing" || state === "subscribed" || state === "unsupported";
  }

  function urlBase64ToUint8Array(base64String) {
    var padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    var base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/");
    var rawData = window.atob(base64);
    var outputArray = new Uint8Array(rawData.length);
    for (var i = 0; i < rawData.length; i++) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
    setState("unsupported");
    return;
  }

  navigator.serviceWorker
    .register("/sw.js")
    .then(function (reg) {
      return reg.pushManager.getSubscription();
    })
    .then(function (sub) {
      if (sub) {
        setState("subscribed");
      } else if (window.Notification && Notification.permission === "denied") {
        setState("denied");
        showHelp("denied");
      } else {
        setState("default");
      }
    })
    .catch(function () {
      setState("default");
    });

  btn.addEventListener("click", function () {
    var retryable = ["default", "error", "pushblocked", "ratelimited"];
    if (retryable.indexOf(btn.dataset.state) === -1) return;
    setState("subscribing");

    // Three genuinely different failures used to collapse into one
    // "something went wrong": the browser refusing to create a push
    // subscription at all (Brave ships with Google push messaging OFF,
    // which is by far the commonest cause and is invisible from the
    // permission prompt), our own per-IP rate limit of 5/hour, and a real
    // backend problem. Telling someone to "tap to retry" when they are
    // rate-limited from tapping is a trap — five taps locks them out for
    // an hour and keeps showing the same message.
    navigator.serviceWorker.ready
      .then(function (reg) {
        return reg.pushManager
          .subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
          })
          .catch(function (err) {
            err.stage = "subscribe";
            throw err;
          });
      })
      .then(function (subscription) {
        return fetch(SUBSCRIBE_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(subscription),
        });
      })
      .then(function (resp) {
        if (resp.status === 429) {
          var err = new Error("rate limited");
          err.stage = "ratelimited";
          throw err;
        }
        if (!resp.ok) throw new Error("subscribe request failed");
        setState("subscribed");
      })
      .catch(function (err) {
        if (window.Notification && Notification.permission === "denied") {
          setState("denied");
        } else if (err && err.stage === "ratelimited") {
          setState("ratelimited");
        } else if (err && err.stage === "subscribe") {
          setState("pushblocked");
        } else {
          setState("error");
        }
        showHelp(btn.dataset.state);
      });
  });
})();
