const CACHE_NAME = 'codecraft-v3';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

async function fetchNavigation(request) {
  try {
    const response = await fetch(request);

    // The shell changes between deployments, so refresh its offline copy when
    // the network is available. A cache write failure must not hide a valid
    // network response from the user.
    if (response.ok) {
      try {
        const cache = await caches.open(CACHE_NAME);
        await cache.put('./index.html', response.clone());
      } catch {
        // Continue with the network response if storage is unavailable.
      }
    }

    return response;
  } catch {
    const cached = await caches.match(request);
    return cached || caches.match('./index.html') || Response.error();
  }
}

async function handleFetch(request) {
  if (request.mode === 'navigate') {
    return fetchNavigation(request);
  }

  const cached = await caches.match(request);
  return cached || fetch(request);
}

self.addEventListener('fetch', e => {
  e.respondWith(handleFetch(e.request));
});
