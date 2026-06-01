#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
星露谷物品数据最终生成器 - v3
- 19个完整分类
- 星露谷中文维基百科标准翻译
- 所有物品正确价格
- 作物/季节采集物品质星级定价
- 完整的赠送数据
"""
import json, os, unicodedata, copy, re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(filename):
    with open(os.path.join(BASE_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    with open(os.path.join(BASE_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===== 已知价格表（从星露谷官方维基获取，用于补充scraper未能提取的价格） =====
KNOWN_PRICES = {
    # === 工匠制品 (Artisan Goods) ===
    "Aged Roe": 400, "Coffee": 150, "Dried Fruit": 100, "Dried Mushrooms": 100,
    "Juice": 75, "Mystic Syrup": 4000, "Oil": 100, "Raisins": 600,
    "Smoked Fish": 100, "Wine": 400, "Roe": 100, "Slime": 0, "Slime Ball": 0,
    # === 怪物战利品 (Monster Loot) ===
    "Bat Wing": 15, "Bug Meat": 30, "Solar Essence": 80, "Void Essence": 80,
    "Spider Eggs": 50, "Gooey Glob": 100, "Cursed Doll": 1000,
    # === 资源 (Resources) ===
    "Battery Pack": 500, "Bone Fragment": 3, "Cinder Shard": 5,
    "Clay": 20, "Coal": 15, "Copper Ore": 5, "Fiber": 5, "Gold Ore": 25,
    "Hardwood": 15, "Iridium Bar": 1000, "Iridium Ore": 100, "Iron Ore": 10,
    "Moss": 5, "Radioactive Ore": 300, "Radioactive Bar": 1500,
    "Refined Quartz": 300, "Stone": 2, "Wood": 2, "Copper Bar": 100,
    "Gold Bar": 400, "Iron Bar": 200, "Oak Resin": 150, "Pine Tar": 100,
    "Maple Syrup": 200, "Sap": 2,
    # === 动物制品 (Animal Products) ===
    "Brown Egg": 50, "White Egg": 50, "Duck Egg": 80, "Void Egg": 300,
    "Golden Egg": 2000, "Large Brown Egg": 75, "Large White Egg": 75,
    "Milk": 125, "Large Milk": 175, "Goat Milk": 225, "Large Goat Milk": 300,
    "Ostrich Egg": 600, "Duck Feather": 250, "Rabbit's Foot": 565,
    "Wool": 340, "Truffle": 625,
    # === 渔具 (Fishing Tackle) ===
    "Barbed Hook": 500, "Cork Bobber": 750, "Curiosity Lure": 500,
    "Dressed Spinner": 500, "Lead Bobber": 200, "Quality Bobber": 750,
    "Sonar Bobber": 300, "Spinner": 250, "Trap Bobber": 400,
    "Treasure Hunter": 400, "Magnet": 1000, "Wild Bait": 5, "Bait": 5,
    "Challenge Bait": 5,
    # === 种子 (Seeds) ===
    "Mixed Seeds": 20, "Mixed Flower Seeds": 30, "Acorn": 20, "Maple Seed": 20,
    "Pine Cone": 20, "Mahogany Seed": 50, "Mushroom Tree Seed": 500,
    "Mystic Tree Seed": 1000, "Cactus Seeds": 150, "Fiber Seeds": 25,
    "Qi Bean": 5, "Tea Sapling": 500, "Mossy Seed": 10,
    # === 肥料 (Fertilizer) ===
    "Basic Fertilizer": 10, "Basic Retaining Soil": 10,
    "Deluxe Fertilizer": 40, "Deluxe Retaining Soil": 20,
    "Deluxe Speed-Gro": 80, "Hyper Speed-Gro": 100,
    "Quality Fertilizer": 20, "Quality Retaining Soil": 10,
    "Speed-Gro": 20, "Tree Fertilizer": 25,
    # === 书 ===
    "Book of Stars": 20000, "Queen of Sauce Cookbook": 5000,
    "Woodskip": 75, "Stardew Valley Almanac": 20000,
    # === 帽子 ===
    "Cowboy Hat": 2000, "Bowler Hat": 2000, "Top Hat": 4000, "Fedora": 3000,
    "Cowgal Hat": 2000, "Skeleton Mask": 3000, "Goggles": 2000,
    "Eye Mask": 2000, "Straw Hat": 2000, "Sombrero": 4000,
    "Hard Hat": 4000, "Hunter's Cap": 1500, "Knight's Helmet": 4000,
    "Wizard Hat": 4000, "Party Hat": 4000, "Santa Hat": 4000,
    "Trucker Hat": 4000, "Propeller Hat": 2000, "Archer's Cap": 1500,
    "Miner's Helmet": 1500,
    # === 鞋类 ===
    "Leather Boots": 500, "Work Boots": 500, "Combat Boots": 750,
    "Tundra Boots": 1000, "Crystal Shoes": 1250, "Space Boots": 1250,
    "Firewalker Boots": 1500, "Dragonscale Boots": 2000,
    "Emily's Magic Boots": 2500, "Genie Shoes": 2000, "Prismatic Shoes": 3000,
    "Cinderclown Shoes": 1500, "Merman's Boots": 2000,
    # === 戒指 ===
    "Small Glow Ring": 100, "Glow Ring": 250, "Small Magnet Ring": 100,
    "Magnet Ring": 250, "Slime Charmer Ring": 1500, "Warrior Ring": 1000,
    "Vampire Ring": 1500, "Ring of Yoba": 1500, "Sturdy Ring": 1500,
    "Burglar's Ring": 1000, "Iridium Band": 5000, "Jade Ring": 1000,
    "Amethyst Ring": 1000, "Topaz Ring": 1000, "Aquamarine Ring": 1000,
    "Ruby Ring": 1000, "Emerald Ring": 1000, "Hot Java Ring": 2500,
    "Glowstone Ring": 2000, "Thorns Ring": 1500, "Savage Ring": 1500,
    "Immunity Band": 1000, "Napalm Ring": 5000, "Phoenix Ring": 5000,
    "Soul Sapper Ring": 5000, "Ring of Forging": 5000, "Lucky Ring": 7500,
    "Ring of Fates": 5000,
    # === 武器 ===
    "Rusty Sword": 100, "Silver Saber": 750, "Dark Sword": 800,
    "Crystal Sword": 900, "Holy Blade": 1000, "Lava Katana": 2500,
    "Galaxy Sword": 5000, "Infinity Blade": 10000, "Wooden Blade": 50,
    "Iron Dirk": 125, "Burglar's Shank": 600, "Shadow Dagger": 200,
    "Galaxy Dagger": 3500, "Infinity Dagger": 8000, "Insect Head": 500,
    "Steel Smallsword": 500, "Cutlass": 800, "Claymore": 700,
    "Templar's Blade": 1500, "Obsidian Edge": 1200, "Bone Sword": 600,
    "Galaxy Hammer": 3500, "Infinity Gavel": 8000, "Wood Club": 150,
    "Iron Edge": 400, "Lead Rod": 200, "Slingshot": 500,
    "Master Slingshot": 1000, "Galaxy Slingshot": 5000,
    "Femur": 80, "Ossified Blade": 1500, "Yeti Tooth": 1000,
    "Forest Sword": 900, "Tempered Broadsword": 1500, "Steel Falchion": 2000,
    "Wicked Kris": 800, "Wind Spire": 600, "Dragontooth Cutlass": 3000,
    "Dragontooth Shiv": 1500, "Dragontooth Club": 2000, "Ibis Hook": 1500,
    "Rapier": 1500, "Dwarf Sword": 2000, "Dwarf Dagger": 1000, "Dwarf Hammer": 2000,
    "Dwarf Gadget": 500,
    # === 矿物 ===
    "Diamond": 750, "Prismatic Shard": 2000, "Aquamarine": 180,
    "Emerald": 250, "Jade": 200, "Ruby": 300, "Amethyst": 100,
    "Topaz": 120, "Earth Crystal": 200, "Frozen Tear": 200,
    "Fire Quartz": 120, "Quartz": 50,
    "Aerinite": 120, "Alamite": 130, "Baryte": 70, "Basalt": 120,
    "Bixite": 140, "Calcifur": 150, "Celestine": 110, "Cinnabar": 130,
    "Dolomite": 150, "Esperite": 180, "Fairy Stone": 180,
    "Fire Opal": 200, "Fluorapatite": 150, "Garnet": 160,
    "Geminite": 200, "Ghost Crystal": 150, "Granite": 75,
    "Hematite": 150, "Honey Agate": 150, "Jagoite": 160,
    "Jasper": 150, "Kyanite": 150, "Lemon Stone": 150,
    "Limestone": 60, "Lunarite": 200, "Malachite": 100,
    "Marble": 110, "Mudstone": 50, "Neptunite": 250,
    "Nekoite": 150, "Obsidian": 200, "Ocean Stone": 150,
    "Opal": 200, "Orpiment": 140, "Petrified Slime": 120,
    "Sandstone": 50, "Slate": 50, "Soapstone": 70,
    "Star Shards": 200, "Thunder Egg": 150, "Tigerseye": 150,
    # === 古物 (已存在于items_zh，补充价格为0的) ===
    "Ancient Doll": 250, "Ancient Seed": 0, "Arrowhead": 100,
    "Bone Flute": 200, "Chicken Statue": 200, "Chewing Stick": 100,
    "Dwarf Gadget": 200, "Dwarvish Helm": 200,
    "Dwarf Scroll I": 10, "Dwarf Scroll II": 10, "Dwarf Scroll III": 10,
    "Dwarf Scroll IV": 10, "Elvish Jewelry": 300, "Glass Shards": 10,
    "Golden Mask": 500, "Golden Relic": 500, "Ornamental Fan": 300,
    "Prehistoric Rib": 100, "Prehistoric Skull": 200, "Prehistoric Tool": 100,
    "Rusty Spoon": 50, "Rusty Spur": 50, "Rusty Cog": 50,
    "Rare Disc": 300, "Skeletal Hand": 100, "Skeletal Tail": 100,
    "Amphibian Fossil": 100, "Palm Fossil": 100, "Trilobite": 150,
    "Bone Fragment": 3, "Dried Starfish": 50, "Large Animal Fossil": 150,
    "Prehistoric Tibia": 100, "Prehistoric Vertebra": 100,
    "Snake Skull": 150, "Snake Vertebrae": 100,
    "Strange Doll (green)": 1000, "Strange Doll (yellow)": 1000,
    "Ancient Drum": 200, "Ancient Sword": 200, "Anchor": 100,
    "Chipped Amphora": 100, "Nautilus Fossil": 100, "Prehistoric Handaxe": 100,
    "Prehistoric Scapula": 100,
    "Chub": 50, "Rainbow Trout": 65, "Walleye": 105, "Perch": 85,
    "Lingcod": 120, "Largemouth Bass": 100, "Carp": 30, "Bullhead": 75,
    "Sturgeon": 90, "Midnight Carp": 105, "Sunfish": 30, "Catfish": 200,
    "Bream": 45, "Shad": 60, "Pike": 100, "Dorado": 100, "Salmon": 75,
    "Tiger Trout": 150, "Shrimp": 60, "Snail": 65, "Periwinkle": 20,
    "Lobster": 120, "Crayfish": 75, "Crab": 100, "Cockle": 50,
    "Mussel": 30, "Squid": 80, "Tuna": 100, "Sardine": 40,
    "Bream": 45, "Eel": 85, "Octopus": 150, "Red Mullet": 75,
    "Herring": 30, "Anchovy": 30, "Ghostfish": 45, "Sandfish": 75,
    "Woodskip": 75, "Void Salmon": 150, "Slimejack": 100,
    "Scorpion Carp": 150, "Flounder": 100, "Midnight Squid": 100,
    "Spook Fish": 120, "Blobfish": 200, "Halibut": 90,
    "Lava Eel": 700, "Glacierfish": 450, "Crimsonfish": 700,
    "Angler": 600, "Legend": 5000, "Mutant Carp": 1000,
    "Glacierfish Jr.": 450, "Ms. Angler": 600, "Son of Crimsonfish": 700,
    "Legend II": 5000, "Radioactive Carp": 1000,
    "River Jelly": 250, "Sea Jelly": 250, "Cave Jelly": 250,
    # === 垃圾 ===
    "Trash (item)": 0, "Driftwood": 0, "Broken Glasses": 0,
    "Broken CD": 0, "Soggy Newspaper": 0, "Joja Cola": 25,
}

# ===== 19个标准分类 =====
REQUESTED_CATEGORIES = [
    "作物", "动物", "果树", "工匠制品", "家具", "墙纸", "地板",
    "矿物", "渔具", "武器", "帽子", "鞋类", "戒指", "菜品",
    "农场工具", "古物", "怪物战利品", "书", "季节采集物"
]

# 需要品质星级的分类
QUALITY_CATEGORIES = ["作物", "季节采集物"]

# ===== 分类映射 (English category -> Chinese) =====
CATEGORY_MAP = {
    "蔬菜": "作物", "水果": "作物", "Fruit": "作物", "Vegetable": "作物",
    "动物制品": "动物", "Animal Products": "动物",
    "工匠制品": "工匠制品", "Artisan Goods": "工匠制品",
    "家具": "家具", "Furniture": "家具",
    "墙纸": "墙纸", "Wallpaper": "墙纸",
    "地板": "地板", "Floor": "地板",
    "矿物": "矿物", "Mineral": "矿物", "Minerals": "矿物",
    "古物": "古物", "Artifact": "古物", "Artifacts": "古物",
    "渔具": "渔具", "Fishing Tackle": "渔具", "Tackle": "渔具", "Bait": "渔具",
    "武器": "武器", "Weapon": "武器", "Weapons": "武器",
    "帽子": "帽子", "Hat": "帽子", "Hats": "帽子",
    "鞋类": "鞋类", "Boots": "鞋类", "Shoes": "鞋类",
    "戒指": "戒指", "Ring": "戒指", "Rings": "戒指",
    "烹饪": "菜品", "Cooking": "菜品",
    "农场工具": "农场工具", "Tool": "农场工具", "Tools": "农场工具",
    "肥料": "农场工具", "Fertilizer": "农场工具",
    "种子": "作物", "Seeds": "作物",
    "怪物战利品": "怪物战利品", "Monster Loot": "怪物战利品",
    "书": "书", "Book": "书", "Books": "书",
    "资源": "资源", "Resources": "资源",
    "垃圾": "垃圾", "Trash": "垃圾",
    "基础": "资源", "Basic": "资源",
    "材料": "资源", "Crafting": "资源",
    "装饰": "家具", "Decor": "家具",
    "装备": "装备", "Equipment": "装备",
    "鱼类": "渔具", "Fish": "渔具",
    "种子": "作物",
    "果树": "果树", "Fruit Trees": "果树",
    "季节采集物": "季节采集物", "Forage": "季节采集物",
    "Foraging": "季节采集物", "采集": "季节采集物",
}

# ===== 英文名 -> 中文标准翻译映射 =====
EN_TO_ZH = {
    # === 作物/蔬菜 ===
    "Amaranth": "苋菜", "Artichoke": "洋蓟", "Beet": "甜菜",
    "Bok Choy": "大白菜", "Broccoli": "西兰花", "Carrot": "胡萝卜",
    "Cauliflower": "花椰菜", "Corn": "玉米", "Eggplant": "茄子",
    "Fiddlehead Fern": "蕨菜", "Garlic": "大蒜", "Green Bean": "绿豆",
    "Hops": "啤酒花", "Kale": "甘蓝菜", "Parsnip": "防风草",
    "Potato": "土豆", "Pumpkin": "南瓜", "Radish": "萝卜",
    "Red Cabbage": "红叶卷心菜", "Taro Root": "芋头",
    "Tea Leaves": "茶叶", "Tomato": "西红柿",
    "Unmilled Rice": "未碾米", "Wheat": "小麦", "Yam": "山药",
    "Summer Squash": "西葫芦",
    # === 水果(作物) ===
    "Blueberry": "蓝莓", "Cactus Fruit": "仙人掌果子",
    "Cranberries": "蔓越莓", "Hot Pepper": "辣椒", "Melon": "甜瓜",
    "Starfruit": "杨桃", "Strawberry": "草莓", "Ancient Fruit": "上古水果",
    "Rhubarb": "大黄", "Sweet Gem Berry": "甜宝石",
    "Coffee Bean": "咖啡豆", "Powdermelon": "粉瓜", "Qi Fruit": "齐瓜",
    "Pineapple": "菠萝",
    # === 花(归入作物) ===
    "Blue Jazz": "蓝爵", "Fairy Rose": "玫瑰仙子", "Poppy": "虞美人花",
    "Summer Spangle": "夏季亮片", "Sunflower": "向日葵", "Tulip": "郁金香",
    # === 果树水果 ===
    "Apple": "苹果", "Apricot": "杏子", "Banana": "香蕉",
    "Cherry": "樱桃", "Mango": "芒果", "Orange": "橙子",
    "Peach": "桃子", "Pomegranate": "石榴",
    # === 季节采集物 ===
    "Wild Horseradish": "野山葵", "Spice Berry": "香料浆果",
    "Spring Onion": "大葱", "Leek": "韭菜", "Dandelion": "蒲公英",
    "Salmonberry": "美洲大树莓", "Morel": "羊肚菌",
    "Common Mushroom": "普通蘑菇", "Hazelnut": "榛子",
    "Wild Plum": "野梅", "Blackberry": "黑莓",
    "Chanterelle": "鸡油菌", "Red Mushroom": "红蘑菇",
    "Purple Mushroom": "紫蘑菇", "Coconut": "椰子",
    "Rainbow Shell": "彩虹贝壳", "Coral": "珊瑚",
    "Nautilus Shell": "鹦鹉螺", "Sea Urchin": "海胆",
    "Snow Yam": "雪山药", "Winter Root": "冬根",
    "Crystal Fruit": "水晶果", "Holly": "冬青树",
    "Ginger": "姜", "Magma Cap": "熔岩菇",
    "Sap": "树液", "Moss": "苔藓",
    "Fossilized Leg": "化石腿", "Fossilized Ribs": "化石肋骨",
    "Fossilized Skull": "化石头骨", "Fossilized Spine": "化石脊柱",
    "Fossilized Tail": "化石尾巴",
    # === 动物产品 ===
    "Brown Egg": "棕色鸡蛋", "White Egg": "白色鸡蛋",
    "Duck Egg": "鸭蛋", "Void Egg": "虚空蛋", "Golden Egg": "金蛋",
    "Large Brown Egg": "大棕色鸡蛋", "Large White Egg": "大白色鸡蛋",
    "Egg": "鸡蛋", "Large Egg": "大鸡蛋",
    "Milk": "牛奶", "Large Milk": "大壶牛奶",
    "Goat Milk": "羊奶", "Large Goat Milk": "大壶羊奶",
    "Ostrich Egg": "鸵鸟蛋", "Duck Feather": "鸭毛",
    "Rabbit's Foot": "兔子的脚", "Wool": "动物毛",
    "Slime": "史莱姆", "Slime Ball": "史莱姆球", "Truffle": "松露",
    # === 工匠制品 ===
    "Aged Roe": "陈酿鱼子酱", "Beer": "啤酒", "Caviar": "鱼子酱",
    "Cheese": "奶酪", "Cloth": "布料", "Coffee": "咖啡",
    "Dinosaur Mayonnaise": "恐龙蛋黄酱", "Dried Fruit": "水果干",
    "Dried Mushrooms": "蘑菇干", "Duck Mayonnaise": "鸭蛋黄酱",
    "Goat Cheese": "羊奶酪", "Green Tea": "绿茶", "Honey": "蜂蜜",
    "Juice": "果汁", "Maple Syrup": "枫糖浆",
    "Mayonnaise": "蛋黄酱", "Mead": "蜜蜂酒",
    "Mystic Syrup": "神秘糖浆", "Oak Resin": "橡树树脂",
    "Oil": "油", "Pale Ale": "淡啤酒", "Pine Tar": "松焦油",
    "Raisins": "葡萄干", "Roe": "鱼子", "Smoked Fish": "熏鱼",
    "Truffle Oil": "松露油", "Void Mayonnaise": "虚空蛋黄酱",
    "Wine": "果酒",
    # === 矿物 ===
    "Diamond": "钻石", "Prismatic Shard": "五彩碎片",
    "Aquamarine": "海蓝宝石", "Emerald": "绿宝石", "Jade": "翡翠",
    "Ruby": "红宝石", "Amethyst": "紫水晶", "Topaz": "黄水晶",
    "Earth Crystal": "地晶", "Frozen Tear": "泪晶",
    "Fire Quartz": "火石英", "Quartz": "石英",
    "Aerinite": "蓝纹石", "Alamite": "铝辉石", "Baryte": "重晶石",
    "Basalt": "玄武岩", "Bixite": "黑方石", "Calcifur": "氟磷灰石",
    "Celestine": "天青石", "Cinnabar": "辰砂",
    "Dolomite": "白云石", "Esperite": "硅锌矿", "Fairy Stone": "仙石",
    "Fire Opal": "火蛋白石", "Fluorapatite": "氟磷灰石",
    "Garnet": "石榴石", "Geminite": "宝石", "Ghost Crystal": "幽灵水晶",
    "Granite": "花岗岩", "Hematite": "赤铁矿", "Honey Agate": "蜜纹玛瑙",
    "Jagoite": "硅铁铅矿", "Jasper": "碧玉", "Kyanite": "蓝晶石",
    "Lemon Stone": "柠檬石", "Limestone": "石灰岩", "Lunarite": "月球石",
    "Malachite": "孔雀石", "Marble": "大理石", "Mudstone": "泥岩",
    "Neptunite": "硅钛钠石", "Nekoite": "针硅钙石", "Obsidian": "黑曜石",
    "Ocean Stone": "海洋石", "Opal": "蛋白石", "Orpiment": "雌黄",
    "Petrified Slime": "石化史莱姆",
    "Sandstone": "砂岩", "Slate": "板岩", "Soapstone": "皂石",
    "Star Shards": "星碎", "Thunder Egg": "雷公蛋", "Tigerseye": "虎眼石",
    # === 古物 ===
    "Ancient Doll": "古代玩偶", "Ancient Seed": "古代种子",
    "Arrowhead": "箭头", "Bone Flute": "骨笛", "Chicken Statue": "鸡雕像",
    "Chewing Stick": "咀嚼棒", "Dwarf Gadget": "矮人小工具",
    "Dwarvish Helm": "矮人头盔",
    "Dwarf Scroll I": "矮人卷轴 I", "Dwarf Scroll II": "矮人卷轴 II",
    "Dwarf Scroll III": "矮人卷轴 III", "Dwarf Scroll IV": "矮人卷轴 IV",
    "Elvish Jewelry": "精灵珠宝", "Glass Shards": "玻璃碎片",
    "Golden Mask": "黄金面具", "Golden Relic": "黄金遗物",
    "Ornamental Fan": "装饰扇子",
    "Prehistoric Rib": "史前肋骨", "Prehistoric Skull": "史前头骨",
    "Prehistoric Tool": "史前工具",
    "Rusty Spoon": "生锈的勺子", "Rusty Spur": "生锈的马刺",
    "Rusty Cog": "生锈的齿轮", "Rare Disc": "稀有圆盘",
    "Skeletal Hand": "骷髅手部", "Skeletal Tail": "骷髅尾部",
    "Amphibian Fossil": "两栖动物化石", "Palm Fossil": "棕榈化石",
    "Trilobite": "三叶虫", "Bone Fragment": "骨头碎片",
    "Dried Starfish": "干海星", "Large Animal Fossil": "大型动物化石",
    "Prehistoric Tibia": "史前胫骨", "Prehistoric Vertebra": "史前脊椎",
    "Snake Skull": "蛇头骨", "Snake Vertebrae": "蛇脊椎",
    "Strange Doll (green)": "诡异玩偶(绿)", "Strange Doll (yellow)": "诡异玩偶(黄)",
    "Ancient Drum": "古代鼓", "Ancient Sword": "古剑", "Anchor": "船锚",
    "Chipped Amphora": "碎双耳瓶", "Nautilus Fossil": "鹦鹉螺化石",
    "Prehistoric Handaxe": "史前手斧", "Prehistoric Scapula": "史前肩胛骨",
    # === 菜品 ===
    "Fried Egg": "煎鸡蛋", "Omelet": "欧姆蛋", "Salad": "沙拉",
    "Cheese Cauliflower": "乳酪花椰菜", "Baked Fish": "烤鱼",
    "Parsnip Soup": "防风草汤", "Vegetable Medley": "混合蔬菜",
    "Complete Breakfast": "完美早餐", "Fried Calamari": "炸鱿鱼",
    "Strange Bun": "奇怪的小面包", "Lucky Lunch": "幸运午餐",
    "Fried Mushroom": "炒蘑菇", "Pizza": "披萨", "Bean Hotpot": "豆类火锅",
    "Glazed Yams": "琉璃山药", "Carp Surprise": "惊奇鲤鱼",
    "Hashbrowns": "薯饼", "Pancakes": "薄煎饼",
    "Mango Sticky Rice": "芒果糯米饭", "Rhubarb Pie": "大黄派",
    "Cranberry Sauce": "蔓越莓酱", "Stuffing": "塞料面包",
    "Coleslaw": "卷心菜沙拉", "Autumn's Bounty": "秋日恩赐",
    "Bruschetta": "意式烤面包", "Chocolate Cake": "巧克力蛋糕",
    "Pumpkin Pie": "南瓜派", "Rabbit's Stew": "烩兔肉",
    "Fish Taco": "鱼肉卷", "Crispy Bass": "香酥鲈鱼",
    "Plum Pudding": "葡萄干布丁", "Chowder": "蛤蜊浓汤",
    "Trout Soup": "鳟鱼汤", "Ice Cream": "冰淇淋",
    "Crab Cakes": "蟹肉糕", "Bouillabaisse": "法式海鲜汤",
    "Algae Soup": "清汤", "Pale Broth": "清炖肉汤",
    "Pumpkin Soup": "南瓜汤", "Tom Kha Soup": "冬阴功汤",
    "Maple Bar": "枫糖棒", "Pink Cake": "粉红蛋糕",
    "Rice Pudding": "大米布丁", "Maki Roll": "生鱼寿司",
    "Sashimi": "生鱼片", "Tortilla": "墨西哥薄饼",
    "Triple Shot Espresso": "三倍浓缩咖啡", "Seafoam Pudding": "海泡布丁",
    "Dish O' The Sea": "海鲜杂烩", "Farmer's Lunch": "农夫午餐",
    "Survival Burger": "救生汉堡", "Pepper Poppers": "爆炒青椒",
    "Bread": "面包", "Cookie": "饼干", "Spaghetti": "意大利面",
    "Eggplant Parmesan": "帕尔玛茄子", "Stir Fry": "爆炒",
    "Blackberry Cobbler": "黑莓脆皮饼", "Cranberry Candy": "蔓越莓糖果",
    "Blueberry Tart": "蓝莓挞", "Fiddlehead Risotto": "蕨菜炖饭",
    "Salmon Dinner": "三文鱼晚餐", "Fish Stew": "鱼汤",
    "Red Plate": "红之盛宴", "Lobster Bisque": "龙虾浓汤",
    "Escargot": "蜗牛沙拉", "Mango Poppyseed Muffin": "芒果松饼",
    "Poppyseed Muffin": "松饼", "Tropical Curry": "热带咖喱",
    "Squid Ink Ravioli": "鱿鱼墨汁意饺", "Ginger Ale": "姜汁汽水",
    "Banana Pudding": "香蕉布丁", "Spicy Eel": "香辣鳗鱼",
    "Fried Eel": "炸鳗鱼", "Roasted Hazelnuts": "烤榛子",
    "Radish Salad": "萝卜沙拉", "Roots Platter": "块茎拼盘",
    "Shrimp Cocktail": "鲜虾开胃菜", "Super Meal": "超级餐",
    "Miner's Treat": "矿工小吃", "Moss Soup": "苔藓汤",
    "Poi": "芋泥", "Fruit Salad": "水果沙拉",
    "Artichoke Dip": "洋蓟蘸酱",
    # === 渔具 ===
    "Barbed Hook": "倒刺钩", "Cork Bobber": "软木塞浮标",
    "Curiosity Lure": "好奇心鱼饵", "Dressed Spinner": "装饰旋转亮片",
    "Lead Bobber": "铅制浮标", "Quality Bobber": "优质浮标",
    "Sonar Bobber": "声纳浮标", "Spinner": "旋转亮片",
    "Trap Bobber": "陷阱浮标", "Treasure Hunter": "寻宝者",
    "Magnet": "磁铁", "Wild Bait": "野生鱼饵", "Bait": "鱼饵",
    "Challenge Bait": "挑战鱼饵", "Deluxe Bait": "豪华鱼饵",
    # === 武器 ===
    "Rusty Sword": "生锈的剑", "Silver Saber": "银剑",
    "Dark Sword": "黑暗之剑", "Crystal Sword": "水晶剑",
    "Holy Blade": "神圣之剑", "Lava Katana": "熔岩武士刀",
    "Galaxy Sword": "银河剑", "Infinity Blade": "无限之剑",
    "Wooden Blade": "木剑", "Iron Dirk": "铁短剑",
    "Burglar's Shank": "窃贼匕首", "Shadow Dagger": "暗影匕首",
    "Galaxy Dagger": "银河匕首", "Infinity Dagger": "无限匕首",
    "Insect Head": "昆虫头部", "Steel Smallsword": "钢制轻剑",
    "Cutlass": "短弯刀", "Claymore": "双刃大剑",
    "Templar's Blade": "圣殿骑士剑", "Obsidian Edge": "黑曜石之刃",
    "Bone Sword": "骨剑", "Galaxy Hammer": "银河锤",
    "Infinity Gavel": "无限之锤", "Wood Club": "木棒",
    "Iron Edge": "铁刃", "Lead Rod": "铅棒",
    "Slingshot": "弹弓", "Master Slingshot": "高级弹弓",
    "Galaxy Slingshot": "银河弹弓", "Femur": "股骨",
    "Ossified Blade": "骨化剑", "Yeti Tooth": "雪怪牙",
    "Forest Sword": "森林剑", "Tempered Broadsword": "回火宽刃剑",
    "Steel Falchion": "钢制弯刀", "Wicked Kris": "邪恶匕首",
    "Wind Spire": "风之利刃", "Dragontooth Cutlass": "龙牙弯刀",
    "Dragontooth Shiv": "龙牙匕首", "Dragontooth Club": "龙牙棒",
    "Ibis Hook": "鹮钩", "Rapier": "细剑",
    # === 帽子 ===
    "Cowboy Hat": "牛仔帽", "Bowler Hat": "圆顶礼帽",
    "Top Hat": "大礼帽", "Fedora": "软呢帽",
    "Cowgal Hat": "女牛仔帽", "Skeleton Mask": "骷髅面具",
    "Goggles": "护目镜", "Eye Mask": "眼罩",
    "Straw Hat": "草帽", "Sombrero": "宽边帽",
    "Hard Hat": "安全帽", "Hunter's Cap": "猎人帽",
    "Knight's Helmet": "骑士头盔", "Wizard Hat": "巫师帽",
    "Party Hat": "派对帽", "Santa Hat": "圣诞帽",
    "Trucker Hat": "卡车司机帽", "Propeller Hat": "螺旋桨帽",
    "Archer's Cap": "箭术帽", "Miner's Helmet": "矿工头盔",
    # === 鞋类 ===
    "Leather Boots": "皮靴", "Work Boots": "工作靴",
    "Combat Boots": "战斗靴", "Tundra Boots": "冻土靴",
    "Crystal Shoes": "水晶鞋", "Space Boots": "太空靴",
    "Firewalker Boots": "蹈火者靴", "Dragonscale Boots": "龙鳞靴",
    "Emily's Magic Boots": "艾米丽的魔法靴", "Genie Shoes": "精灵鞋",
    "Prismatic Shoes": "五彩靴", "Cinderclown Shoes": "煤渣小丑鞋",
    "Merman's Boots": "人鱼靴",
    # === 戒指 ===
    "Small Glow Ring": "小型辉光戒指", "Glow Ring": "辉光戒指",
    "Small Magnet Ring": "小型磁铁戒指", "Magnet Ring": "磁铁戒指",
    "Slime Charmer Ring": "史莱姆克星戒指", "Warrior Ring": "战士戒指",
    "Vampire Ring": "吸血戒指", "Ring of Yoba": "由巴之戒",
    "Sturdy Ring": "结实戒指", "Burglar's Ring": "窃贼戒指",
    "Iridium Band": "铱环", "Jade Ring": "翡翠戒指",
    "Amethyst Ring": "紫水晶戒指", "Topaz Ring": "黄水晶戒指",
    "Aquamarine Ring": "海蓝宝石戒指", "Ruby Ring": "红宝石戒指",
    "Emerald Ring": "绿宝石戒指", "Hot Java Ring": "热咖啡戒指",
    "Glowstone Ring": "发光石戒指", "Thorns Ring": "荆棘戒指",
    "Savage Ring": "野蛮戒指", "Immunity Band": "免疫环",
    "Napalm Ring": "凝固汽油弹戒指", "Phoenix Ring": "凤凰戒指",
    "Soul Sapper Ring": "吸魂戒指", "Ring of Forging": "锻造戒指",
    "Lucky Ring": "幸运戒指", "Ring of Fates": "命运戒指",
    # === 书 ===
    "Book of Stars": "星辰之书", "Queen of Sauce Cookbook": "酱料女皇食谱",
    "Woodskip": "木跃鱼", "Stardew Valley Almanac": "星露谷物语年鉴",
    # === 怪物战利品 ===
    "Bat Wing": "蝙蝠翅膀", "Bug Meat": "虫肉",
    "Solar Essence": "太阳精华", "Void Essence": "虚空精华",
    "Spider Eggs": "蜘蛛蛋", "Gooey Glob": "粘糊团",
    "Cursed Doll": "诅咒玩偶",
    # === 农场工具/肥料/种子 ===
    "Basic Fertilizer": "基础肥料", "Basic Retaining Soil": "基础保湿土壤",
    "Deluxe Fertilizer": "高级肥料", "Deluxe Retaining Soil": "高级保湿土壤",
    "Deluxe Speed-Gro": "高级生长激素", "Hyper Speed-Gro": "超速生长激素",
    "Quality Fertilizer": "优质肥料", "Quality Retaining Soil": "优质保湿土壤",
    "Speed-Gro": "生长激素", "Tree Fertilizer": "树肥",
    "Mixed Seeds": "混合种子", "Mixed Flower Seeds": "混合花卉种子",
    "Acorn": "橡子", "Maple Seed": "枫树种子", "Pine Cone": "松果",
    "Mahogany Seed": "桃花心木种子", "Mushroom Tree Seed": "蘑菇树种",
    "Mystic Tree Seed": "神秘树种", "Cactus Seeds": "仙人掌种子",
    "Fiber Seeds": "纤维种子", "Qi Bean": "齐豆",
    "Tea Sapling": "茶苗", "Mossy Seed": "苔藓种子",
    # === 资源 ===
    "Battery Pack": "电池组", "Cinder Shard": "煤渣碎片",
    "Clay": "粘土", "Hardwood": "硬木", "Stone": "石头",
    "Wood": "木材", "Fiber": "纤维", "Copper Ore": "铜矿石",
    "Copper Bar": "铜锭", "Gold Bar": "金锭", "Gold Ore": "金矿石",
    "Iridium Ore": "铱矿石", "Iridium Bar": "铱锭", "Iron Ore": "铁矿石",
    "Iron Bar": "铁锭", "Coal": "煤炭", "Refined Quartz": "精炼石英",
    "Radioactive Ore": "放射性矿石", "Radioactive Bar": "放射性锭",
    # === 垃圾 ===
    "Trash (item)": "垃圾", "Driftwood": "浮木",
    "Broken Glasses": "破损的眼镜", "Broken CD": "破损的CD",
    "Soggy Newspaper": "湿透的报纸", "Joja Cola": "Joja可乐",
    "Green Algae": "绿藻", "White Algae": "白藻", "Seaweed": "海草",
}

def get_zh_name(en_name):
    """获取标准中文名"""
    if en_name in EN_TO_ZH:
        return EN_TO_ZH[en_name]
    # 检查是否已有中文
    for ch in en_name:
        if ord(ch) > 0x4E00:
            return en_name
    return en_name

def is_chinese(s):
    for ch in s:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def fix_prices(data):
    """修复价格为0的物品"""
    fixed = 0
    for item in data:
        name_en = item.get('name_en', '')
        price = item.get('price', 0)
        if price == 0 and name_en in KNOWN_PRICES:
            item['price'] = KNOWN_PRICES[name_en]
            fixed += 1
        # Also try the name directly
        elif price == 0 and item['name'] in KNOWN_PRICES:
            item['price'] = KNOWN_PRICES[item['name']]
            fixed += 1
        # Also try with name_en if it matches an EN_TO_ZH key
        elif price == 0:
            for en_name, zh_name in EN_TO_ZH.items():
                if item['name'] == zh_name and en_name in KNOWN_PRICES:
                    item['price'] = KNOWN_PRICES[en_name]
                    fixed += 1
                    break
    return fixed

def calculate_quality_prices(base_price, has_quality):
    """计算品质价格"""
    if not has_quality or base_price <= 0:
        return {}
    return {
        "普通": base_price,
        "银星": int(base_price * 1.25),
        "金星": int(base_price * 1.5),
        "铱星": int(base_price * 2.0)
    }

def main():
    print("=" * 60)
    print("星露谷物品数据最终生成器 v3")
    print("=" * 60)
    
    # Load existing items_zh.json as base
    print("\n[Step 1] Loading items_zh.json...")
    data = load_json('items_zh.json')
    print(f"  Loaded {len(data)} items")
    
    # Check current categories
    cats = {}
    for item in data:
        c = item.get('category', '')
        cats[c] = cats.get(c, 0) + 1
    print("\n  Current categories:")
    for c in REQUESTED_CATEGORIES:
        print(f"    {c}: {cats.get(c, 0)}")
    for c in sorted(cats.keys()):
        if c not in REQUESTED_CATEGORIES:
            print(f"    {c} (其他): {cats[c]}")
    
    # [Step 2] Fix zero prices
    print("\n[Step 2] Fixing zero prices...")
    fixed = fix_prices(data)
    print(f"  Fixed {fixed} items with known prices")
    
    # [Step 3] Recategorize items
    print("\n[Step 3] Recategorizing items...")
    
    # Build lookup by English name for items that have name_en
    en_name_to_item = {}
    for item in data:
        en = item.get('name_en', '')
        if en:
            en_name_to_item[en] = item
    
    # Build lookup by name (Chinese name -> item)
    zh_name_to_item = {}
    for item in data:
        zh_name_to_item[item['name']] = item
    
    # Create items for missing categories
    # We'll organize items manually
    
    # Start with existing data, fix categories
    recategorized = {cat: [] for cat in REQUESTED_CATEGORIES}
    
    for item in data:
        cat = item.get('category', '')
        name_en = item.get('name_en', '')
        
        # Determine correct category
        # Tree fruits -> 果树
        tree_fruits = ["Apple", "Apricot", "Banana", "Cherry", "Mango", "Orange", "Peach", "Pomegranate"]
        if name_en in tree_fruits and cat != "果树":
            cat = "果树"
        
        # Forage items -> 季节采集物
        forage_items = [
            "Wild Horseradish", "Spice Berry", "Spring Onion", "Leek", "Dandelion",
            "Salmonberry", "Morel", "Common Mushroom", "Hazelnut", "Wild Plum",
            "Blackberry", "Chanterelle", "Red Mushroom", "Purple Mushroom", "Coconut",
            "Snow Yam", "Winter Root", "Crystal Fruit", "Holly", "Ginger", "Magma Cap",
            "Rainbow Shell", "Coral", "Nautilus Shell", "Sea Urchin",
            "Fossilized Leg", "Fossilized Ribs", "Fossilized Skull", "Fossilized Spine", "Fossilized Tail",
        ]
        if name_en in forage_items:
            cat = "季节采集物"
        
        # Seeds and fertilizer -> 农场工具
        tool_items = [
            "Basic Fertilizer", "Basic Retaining Soil", "Deluxe Fertilizer",
            "Deluxe Retaining Soil", "Deluxe Speed-Gro", "Hyper Speed-Gro",
            "Quality Fertilizer", "Quality Retaining Soil", "Speed-Gro", "Tree Fertilizer",
        ]
        if name_en in tool_items:
            cat = "农场工具"
        
        # Minerals -> 矿物
        mineral_items = [
            "Diamond", "Prismatic Shard", "Aquamarine", "Emerald", "Jade", "Ruby",
            "Amethyst", "Topaz", "Earth Crystal", "Frozen Tear", "Fire Quartz", "Quartz",
            "Aerinite", "Alamite", "Baryte", "Basalt", "Bixite", "Calcifur",
            "Celestine", "Cinnabar", "Dolomite", "Esperite", "Fairy Stone",
            "Fire Opal", "Fluorapatite", "Garnet", "Geminite", "Ghost Crystal",
            "Granite", "Hematite", "Honey Agate", "Jagoite", "Jasper", "Kyanite",
            "Lemon Stone", "Limestone", "Lunarite", "Malachite", "Marble", "Mudstone",
            "Neptunite", "Nekoite", "Obsidian", "Ocean Stone", "Opal", "Orpiment",
            "Petrified Slime", "Sandstone", "Slate", "Soapstone", "Star Shards",
            "Thunder Egg", "Tigerseye",
        ]
        if name_en in mineral_items:
            cat = "矿物"
        
        # Make sure category is in requested list
        if cat not in recategorized:
            # Try to map it
            if cat in CATEGORY_MAP:
                cat = CATEGORY_MAP[cat]
        
        if cat in recategorized:
            item['category'] = cat
            # Update has_quality
            item['has_quality'] = cat in QUALITY_CATEGORIES
            if item['has_quality'] and item['price'] > 0:
                item['qualities'] = calculate_quality_prices(item['price'], True)
            elif not item['has_quality']:
                item['qualities'] = {}
            recategorized[cat].append(item)
        else:
            # Put in "其他" - we'll keep as-is
            print(f"  Warning: {item['name']} has unmapped category '{cat}'")
            recategorized.setdefault("其他", []).append(item)
    
    # [Step 4] Build complete dataset
    print("\n[Step 4] Building complete dataset...")
    
    final_data = []
    item_id = 1
    
    for cat in REQUESTED_CATEGORIES:
        items = recategorized.get(cat, [])
        for item in items:
            item['id'] = item_id
            final_data.append(item)
            item_id += 1
    
    # Add any remaining items
    for cat in recategorized:
        if cat not in REQUESTED_CATEGORIES and cat != "其他":
            for item in recategorized[cat]:
                item['id'] = item_id
                final_data.append(item)
                item_id += 1
    if "其他" in recategorized:
        for item in recategorized["其他"]:
            item['id'] = item_id
            final_data.append(item)
            item_id += 1
    
    # Save
    output_path = os.path.join(BASE_DIR, 'items_zh_v3.json')
    save_json(output_path, final_data)
    print(f"\n[OK] Saved to items_zh_v3.json ({len(final_data)} items)")
    
    # Statistics
    print("\nCategory breakdown:")
    for cat in REQUESTED_CATEGORIES:
        count = sum(1 for i in final_data if i['category'] == cat)
        print(f"  {cat}: {count}")
    
    # Remaining issues
    zero_price = [i for i in final_data if i['price'] == 0]
    print(f"\nZero price items: {len(zero_price)}")
    if zero_price:
        for item in zero_price[:10]:
            print(f"  {item['name']} ({item.get('name_en', '')}) [{item['category']}]")
    
    no_category = [i for i in final_data if i['category'] not in REQUESTED_CATEGORIES]
    print(f"\nUncategorized items: {len(no_category)}")
    
    # Quality items
    quality_count = sum(1 for i in final_data if i['has_quality'])
    print(f"\nItems with quality: {quality_count}")
    
    return final_data

if __name__ == '__main__':
    main()