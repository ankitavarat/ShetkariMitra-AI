const CACHE_NAME = 'shetkarimitra-v20';

// कॅशे करायच्या अचूक फाईल्स
const ASSETS_TO_CACHE = [
  '/',
  '/manifest.json',
  '/icon-192.png',
  '/icon-512.png'
];

// १. इन्स्टॉल करताना होमपेज सेव्ह करा
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// २. जुना कॅशे साफ करा
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// ३. ऑफलाईन असताना कॅशेमधून होमपेज दाखवा
self.addEventListener('fetch', (event) => {
  // फक्त पेज नेव्हिगेशन किंवा GET रिक्वेस्ट हाताळा
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => {
        return caches.match('/');
      })
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
