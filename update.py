import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

SITE_URL = "https://vitalibystrov.mypixieset.com/"
DATA_FILE = "data.json"

def main():
    print("Проверяем сайт...")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(SITE_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Ошибка: сайт вернул код {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    links_found = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        text = a_tag.get_text(strip=True)
        
        if href.startswith('/') and len(text) > 3:
            full_url = f"https://vitalibystrov.mypixieset.com{href}"
            links_found.append({"title": text, "url": full_url})

    unique_links = []
    seen_urls = set()
    for item in links_found:
        if item['url'] not in seen_urls:
            seen_urls.add(item['url'])
            unique_links.append(item)

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"items": []}

    old_urls = {item['url'] for item in data['items']}
    new_items = [item for item in unique_links if item['url'] not in old_urls]

    if new_items:
        print(f"Найдено {len(new_items)} новых элементов!")
        data['items'].extend(new_items)
        data['last_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        with open("has_changes.txt", "w") as f:
            f.write("yes")
    else:
        print("Новых элементов нет.")

if __name__ == "__main__":
    main()
