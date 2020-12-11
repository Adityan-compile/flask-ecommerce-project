self.addEventListener("install", (e) => {
  console.log("Service worker changed");
  e.waitUntil(
    caches.open("static").then((cache) => {
      return cache.addAll(["./static", "./"]);
    })
  );
});

self.addEventListener("fetch", (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
