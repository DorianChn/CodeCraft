import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const serviceWorkerPath = fileURLToPath(new URL('../sw.js', import.meta.url));
const source = readFileSync(serviceWorkerPath, 'utf8');
const listeners = new Map();
const entries = new Map();
let networkResponse;
let networkError;
let fetchCalls = 0;

const cacheKey = request => (typeof request === 'string' ? request : request.url);
const cache = {
  async put(request, response) {
    entries.set(cacheKey(request), response);
  },
  async match(request) {
    return entries.get(cacheKey(request)) ?? null;
  },
};

const caches = {
  async open() {
    return cache;
  },
  async match(request) {
    return cache.match(request);
  },
  async keys() {
    return ['codecraft-v2', 'codecraft-v3'];
  },
  async delete() {
    return true;
  },
};

const context = {
  caches,
  console,
  fetch: async () => {
    fetchCalls += 1;
    if (networkError) throw networkError;
    return networkResponse;
  },
  Promise,
  Response: { error: () => ({ status: 0, type: 'error' }) },
  self: {
    addEventListener(type, handler) {
      listeners.set(type, handler);
    },
    clients: { claim: async () => {} },
    skipWaiting: async () => {},
  },
};

vm.runInNewContext(source, context, { filename: serviceWorkerPath });

async function dispatchFetch(request) {
  let responsePromise;
  listeners.get('fetch')({
    request,
    respondWith(promise) {
      responsePromise = Promise.resolve(promise);
    },
  });
  return responsePromise;
}

const navigationRequest = {
  mode: 'navigate',
  url: 'https://codecraft.example/',
};

const staleShell = { name: 'stale shell' };
const freshShell = {
  name: 'fresh shell',
  ok: true,
  clone() {
    return this;
  },
};

entries.set('./index.html', staleShell);
networkResponse = freshShell;
networkError = null;
fetchCalls = 0;

assert.equal(await dispatchFetch(navigationRequest), freshShell);
assert.equal(entries.get('./index.html'), freshShell);
assert.equal(fetchCalls, 1);

networkError = new Error('offline');
fetchCalls = 0;
assert.equal(await dispatchFetch(navigationRequest), freshShell);
assert.equal(fetchCalls, 1);

const cachedAsset = { name: 'cached asset' };
entries.set('https://codecraft.example/app.js', cachedAsset);
assert.equal(
  await dispatchFetch({ mode: 'same-origin', url: 'https://codecraft.example/app.js' }),
  cachedAsset,
);
assert.equal(fetchCalls, 1, 'cached static assets should avoid a network request');

console.log('Service Worker cache strategy tests passed');
