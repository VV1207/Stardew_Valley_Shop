#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
星露谷维基百科商品数据抓取器 (增强版)
- 抓取所有可交易物品的完整数据
- 包括村民喜好（赠送反应）、价格、来源、属性等
- 下载所有物品图片
"""

import requests
import json
import os
import time
import re
from bs4 import BeautifulSoup

# 配置
BASE_URL = "https://stardewvalleywiki.com"
API_URL = f"{BASE_URL}/mediawiki/api.php"
HEADERS = {
    "User-Agent": "StardewValleyDataCollector/1.0 (for personal project)"
}
DATA_FILE = os.path.join(os.path.dirname(__file__), "items_data.json")
SIMPLE_FILE = os.path.join(os.path.dirname(__file__), "items_simple.json")
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "images")

# 确保图片目录存在
os.makedirs(IMAGE_DIR, exist_ok=True)

# 所有村民名单（用于赠送数据校验）
ALL_VILLAGERS = [
    "Abigail", "Alex", "Caroline", "Clint", "Demetrius", "Dwarf", "Elliott",
    "Emily", "Evelyn", "George", "Gus", "Haley", "Harvey", "Jas", "Jodi",
    "Kent", "Krobus", "Leah", "Leo", "Lewis", "Linus", "Marnie", "Maru",
    "Pam", "Penny", "Pierre", "Robin", "Sam", "Sandy", "Sebastian", "Shane",
    "Vincent", "Willy", "Wizard"
]

# 分类映射（英文 -> 中文）
CATEGORY_MAP = {
    "Basic": "基础",
    "Cooking": "烹饪",
    "Fish": "鱼类",
    "Forage": "采集",
    "Mineral": "矿物",
    "Vegetable": "蔬菜",
    "Fruit": "水果",
    "Artisan Goods": "工匠制品",
    "Animal Produce": "动物制品",
    "Monster Loot": "怪物战利品",
    "Seeds": "种子",
    "Fertilizer": "肥料",
    "Fishing": "渔具",
    "Tackle": "渔具",
    "Artifact": "古物",
    "Resources": "资源",
    "Crafting": "材料",
    "Decor": "装饰",
    "Equipment": "装备",
    "Ring": "戒指",
    "Tool": "工具",
    "Weapon": "武器",
    "Boots": "靴子",
    "Hat": "帽子",
    "Trash": "垃圾",
    "Bait": "鱼饵",
    "Other": "其他",
    "Furniture": "家具",
}


def api_get_page_html(title):
    """通过 MediaWiki API 获取页面解析后的 HTML"""
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "format": "json",
        "redirects": "true",
    }
    try:
        r = requests.get(API_URL, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            print(f"  API Error for {title}: {data['error']}")
            return None
        # 尝试获取重定向
        if "redirects" in data:
            for redir in data["redirects"]:
                title = redir["to"]
        return data["parse"]["text"]["*"]
    except Exception as e:
        print(f"  API Request failed for {title}: {e}")
        return None


def extract_infobox(html):
    """从页面 HTML 中提取信息框数据"""
    info = {}
    if not html:
        return info
    soup = BeautifulSoup(html, "lxml")
    infobox = soup.find("table", id="infoboxtable")
    if not infobox:
        return info

    rows = infobox.find_all("tr")
    current_section = None
    for row in rows:
        cells = row.find_all("td")
        # 检查是否是 section header
        section_cell = row.find("td", id="infoboxsection")
        if section_cell and section_cell.get("colspan") == "2":
            current_section = section_cell.get_text(strip=True)
            continue

        if len(cells) >= 2:
            label_cell = cells[0]
            value_cell = cells[1]
            label = label_cell.get_text(strip=True)
            
            # 特殊处理某些字段
            if label == "Sell Price":
                # 提取数字
                value_text = value_cell.get_text(strip=True)
                # 清理 data-sort-value 标签内容
                value_text = re.sub(r'data-sort-value="[^"]*"\s*', '', value_text)
                value_text = re.sub(r'[gG]$', '', value_text.strip())
                price_match = re.search(r'(\d[\d,]*)', value_text)
                if price_match:
                    info["sell_price"] = int(price_match.group(1).replace(",", ""))
                else:
                    info["sell_price"] = 0
            elif label == "Source":
                info["source"] = value_cell.get_text("•", strip=True)
            elif label in ["Buff(s)", "Buff"]:
                info["buff"] = value_cell.get_text(strip=True)
            elif label == "Energy / Health":
                energy_health = value_cell.get_text(strip=True)
                info["energy_health"] = energy_health
            elif label == "Ingredients":
                info["ingredients"] = value_cell.get_text("•", strip=True)
            elif label == "Recipe":
                info["recipe_from"] = value_cell.get_text(strip=True)
            elif label == "Healing":
                info["healing"] = value_cell.get_text(strip=True)

    return info


def parse_gifting_section(html):
    """从页面 HTML 中解析 Gifting（赠送）部分的数据"""
    gift_data = {"love": [], "like": [], "neutral": [], "dislike": [], "hate": []}
    if not html:
        return gift_data

    soup = BeautifulSoup(html, "lxml")

    # 查找 Gifting 标题
    for h2 in soup.find_all("h2"):
        sp = h2.find("span", class_="mw-headline")
        if sp and "gift" in sp.get_text(strip=True).lower():
            # 找到章节后的表格
            table = h2.find_next("table")
            if not table:
                continue

            # 解析表格行
            for row in table.find_all("tr"):
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    reaction_type = cells[0].get_text(strip=True).lower()
                    villagers_text = cells[1].get_text(strip=True)

                    # 按 • 分割村民名单
                    villager_list = [
                        v.strip()
                        for v in villagers_text.split("•")
                        if v.strip()
                    ]

                    # 验证并归类
                    for v in villager_list:
                        if v in ALL_VILLAGERS:
                            if "love" in reaction_type:
                                gift_data["love"].append(v)
                            elif "like" in reaction_type:
                                gift_data["like"].append(v)
                            elif "neutral" in reaction_type:
                                gift_data["neutral"].append(v)
                            elif "dislike" in reaction_type:
                                gift_data["dislike"].append(v)
                            elif "hate" in reaction_type:
                                gift_data["hate"].append(v)
            break  # 只处理第一个 Gifting 表格

    return gift_data


def download_image(image_url, filename):
    """下载图片到本地"""
    filepath = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(filepath):
        # print(f"  Image already exists: {filename}")
        return True

    try:
        r = requests.get(image_url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        print(f"  ✓ Downloaded image: {filename}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to download {filename}: {e}")
        return False


def get_sell_price_from_page(page_title):
    """从物品页面提取 sell price"""
    html = api_get_page_html(page_title)
    if html:
        info = extract_infobox(html)
        return info.get("sell_price", 0)
    return 0


def scrape_all_items():
    """主爬虫：抓取所有物品数据"""
    print("=" * 60)
    print("星露谷维基百科商品数据抓取器 (增强版)")
    print("=" * 60)

    # Step 1: 从主页面获取所有物品列表
    print("\n[Step 1] 获取物品列表...")
    main_html = api_get_page_html("Stardew_Valley_Wiki")
    if not main_html:
        print("无法获取主页面数据，启用备用方案 - 从表格页面获取")
        main_html = api_get_page_html("Crops")
        if not main_html:
            print("所有方式均失败，退出")
            return

    soup = BeautifulSoup(main_html, "lxml")

    # 查找商品分类表格 - 找 class 包含 wikitable 的 table
    tables = soup.find_all("table", class_="wikitable")
    print(f"  找到 {len(tables)} 个 wikitable 表格")

    # 收集所有物品条目
    items = []
    seen_names = set()

    for table in tables:
        rows = table.find_all("tr")
        for row in rows[1:]:  # 跳过表头
            cells = row.find_all("td")
            if len(cells) < 3:
                continue

            # 第一格通常是图片链接，第二格是物品名，第三格是分类
            img_cell = cells[0]
            name_cell = cells[1]
            cat_cell = cells[2] if len(cells) > 2 else None

            # 提取物品名称
            name_link = name_cell.find("a")
            if not name_link:
                continue
            name = name_link.get_text(strip=True)
            if not name or name in seen_names:
                continue
            seen_names.add(name)

            # 提取分类
            category_en = cat_cell.get_text(strip=True) if cat_cell else "Other"
            category = CATEGORY_MAP.get(category_en, category_en)

            # 提取图片 URL
            img_tag = img_cell.find("img")
            image_url = None
            if img_tag:
                src = img_tag.get("src") or img_tag.get("srcset", "").split(" ")[0]
                if src:
                    if src.startswith("//"):
                        image_url = "https:" + src
                    elif src.startswith("/"):
                        image_url = BASE_URL + src
                    else:
                        image_url = src

            # 提取 wiki 页面链接
            page_url = name_link.get("href", "")
            if page_url.startswith("/"):
                page_url = BASE_URL + page_url

            # 从 wiki URL 提取页面标题
            page_title = name_link.get("title", name)
            if not page_title or page_title == name:
                # 从 URL 提取
                page_title = page_url.split("/")[-1] if "/" in page_url else name

            items.append({
                "name": name,
                "name_url": page_title,
                "category": category,
                "category_en": category_en,
                "image_url": image_url,
                "page_url": page_url,
            })

    print(f"  共发现 {len(items)} 个物品")

    # 如果主页面没找到足够的物品，从更具体的页面补充
    if len(items) < 50:
        print("\n  [补充] 从其他分类页面获取更多物品...")
        extra_pages = [
            "Cooking", "Fish", "Minerals", "Artifacts", "Seeds",
            "Fertilizer", "Artisan_Goods", "Animal_Products",
            "Monster_Loot", "Resources", "Tackle", "Trash"
        ]
        for extra_page in extra_pages:
            html = api_get_page_html(extra_page)
            if not html:
                continue
            extra_soup = BeautifulSoup(html, "lxml")
            for table in extra_soup.find_all("table", class_="wikitable"):
                rows = table.find_all("tr")
                for row in rows[1:]:
                    cells = row.find_all("td")
                    if not cells:
                        continue
                    # 尝试找到带有链接的单元格
                    for cell in cells[:3]:
                        link = cell.find("a")
                        if link and link.get("href", "").startswith("/"):
                            name = link.get_text(strip=True)
                            if name and name not in seen_names:
                                seen_names.add(name)
                                category_en = "Other"
                                if len(cells) > 1:
                                    cat_text = cells[-1].get_text(strip=True)
                                    if cat_text:
                                        category_en = cat_text
                                category = CATEGORY_MAP.get(category_en, category_en)

                                img_tag = cell.find("img")
                                image_url = None
                                if img_tag:
                                    src = img_tag.get("src") or ""
                                    if src.startswith("//"):
                                        image_url = "https:" + src
                                    elif src.startswith("/"):
                                        image_url = BASE_URL + src

                                page_url = link.get("href", "")
                                if page_url.startswith("/"):
                                    page_url = BASE_URL + page_url

                                items.append({
                                    "name": name,
                                    "name_url": link.get("title", name),
                                    "category": category,
                                    "category_en": category_en,
                                    "image_url": image_url,
                                    "page_url": page_url,
                                })
            print(f"    从 {extra_page} 补充了物品")

        print(f"  补充后共 {len(items)} 个物品")

    # Step 2: 逐个抓取每个物品的详细数据
    print(f"\n[Step 2] 抓取详情数据 & 下载图片 (共 {len(items)} 个物品)...")

    full_data = []
    for idx, item in enumerate(items, 1):
        name = item["name"]
        name_url = item["name_url"]
        print(f"\n  [{idx}/{len(items)}] {name}...")

        # 获取页面 HTML
        page_html = api_get_page_html(name_url)
        if not page_html:
            print(f"    ✗ 获取页面失败，使用基础数据")
            full_data.append({
                "id": idx,
                "name": name,
                "category": item["category"],
                "category_en": item["category_en"],
                "price": 0,
                "description": "",
                "sell_price": 0,
                "source": "",
                "buff": "",
                "energy_health": "",
                "ingredients": "",
                "gifting": {"love": [], "like": [], "neutral": [], "dislike": [], "hate": []},
                "image": "",
                "wiki_url": item["page_url"],
            })
            continue

        # 提取信息框数据
        info = extract_infobox(page_html)

        # 提取赠送数据
        gift_data = parse_gifting_section(page_html)

        # 获取描述（第一个段落）
        soup = BeautifulSoup(page_html, "lxml")
        description = ""
        content_div = soup.find("div", class_="mw-parser-output")
        if content_div:
            for p in content_div.find_all("p", recursive=False):
                text = p.get_text(strip=True)
                if len(text) > 20:
                    description = text[:300]
                    break

        # 下载图片
        image_filename = ""
        if item["image_url"]:
            # 从 URL 提取文件名
            image_filename = item["image_url"].split("/")[-1].split("?")[0]
            # 处理文件名编码
            image_filename = requests.utils.unquote(image_filename)
            download_image(item["image_url"], image_filename)

        # 组装完整数据
        item_data = {
            "id": idx,
            "name": name,
            "category": item["category"],
            "category_en": item["category_en"],
            "price": info.get("sell_price", 0),
            "sell_price": info.get("sell_price", 0),
            "description": description,
            "source": info.get("source", ""),
            "buff": info.get("buff", ""),
            "energy_health": info.get("energy_health", ""),
            "ingredients": info.get("ingredients", ""),
            "recipe_from": info.get("recipe_from", ""),
            "gifting": gift_data,
            "image": f"images/{image_filename}" if image_filename else "",
            "wiki_url": item["page_url"],
        }

        full_data.append(item_data)
        print(f"    ✓ 价格: {info.get('sell_price', '?')} | 喜爱: {len(gift_data['love'])}人 | 讨厌: {len(gift_data['hate'])}人")

        # 适度延迟，避免过于频繁请求
        time.sleep(0.3)

    # Step 3: 保存数据
    print(f"\n[Step 3] 保存数据...")

    # 保存完整数据
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 完整数据已保存到: {DATA_FILE} ({len(full_data)} 个物品)")

    # 保存简化数据（前端用）
    simple_data = []
    for item in full_data:
        # 判断是否为最爱物品（某村民的最爱）
        love_villagers = item["gifting"]["love"]
        simple_data.append({
            "id": item["id"],
            "name": item["name"],
            "category": item["category"],
            "category_en": item["category_en"],
            "price": item["price"],
            "image": item["image"],
            "source": item["source"],
            "buff": item["buff"],
            "energy_health": item["energy_health"],
            "ingredients": item["ingredients"],
            "gifting": {
                "love": item["gifting"]["love"],
                "like": item["gifting"]["like"],
                "neutral": item["gifting"]["neutral"],
                "dislike": item["gifting"]["dislike"],
                "hate": item["gifting"]["hate"],
            }
        })

    with open(SIMPLE_FILE, "w", encoding="utf-8") as f:
        json.dump(simple_data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 简化数据已保存到: {SIMPLE_FILE}")

    # 统计
    total_items = len(full_data)
    with_images = sum(1 for i in full_data if i["image"])
    with_gift_data = sum(1 for i in full_data if i["gifting"]["love"] or i["gifting"]["like"])
    
    print(f"\n{'='*60}")
    print(f"抓取完成！统计：")
    print(f"  - 总物品数: {total_items}")
    print(f"  - 有图片: {with_images}")
    print(f"  - 有赠送数据: {with_gift_data}")
    print(f"  - 图片目录: {IMAGE_DIR}")
    print(f"{'='*60}")

    return full_data


if __name__ == "__main__":
    scrape_all_items()