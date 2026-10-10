self.addEventListener('install',event=>event.waitUntil(caches.open('speakwise-v2').then(c=>c.addAll(['/','/static/icon.svg','/static/manifest.webmanifest']))));
self.addEventListener('fetch',event=>{if(event.request.url.includes('/api/'))return;event.respondWith(fetch(event.request).catch(()=>caches.match(event.request)));});
