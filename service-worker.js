const CACHE_NAME = 'shetkarimitra-v5'; // Version 5

// ऑफलाईन सेव्ह करायच्या सर्व फाईल्स आणि लिंक्स
const ASSETS = [
  '/',
  './smart_farmer_ui.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  'https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap'
];

// 1. Install & Cache All Assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[PWA] Caching all essential files');
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

// 2. Activate & Clear Old Cache
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[PWA] Removing old cache:', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// 3. Fetch (Network First, Fallback to Cache)
self.addEventListener('fetch', (event) => {
  // Backend API calls bypass cache
  if (event.request.url.includes('/chat') || 
      event.request.url.includes('/weather') || 
      event.request.url.includes('/detect')) {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // dynamic cache update
        if (response && response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // इंटरनेट नसेल तर कॅशेमधून होमपेज द्या
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          if (event.request.mode === 'navigate') {
            return caches.match('/');
          }
        });
      })
  );
});
