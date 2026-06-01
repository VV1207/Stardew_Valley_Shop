import requests, sys, json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

pages = ['Beer', 'Strawberry', 'Diamond', 'Pumpkin_Pie', 'Dinosaur_Mayonnaise', 'Fried_Egg']

for page in pages:
    print(f'\n{"="*60}')
    print(f'PAGE: {page}')
    print('='*60)
    r = requests.get(f'https://stardewvalleywiki.com/{page}', headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Find all h2 sections
    sections = []
    for h2 in soup.find_all('h2'):
        sp = h2.find('span', class_='mw-headline')
        if sp:
            sections.append(sp.get_text(strip=True))
    
    print('Sections:', sections)
    
    # Get infobox details
    infobox = soup.find('table', id='infoboxtable')
    if infobox:
        rows = infobox.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                if label in ['Source', 'Buff(s)', 'Energy / Health', 'Sell Price', 'Recipe', 'Ingredients', 'Healing']:
                    print(f'  {label}: {value[:100]}')
    
    # Get Gifting section
    for h2 in soup.find_all('h2'):
        sp = h2.find('span', class_='mw-headline')
        if sp and 'gift' in sp.get_text(strip=True).lower():
            table = h2.find_next('table')
            if table:
                for row in table.find_all('tr'):
                    cells = row.find_all(['td','th'])
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    if len(row_data) >= 2:
                        print(f'  GIFT: {row_data[0]} -> {row_data[1][:200]}')
            break