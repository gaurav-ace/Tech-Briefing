const CACHE='tech-briefing-v6';
const CORE=['./','./index.html','./manifest.json','./icon.svg','./data/headlines.json'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE))));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('tech-briefing-')&&k!==CACHE).map(k=>caches.delete(k))))));
self.addEventListener('fetch',e=>{if(new URL(e.request.url).origin===location.origin){e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{if(e.request.url.includes('/data/headlines.json'))return res; caches.open(CACHE).then(c=>c.put(e.request,res.clone()));return res}).catch(()=>caches.match('./index.html'))));}});
