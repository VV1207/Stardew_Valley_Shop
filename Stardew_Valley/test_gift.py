import requests, sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://stardewvalleywiki.com/Beer', headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
soup = BeautifulSoup(r.text, 'lxml')
for h2 in soup.find_all('h2'):
    sp = h2.find('span', class_='mw-headline')
    if sp and 'gift' in sp.get_text(strip=True).lower():
        print('GIFT SECTION FOUND')
        table = h2.find_next('table')
        if table:
            print('TABLE FOUND')
            # print the HTML structure
            for row in table.find_all('tr'):
                cells = row.find_all(['td','th'])
                row_data = [cell.get_text(strip=True) for cell in cells]
                print('  |  '.join(row_data))
        break