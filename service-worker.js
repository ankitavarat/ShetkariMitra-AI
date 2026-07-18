const CACHE_NAME = 'shetkarimitra-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];


self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    }).then(() => self.skipWaiting()) // लगेच ॲक्टिव्हेट करण्यासाठी
  );
});

// सर्विस वर्कर ॲक्टिव्हेट करणे
self.addEventListener('activate', (e) => {
  e.waitUntil(self.clients.claim());
});

// नेटवर्कवरून डेटा मिळवणे
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
