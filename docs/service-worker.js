// MOFNet Service Worker - Simple Version
const CACHE_NAME = 'mofnet-v1.0';
const APP_VERSION = '1.0.2';

// Install
self.addEventListener('install', event => {
  console.log('[SW] Installing MOFNet v' + APP_VERSION);
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll([
        '/',
        '/index.html',
        '/manifest.json'
      ]))
  );
});

// Activate
self.addEventListener('activate', event => {
  console.log('[SW] MOFNet activated');
});

// Fetch
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});

// Listen for messages (for updates)
self.addEventListener('message', event => {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
});
