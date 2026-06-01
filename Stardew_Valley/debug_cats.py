import json, os
from collections import Counter

# Check items_gift.json categories
with open(os.path.join('c:\\Users\\中国\\Desktop\\web\\Stardew_Valley', 'items_gift.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

cats = Counter(i.get('category','') for i in data)
print('Categories in items_gift.json:')
for c, n in cats.most_common():
    print(f'  [{c}] -> count={n}')

# Check for items with prices
price_zero = [i for i in data if i.get('price',0) == 0]
print(f'\nItems with price=0: {len(price_zero)}')

# Check if items have source
no_source = [i for i in data if not i.get('source','')]
print(f'Items without source: {len(no_source)}')

# Sample an item from each category
for c in cats:
    items_in = [i for i in data if i.get('category','') == c]
    if items_in:
        ex = items_in[0]
        print(f'\nSample [{c}]: id={ex.get("id","")} name={ex.get("name","")} price={ex.get("price",0)} source={ex.get("source","")}')

# Check if chinese_items.json or items_zh.json exist
for fn in ['chinese_items.json', 'items_zh.json']:
    fp = os.path.join('c:\\Users\\中国\\Desktop\\web\\Stardew_Valley', fn)
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            d2 = json.load(f)
        cats2 = Counter(i.get('category','') for i in d2)
        print(f'\n{fn}: {len(d2)} items')
        for c2, n2 in cats2.most_common():
            print(f'  [{c2}] -> {n2}')