# -*- coding: utf-8 -*-
import json, os, random
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))

# 1. Load data
with open(os.path.join(BASE, 'items_complete.json'), 'r', encoding='utf-8') as f:
    items = json.load(f)

# 2. Check images
images_dir = os.path.join(BASE, 'images')
existing_files = set(os.listdir(images_dir))
missing_images = []
for i, item in enumerate(items):
    path = item.get('image','')
    if path:
        fname = path.split('/')[-1]
        # Normalize for comparison
        fname_clean = fname.replace('%20', '_').replace(' ', '_')
        if fname not in existing_files and fname_clean not in existing_files and '24px-' + fname not in existing_files and '24px-' + fname_clean not in existing_files:
            # Check case-insensitive
            found = False
            for ef in existing_files:
                if ef.lower() == fname.lower() or ef.lower() == fname_clean.lower():
                    found = True
                    # Fix the path
                    items[i]['image'] = 'images/' + ef
                    break
            if not found:
                # Check with underscore space replacement
                alt_name = fname.replace(' ', '_')
                if alt_name in existing_files:
                    items[i]['image'] = 'images/' + alt_name
                else:
                    missing_images.append((i, item.get('name','?'), item.get('name_en','?'), fname))

print(f"=== IMAGE ANALYSIS ===")
print(f"Total items with image: {sum(1 for i in items if i.get('image'))}")
print(f"Missing images: {len(missing_images)}")
for idx, name, ename, fpath in missing_images[:30]:
    print(f"  [{idx}] {name} ({ename}): {fpath}")

# 3. Check gifting data
gifting_missing = sum(1 for i in items if not i.get('gifting'))
gifting_present = sum(1 for i in items if i.get('gifting'))
print(f"\n=== GIFTING DATA ===")
print(f"Items with gifting: {gifting_present}")
print(f"Items without gifting: {gifting_missing}")

# 4. Check food properties (energy/health)
food_items = [i for i in items if i.get('category') == '菜品']
food_with_energy = sum(1 for i in food_items if i.get('energy') or i.get('health'))
print(f"\n=== FOOD PROPERTIES ===")
print(f"Food items: {len(food_items)}")
print(f"Food with energy/health: {food_with_energy}")

# 5. Check prices - items with zero price
from collections import defaultdict
cats_with_missing_prices = defaultdict(list)
for item in items:
    price = item.get('price')
    if price is None or price == 0:
        cats_with_missing_prices[item['category']].append(item['name'])

print(f"\n=== ZERO PRICE ITEMS BY CATEGORY ===")
for cat, names in sorted(cats_with_missing_prices.items()):
    print(f"  {cat}: {len(names)} items - {', '.join(names[:10])}")

# 6. Check what categories have gifting data
cats_gifting = defaultdict(lambda: {'with': 0, 'without': 0})
for item in items:
    cats_gifting[item['category']]['with' if item.get('gifting') else 'without'] += 1

print(f"\n=== GIFTING BY CATEGORY ===")
for cat, counts in sorted(cats_gifting.items()):
    print(f"  {cat}: with={counts['with']}, without={counts['without']}")

print("\nDone analysis")