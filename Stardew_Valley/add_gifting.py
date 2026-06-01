#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为已有物品数据补充村民喜好（赠送）信息
批量读取 items_simple.json，为每个物品页面爬取赠送数据
支持断点续传：每处理 15 个物品自动保存
"""

import requests
import json
import os
import sys
import time
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://stardewvalleywiki.com"
API_URL = f"{BASE_URL}/mediawiki/api.php"
HEADERS = {"User-Agent": "StardewValleyDataCollector/1.0"}
BASE_DIR = os.path.dirname(__file__)
SIMPLE_FILE = os.path.join(BASE_DIR, "items_simple.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "items_gift.json")
CHECKPOINT_FILE = os.path.join(BASE_DIR, "items_gift_checkpoint.json")
LOG_FILE = os.path.join(BASE_DIR, "gift_progress.log")

ALL_VILLAGERS = [
    "Abigail", "Alex", "Caroline", "Clint", "Demetrius", "Dwarf", "Elliott",
    "Emily", "Evelyn", "George", "Gus", "Haley", "Harvey", "Jas", "Jodi",
    "Kent", "Krobus", "Leah", "Leo", "Lewis", "Linus", "Marnie", "Maru",
    "Pam", "Penny", "Pierre", "Robin", "Sam", "Sandy", "Sebastian", "Shane",
    "Vincent", "Willy", "Wizard"
]

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(msg)

def api_get_page_html(title):
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "format": "json",
        "redirects": "true",
    }
    for attempt in range(3):
        try:
            r = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                return None
            return data["parse"]["text"]["*"]
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
    return None


def extract_gifting_from_page(html):
    gift_data = {"love": [], "like": [], "neutral": [], "dislike": [], "hate": []}
    if not html:
        return gift_data

    soup = BeautifulSoup(html, "lxml")
    for h2 in soup.find_all("h2"):
        sp = h2.find("span", class_="mw-headline")
        if sp and "gift" in sp.get_text(strip=True).lower():
            table = h2.find_next("table")
            if not table:
                continue
            for row in table.find_all("tr"):
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    reaction_type = cells[0].get_text(strip=True).lower()
                    villagers_text = cells[1].get_text(strip=True)
                    villager_list = [v.strip() for v in villagers_text.split("•") if v.strip()]
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
            break
    return gift_data


def extract_infobox(html):
    info = {}
    if not html:
        return info
    soup = BeautifulSoup(html, "lxml")
    infobox = soup.find("table", id="infoboxtable")
    if not infobox:
        return info
    rows = infobox.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 2:
            label = cells[0].get_text(strip=True)
            if label == "Source":
                info["source"] = cells[1].get_text("•", strip=True)
            elif label in ["Buff(s)", "Buff"]:
                info["buff"] = cells[1].get_text(strip=True)
            elif label == "Energy / Health":
                info["energy_health"] = cells[1].get_text(strip=True)
            elif label == "Ingredients":
                info["ingredients"] = cells[1].get_text("•", strip=True)
    return info


def save_checkpoint(items, processed_idx):
    """保存检查点"""
    data = {
        "processed_idx": processed_idx,
        "items": items
    }
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # 同时保存最终输出
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def main():
    log("=" * 60)
    log("补充村民喜好数据（支持断点续传）")
    log("=" * 60)

    # 优先从检查点恢复
    items = []
    start_idx = 0

    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                cp = json.load(f)
            items = cp.get("items", [])
            start_idx = cp.get("processed_idx", 0)
            log(f"📦 从检查点恢复：已处理到第 {start_idx} 个物品")
        except:
            pass

    if not items:
        if not os.path.exists(SIMPLE_FILE):
            log(f"❌ 找不到数据文件: {SIMPLE_FILE}")
            return
        with open(SIMPLE_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)
        start_idx = 0
        log(f"📦 从零开始，加载 {len(items)} 个物品")

    updated = items[:start_idx] if start_idx > 0 else []
    total = len(items)
    success = 0
    skip = 0
    
    for idx in range(start_idx, total):
        item = items[idx]
        name = item["name"]
        page_title = name.replace(" ", "_")
        
        # 如果已经有赠送数据且不为空，跳过
        if "gifting" in item and (item["gifting"].get("love") or item["gifting"].get("like") or 
                                  item["gifting"].get("hate") or item["gifting"].get("dislike") or
                                  item["gifting"].get("neutral")):
            log(f"[{idx+1}/{total}] {name} ⏭ 已有数据")
            updated.append(item)
            skip += 1
            continue

        # 获取页面HTML
        page_html = api_get_page_html(page_title)
        if not page_html:
            # 尝试 URL 编码
            from urllib.parse import quote
            page_title_enc = quote(name.replace(" ", "_"))
            page_html = api_get_page_html(page_title_enc)
        
        if not page_html:
            log(f"[{idx+1}/{total}] {name} ❌ 获取页面失败")
            if "gifting" not in item:
                item["gifting"] = {"love": [], "like": [], "neutral": [], "dislike": [], "hate": []}
            updated.append(item)
            # 每 15 个保存一次检查点
            if (idx + 1) % 15 == 0:
                save_checkpoint(updated, idx + 1)
            continue

        # 提取赠送数据
        gift_data = extract_gifting_from_page(page_html)

        # 也提取额外信息
        info = extract_infobox(page_html)
        for key in ["source", "buff", "energy_health", "ingredients"]:
            if info.get(key) and not item.get(key):
                item[key] = info[key]

        item["gifting"] = gift_data
        updated.append(item)
        success += 1

        total_lovers = len(gift_data["love"]) + len(gift_data["like"])
        total_haters = len(gift_data["hate"]) + len(gift_data["dislike"])
        log(f"[{idx+1}/{total}] {name} ✓ 最爱:{len(gift_data['love'])} 讨厌:{len(gift_data['hate'])}")

        # 每 15 个保存一次检查点
        if (idx + 1) % 15 == 0:
            save_checkpoint(updated, idx + 1)
            log(f"💾 已保存检查点（第 {idx+1} 个）")
        
        # 延迟
        time.sleep(0.5)

    # 最终保存
    save_checkpoint(updated, total)

    log(f"\n{'='*60}")
    log(f"✅ 完成！统计：")
    log(f"  成功更新: {success}")
    log(f"  跳过: {skip}")
    log(f"  总物品: {len(updated)}")
    log(f"  输出: {OUTPUT_FILE}")
    log(f"{'='*60}")


if __name__ == "__main__":
    main()