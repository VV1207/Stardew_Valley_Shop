#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, sys, os

os.chdir(os.path.dirname(__file__) or '.')

# Load data
with open('items_gift.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get categories
cats = sorted(set(i['category'] for i in data if 'category' in i))
print("Categories found:", cats)

# Sample items from each category
for cat in cats:
    items_in_cat = [i for i in data if i['category'] == cat]
    print(f"\n{cat} ({len(items_in_cat)} items):")
    for item in items_in_cat[:3]:
        print(f"  - {item['name']}: price={item.get('price', '?')}")
    if len(items_in_cat) > 3:
        print(f"  ... and {len(items_in_cat)-3} more")

# Check for items where price is 0
zero_price = [i for i in data if i.get('price', 0) == 0]
print(f"\n\nItems with price=0: {len(zero_price)}")
for z in zero_price[:5]:
    print(f"  {z['name']} (cat: {z['category']})")

# Write results to file
output = []
output.append("Categories: " + str(cats))
for cat in cats:
    items_in_cat = [i for i in data if i['category'] == cat]
    output.append(f"\n{cat} ({len(items_in_cat)} items):")
    for item in items_in_cat:
        output.append(f"  {item['name']}: price={item.get('price', 0)}")

with open('analysis_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("\n\nAnalysis written to analysis_result.txt")