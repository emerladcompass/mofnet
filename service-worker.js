// MOFNet Service Worker v1.0
const CACHE_NAME = 'mofnet-v1.0';
const APP_VERSION = '1.0.2';

// Install Service Worker
self.addEventListener('install', event => {
  console.log('[SW] Installing MOFNet PWA v' + APP_VERSION);
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll([
        '/',
        '/index.html',
        '/manifest.json'
      ]))
  );
});

// Activate Service Worker
self.addEventListener('activate', event => {
  console.log('[SW] MOFNet activated');
});

// Handle network requests
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});

// Background sync (for future features)
self.addEventListener('sync', event => {
  if (event.tag === 'sync-data') {
    console.log('[SW] Background sync triggered');
  }
});
