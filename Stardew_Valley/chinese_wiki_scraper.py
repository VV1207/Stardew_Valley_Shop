#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
星露谷中文维基百科数据抓取器
- 从 zh.stardewvalleywiki.com 获取标准中文翻译
- 获取所有物品的正确售价
- 按指定分类重新组织数据
- 包括星级品质定价
"""
import sys
import io
# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
import json
import os
import time
import re
from bs4 import BeautifulSoup

# 中文维基配置
ZH_BASE_URL = "https://zh.stardewvalleywiki.com"
ZH_API_URL = f"{ZH_BASE_URL}/mediawiki/api.php"
HEADERS = {
    "User-Agent": "StardewValleyDataCollector/1.0 (for personal project)"
}
DATA_FILE = os.path.join(os.path.dirname(__file__), "chinese_items.json")

# 中文维基页面名称映射
CATEGORY_PAGE_NAMES = {
    "作物": "农作物",
    "动物": "动物",
    "果树": "果树",
    "工匠制品": "工匠物品",
    "家具": "家具",
    "墙纸": "墙纸",
    "地板": "地板",
    "矿物": "矿物",
    "渔具": "渔具",
    "武器": "武器",
    "帽子": "帽子",
    "鞋类": "鞋类",
    "戒指": "戒指",
    "菜品": "烹饪",
    "农场工具": "工具",
    "古物": "古物",
    "怪物战利品": "怪物战利品",
    "书": "书",
    "季节采集物": "采集"
}

# 品质倍率
QUALITY_MULTIPLIER = {
    "普通": 1.0,
    "银星": 1.25,
    "金星": 1.5,
    "铱星": 2.0
}

def api_get_page_html(title):
    """通过 MediaWiki API 获取页面解析后的 HTML"""
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "format": "json",
        "redirects": "true",
        "utf8": "1",
    }
    try:
        r = requests.get(ZH_API_URL, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            print(f"  [ERROR] API Error for {title}: {data['error']}")
            return None
        return data["parse"]["text"]["*"]
    except Exception as e:
        print(f"  [ERROR] API Request failed for {title}: {e}")
        return None


def extract_sell_price(html):
    """从页面 HTML 中提取售价"""
    price = 0
    if not html:
        return price
    soup = BeautifulSoup(html, "lxml")
    infobox = soup.find("table", id="infoboxtable")
    if not infobox:
        return price
    
    rows = infobox.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 2:
            label_cell = cells[0]
            value_cell = cells[1]
            label = label_cell.get_text(strip=True)
            
            if label == "售价":
                value_text = value_cell.get_text(strip=True)
                # Remove HTML comments and sort values
                value_text = re.sub(r'<!--.*?-->', '', value_text)
                value_text = re.sub(r'data-sort-value="[^"]*"\s*', '', value_text)
                # Extract first number
                price_match = re.search(r'(\d[\d,]*)', value_text)
                if price_match:
                    price = int(price_match.group(1).replace(",", ""))
                break
    
    return price


def extract_items_from_category_table(html, category_zh, seen_names):
    """从分类页面的表格中提取物品"""
    items = []
    if not html:
        return items
    
    soup = BeautifulSoup(html, "lxml")
    
    # Find the main content
    tables = soup.find_all("table", class_="wikitable")
    
    for table in tables:
        rows = table.find_all("tr")
        for row in rows[1:]:  # Skip header
            cells = row.find_all("td")
            if len(cells) < 2:
                continue
            
            # Find item link in first few cells
            link = None
            img_tag = None
            for cell in cells[:3]:
                l = cell.find("a")
                if l and l.get("href", "").startswith("/"):
                    link = l
                    img_tag = cell.find("img")
                    break
            
            if not link:
                continue
            
            name = link.get_text(strip=True)
            if not name or name in seen_names:
                continue
            
            seen_names.add(name)
            
            # Get image URL
            image_url = None
            if img_tag:
                src = img_tag.get("src") or ""
                if src.startswith("//"):
                    image_url = "https:" + src
                elif src.startswith("/"):
                    image_url = ZH_BASE_URL + src
                else:
                    image_url = src
            
            # Get page URL
            page_url = link.get("href", "")
            if page_url.startswith("/"):
                page_url = ZH_BASE_URL + page_url
            
            # Determine if item has quality
            has_quality = category_zh in ["作物", "季节采集物"]
            
            items.append({
                "name": name,
                "category": category_zh,
                "image_url": image_url or "",
                "page_url": page_url,
                "has_quality": has_quality,
            })
    
    return items


def scrape_all_chinese_data():
    """主爬虫：从中文维基抓取所有物品数据"""
    print("=" * 60)
    print("Stardew Valley Chinese Wiki Data Scraper")
    print("=" * 60)
    
    print("\n[Step 1] Fetching item lists from Chinese wiki categories...")
    
    all_items = []
    seen_names = set()
    
    # Fetch from each category
    for cat_zh, page_name in CATEGORY_PAGE_NAMES.items():
        print(f"\n  [{cat_zh}] Fetching page: {page_name}")
        
        html = api_get_page_html(page_name)
        if not html:
            print(f"    [FAIL] Could not get {page_name}")
            continue
        
        items = extract_items_from_category_table(html, cat_zh, seen_names)
        all_items.extend(items)
        
        print(f"    [OK] Found {len(items)} items")
        time.sleep(0.5)
    
    print(f"\n[Step 2] Total candidates: {len(all_items)}")
    
    # Step 2: Get details for each item
    print(f"\n[Step 3] Getting detailed data...")
    full_data = []
    
    for idx, item in enumerate(all_items, 1):
        name = item["name"]
        print(f"  [{idx}/{len(all_items)}] {name}...", end=" ")
        
        # Get page HTML
        # Extract page title from URL
        page_title = item["page_url"].replace(ZH_BASE_URL + "/", "")
        page_title = requests.utils.unquote(page_title)
        
        page_html = api_get_page_html(page_title)
        
        sell_price = 0
        if page_html:
            sell_price = extract_sell_price(page_html)
            print(f"price={sell_price}")
        else:
            print(f"price=0 (no detail)")
        
        # Download image
        image_filename = ""
        if item["image_url"]:
            image_filename = item["image_url"].split("/")[-1].split("?")[0]
            image_filename = requests.utils.unquote(image_filename)
            download_image(item["image_url"], image_filename)
        
        item_data = {
            "id": idx,
            "name": name,
            "category": item["category"],
            "sell_price": sell_price,
            "image": f"images/{image_filename}" if image_filename else "",
            "wiki_url": item["page_url"],
            "has_quality": item["has_quality"],
            "qualities": get_quality_prices(sell_price, item["has_quality"]),
        }
        
        full_data.append(item_data)
        time.sleep(0.3)
    
    # Save data
    print(f"\n[Step 4] Saving data...")
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    print(f"  [OK] Saved to: {DATA_FILE} ({len(full_data)} items)")
    
    # Statistics
    print(f"\n{'='*60}")
    print("Statistics:")
    for cat in CATEGORY_PAGE_NAMES.keys():
        count = sum(1 for i in full_data if i["category"] == cat)
        if count > 0:
            print(f"  - {cat}: {count}")
    print(f"{'='*60}")
    
    return full_data


def get_quality_prices(base_price, has_quality):
    """获取品质价格"""
    if not has_quality:
        return {}
    
    return {
        "普通": base_price,
        "银星": int(base_price * 1.25),
        "金星": int(base_price * 1.5),
        "铱星": int(base_price * 2.0)
    }


def download_image(image_url, filename):
    """下载图片到本地"""
    if not image_url or not filename:
        return False
    image_dir = os.path.join(os.path.dirname(__file__), "images")
    os.makedirs(image_dir, exist_ok=True)
    filepath = os.path.join(image_dir, filename)
    if os.path.exists(filepath):
        return True
    try:
        r = requests.get(image_url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        print(f"    [OK] Downloaded image: {filename}")
        return True
    except Exception as e:
        print(f"    [FAIL] Download {filename}: {e}")
        return False


if __name__ == "__main__":
    data = scrape_all_chinese_data()