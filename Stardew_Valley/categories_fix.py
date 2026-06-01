#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

# Load the data
with open('items_gift.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check actual category strings
cats = sorted(set(i.get('category', '') for i in data))
print("Categories with hex:")
for c in cats:
    print(f"  {c!r} -> bytes: {c.encode('utf-8').hex()}")

# Test mapping with actual Chinese strings from the file
category_map_test = {
    "动物制品": "动物",
    "古物": "古物",
    "垃圾": "垃圾",
    "工匠制品": "工匠制品",
    "怪物战利品": "怪物战利品",
    "水果": "果树",
    "渔具": "渔具",
    "烹饪": "菜品",
    "种子": "作物",
    "肥料": "农场工具",
    "蔬菜": "作物",
    "资源": "资源",
}

# Try the mapping
for item in data[:5]:
    orig = item.get('category', '')
    mapped = category_map_test.get(orig, orig)
    print(f"  {item['name']}: orig={orig!r} -> mapped={mapped!r}")