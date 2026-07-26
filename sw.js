// Service worker for Baltic Signal Monitor browser alerts.
// Only handles push display + click routing — no caching/offline logic,
// this site has no need for it.

self.addEventListener("push", function (event) {
  var data = {};
  try {
    data = event.data ? event.data.json() : {};
  } catch (e) {
    data = {};
  }
  var title = data.title || "Baltic Signal Monitor";
  var body = data.body || "";
  var url = data.url || "https://balticsignalmonitor.com/#status";

  event.waitUntil(
    self.registration.showNotification(title, {
      body: body,
      icon: "icon-192.png",
      data: { url: url },
    })
  );
});

self.addEventListener("notificationclick", function (event) {
  event.notification.close();
  var url =
    (event.notification.data && event.notification.data.url) ||
    "https://balticsignalmonitor.com/#status";

  event.waitUntil(
    clients.matchAll({ type: "window" }).then(function (clientList) {
      for (var i = 0; i < clientList.length; i++) {
        var client = clientList[i];
        if (client.url === url && "focus" in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(url);
      }
    })
  );
});
