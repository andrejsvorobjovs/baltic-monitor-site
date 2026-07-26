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

  var LABELS = {
    unsupported: "Not supported on this browser",
    default: "Enable Browser Alerts",
    subscribing: "Enabling…",
    subscribed: "Alerts Enabled ✓",
    denied: "Notifications blocked in browser settings",
    error: "Something went wrong — tap to retry",
  };

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
    .register("sw.js")
    .then(function (reg) {
      return reg.pushManager.getSubscription();
    })
    .then(function (sub) {
      if (sub) {
        setState("subscribed");
      } else if (window.Notification && Notification.permission === "denied") {
        setState("denied");
      } else {
        setState("default");
      }
    })
    .catch(function () {
      setState("default");
    });

  btn.addEventListener("click", function () {
    if (btn.dataset.state !== "default" && btn.dataset.state !== "error") return;
    setState("subscribing");

    navigator.serviceWorker.ready
      .then(function (reg) {
        return reg.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
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
        if (!resp.ok) throw new Error("subscribe request failed");
        setState("subscribed");
      })
      .catch(function () {
        if (window.Notification && Notification.permission === "denied") {
          setState("denied");
        } else {
          setState("error");
        }
      });
  });
})();
