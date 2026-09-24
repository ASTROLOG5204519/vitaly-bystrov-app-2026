import feedparser
import json
import os
from datetime import datetime

RSS_URL = "https://vitalibystrov.mypixieset.com/journal/rss"
DATA_FILE = "data.json"

def main():
    print("Читаем RSS ленту...")
    
    # Скачиваем и парсим RSS
    feed = feedparser.parse(RSS_URL)
    
    if feed.bozo:
        print(f"Ошибка чтения RSS: {feed.bozo_exception}")
        return

    new_items = []
    for entry in feed.entries:
        new_items.append({
            "title": entry.get("title", "Без названия"),
            "link": entry.get("link", ""),
            "published": entry.get("published", "")
        })

    print(f"Найдено {len(new_items)} записей в RSS.")

    # Читаем старые данные
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except:
                data = {"items": []}
    else:
        data = {"items": []}

    # Обновляем данные (перезаписываем список, чтобы всегда было актуально)
    data['items'] = new_items
    data['last_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Сохраняем
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print("✅ data.json успешно обновлен!")

if __name__ == "__main__":
    main()
