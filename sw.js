const CACHE='vitaly-bystrov-v8';
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.add('./'))));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k))))));
self.addEventListener('fetch',e=>e.respondWith(fetch(e.request).catch(()=>caches.match(e.request))));
