import requests
from bs4 import BeautifulSoup
import json

def scrape_site():
    url = "https://vitalibystrov.mypixieset.com/"
    
    # Заходим на сайт
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Собираем все ссылки из меню
    links = []
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        href = a['href']
        if text and href.startswith('/') and len(text) > 2:
            full_url = f"https://vitalibystrov.mypixieset.com{href}"
            if not any(link['url'] == full_url for link in links):
                links.append({"title": text, "url": full_url})
    
    # Собираем тексты с главной страницы
    texts = []
    for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
        text = tag.get_text(strip=True)
        if len(text) > 15:
            texts.append({"type": tag.name, "text": text})
    
    # Сохраняем всё в data.json
    data = {
        "site_title": "Vitaly Bystrov",
        "navigation": links[:15],
        "main_content": texts[:20]
    }
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Готово!")

if __name__ == "__main__":
    scrape_site()
