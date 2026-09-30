// Минимальный Service Worker для активации PWA
// Он ничего не кэширует агрессивно, но позволяет браузеру считать сайт "устанавливаемым"

self.addEventListener('install', (event) => {
  console.log('Service Worker installed');
  self.skipWaiting(); // Активируем сразу, не ждем закрытия вкладок
});

self.addEventListener('activate', (event) => {
  console.log('Service Worker activated');
  return self.clients.claim(); // Берем контроль над страницей сразу
});

self.addEventListener('fetch', (event) => {
  // Просто пропускаем запросы как есть
  // Это безопасно и решает проблему блокировки установки
});
