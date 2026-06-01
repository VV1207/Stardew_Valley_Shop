#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
星露谷物品数据重组脚本 - v2
- 重新分类到用户要求的19个类别
- 使用星露谷中文维基百科的标准翻译
- 为作物和采集物添加品质星级价格
- 修复价格显示问题
"""
import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(filename):
    with open(os.path.join(BASE_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    with open(os.path.join(BASE_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========== 星露谷中文维基百科标准翻译映射 ==========

# 原始数据中的分类 -> 用户要求的19个分类
CATEGORY_MAP = {
    "蔬菜": "作物",       # 蔬菜类归入作物
    "水果": "作物",       # 水果类归入作物
    "动物制品": "动物",   # 动物产品
    "果树": "果树",
    "工匠制品": "工匠制品",
    "家具": "家具",
    "墙纸": "墙纸",
    "地板": "地板",
    "矿物": "矿物",
    "古物": "古物",
    "渔具": "渔具",
    "武器": "武器",
    "帽子": "帽子",
    "鞋类": "鞋类",
    "戒指": "戒指",
    "烹饪": "菜品",
    "农场工具": "农场工具",
    "种子": "作物",       # 种子归入作物
    "肥料": "农场工具",   # 肥料归入农场工具
    "怪物战利品": "怪物战利品",
    "书": "书",
    "书": "书",
    "资源": "资源",       # 保留
    "垃圾": "垃圾",
}

# 需要品质星级的分类
QUALITY_CATEGORIES = ["作物", "季节采集物"]

# 标准中文翻译映射 (英文名 -> 中文维基标准名)
# 对于已存中文名称，保留原样；英文名称进行翻译
EN_TO_ZH_NAMES = {
    # === 蔬菜/作物 ===
    "Amaranth": "苋菜",
    "Artichoke": "洋蓟",
    "Beet": "甜菜",
    "Bok Choy": "大白菜",
    "Broccoli": "西兰花",
    "Carrot": "胡萝卜",
    "Cauliflower": "花椰菜",
    "Corn": "玉米",
    "Eggplant": "茄子",
    "Fiddlehead Fern": "蕨菜",
    "Garlic": "大蒜",
    "Green Bean": "绿豆",
    "Hops": "啤酒花",
    "Kale": "甘蓝菜",
    "Parsnip": "防风草",
    "Potato": "土豆",
    "Pumpkin": "南瓜",
    "Radish": "萝卜",
    "Red Cabbage": "红叶卷心菜",
    "Taro Root": "芋头",
    "Tea Leaves": "茶叶",
    "Tomato": "西红柿",
    "Unmilled Rice": "未碾米",
    "Wheat": "小麦",
    "Yam": "山药",
    "Summer Squash": "西葫芦",
    # === 水果 ===
    "Blueberry": "蓝莓",
    "Cactus Fruit": "仙人掌果子",
    "Cranberries": "蔓越莓",
    "Hot Pepper": "辣椒",
    "Melon": "甜瓜",
    "Starfruit": "杨桃",
    "Strawberry": "草莓",
    "Ancient Fruit": "上古水果",
    "Rhubarb": "大黄",
    "Blue Jazz": "蓝爵",
    "Sweet Gem Berry": "甜宝石",
    "Coffee Bean": "咖啡豆",
    "Fairy Rose": "玫瑰仙子",
    "Poppy": "虞美人花",
    "Summer Spangle": "夏季亮片",
    "Sunflower": "向日葵",
    "Tulip": "郁金香",
    "Powdermelon": "粉瓜",
    "Qi Fruit": "齐瓜",
    "Pineapple": "菠萝",
    # === 果树水果 ===
    "Apple": "苹果",
    "Apricot": "杏子",
    "Banana": "香蕉",
    "Cherry": "樱桃",
    "Mango": "芒果",
    "Orange": "橙子",
    "Peach": "桃子",
    "Pomegranate": "石榴",
    # === 采集物 ===
    "Wild Horseradish": "野山葵",
    "Spice Berry": "香料浆果",
    "Spring Onion": "大葱",
    "Leek": "韭菜",
    "Dandelion": "蒲公英",
    "Salmonberry": "美洲大树莓",
    "Morel": "羊肚菌",
    "Common Mushroom": "普通蘑菇",
    "Hazelnut": "榛子",
    "Wild Plum": "野梅",
    "Blackberry": "黑莓",
    "Chanterelle": "鸡油菌",
    "Red Mushroom": "红蘑菇",
    "Purple Mushroom": "紫蘑菇",
    "Coconut": "椰子",
    "Rainbow Shell": "彩虹贝壳",
    "Coral": "珊瑚",
    "Nautilus Shell": "鹦鹉螺",
    "Sea Urchin": "海胆",
    "Snow Yam": "雪山药",
    "Winter Root": "冬根",
    "Crystal Fruit": "水晶果",
    "Holly": "冬青树",
    "Ginger": "姜",
    "Magma Cap": "熔岩菇",
    "Sap": "树液",
    "Moss": "苔藓",
    "Fossilized Leg": "化石腿",
    "Fossilized Ribs": "化石肋骨",
    "Fossilized Skull": "化石头骨",
    "Fossilized Spine": "化石脊柱",
    "Fossilized Tail": "化石尾巴",
    # === 动物产品 ===
    "Brown Egg": "棕色鸡蛋",
    "White Egg": "白色鸡蛋",
    "Duck Egg": "鸭蛋",
    "Void Egg": "虚空蛋",
    "Golden Egg": "金蛋",
    "Large Brown Egg": "大棕色鸡蛋",
    "Large White Egg": "大白色鸡蛋",
    "Egg": "鸡蛋",
    "Large Egg": "大鸡蛋",
    "Milk": "牛奶",
    "Large Milk": "大壶牛奶",
    "Goat Milk": "羊奶",
    "Large Goat Milk": "大壶羊奶",
    "Ostrich Egg": "鸵鸟蛋",
    "Duck Feather": "鸭毛",
    "Rabbit's Foot": "兔子的脚",
    "Wool": "动物毛",
    "Slime": "史莱姆",
    "Slime Ball": "史莱姆球",
    "Truffle": "松露",
    # === 工匠制品 ===
    "Aged Roe": "陈酿鱼子酱",
    "Beer": "啤酒",
    "Caviar": "鱼子酱",
    "Cheese": "奶酪",
    "Cloth": "布料",
    "Coffee": "咖啡",
    "Dinosaur Mayonnaise": "恐龙蛋黄酱",
    "Dried Fruit": "水果干",
    "Dried Mushrooms": "蘑菇干",
    "Duck Mayonnaise": "鸭蛋黄酱",
    "Goat Cheese": "羊奶酪",
    "Green Tea": "绿茶",
    "Honey": "蜂蜜",
    "Juice": "果汁",
    "Maple Syrup": "枫糖浆",
    "Mayonnaise": "蛋黄酱",
    "Mead": "蜜蜂酒",
    "Mystic Syrup": "神秘糖浆",
    "Oak Resin": "橡树树脂",
    "Oil": "油",
    "Pale Ale": "淡啤酒",
    "Pine Tar": "松焦油",
    "Raisins": "葡萄干",
    "Roe": "鱼子",
    "Smoked Fish": "熏鱼",
    "Truffle Oil": "松露油",
    "Void Mayonnaise": "虚空蛋黄酱",
    "Wine": "果酒",
    # === 矿物 ===
    "Diamond": "钻石",
    "Prismatic Shard": "五彩碎片",
    "Aquamarine": "海蓝宝石",
    "Emerald": "绿宝石",
    "Jade": "翡翠",
    "Ruby": "红宝石",
    "Amethyst": "紫水晶",
    "Topaz": "黄水晶",
    "Earth Crystal": "地晶",
    "Frozen Tear": "泪晶",
    "Fire Quartz": "火石英",
    "Quartz": "石英",
    "Aerinite": "蓝纹石",
    "Alamite": "铝辉石",
    "Baryte": "重晶石",
    "Basalt": "玄武岩",
    "Bixite": "黑方石",
    "Calcifur": "氟磷灰石",
    "Celestine": "天青石",
    "Cinnabar": "辰砂",
    "Copper Ore": "铜矿石",
    "Copper Bar": "铜锭",
    "Dolomite": "白云石",
    "Esperite": "硅锌矿",
    "Fairy Stone": " Fairy Stone",
    "Fire Opal": "火蛋白石",
    "Fluorapatite": "氟磷灰石",
    "Garnet": "石榴石",
    "Geminite": "宝石",
    "Ghost Crystal": "幽灵水晶",
    "Gold Bar": "金锭",
    "Gold Ore": "金矿石",
    "Granite": "花岗岩",
    "Hematite": "赤铁矿",
    "Honey Agate": " Honey Agate",
    "Iridium Ore": "铱矿石",
    "Iridium Bar": "铱锭",
    "Iron Ore": "铁矿石",
    "Iron Bar": "铁锭",
    "Coal": "煤炭",
    "Jagoite": " Jagoite",
    "Jasper": "碧玉",
    "Kyanite": "蓝晶石",
    "Lemon Stone": " Lemon Stone",
    "Limestone": "石灰岩",
    "Lunarite": "月球石",
    "Malachite": "孔雀石",
    "Marble": "大理石",
    "Mudstone": "泥岩",
    "Neptunite": "硅钛钠石",
    "Nekoite": "针硅钙石",
    "Obsidian": "黑曜石",
    "Ocean Stone": "海洋石",
    "Opal": "蛋白石",
    "Orpiment": "雌黄",
    "Petrified Slime": "石化史莱姆",
    "Radioactive Ore": "放射性矿石",
    "Radioactive Bar": "放射性锭",
    "Refined Quartz": "精炼石英",
    "Sandstone": "砂岩",
    "Slate": "板岩",
    "Soapstone": "皂石",
    "Star Shards": "星碎",
    "Thunder Egg": "雷公蛋",
    "Tigerseye": "虎眼石",
    "Limestone": "石灰岩",
    # === 古物 ===
    "Ancient Doll": "古代玩偶",
    "Ancient Seed": "古代种子",
    "Arrowhead": "箭头",
    "Bone Flute": "骨笛",
    "Chicken Statue": "鸡雕像",
    "Chewing Stick": "咀嚼棒",
    "Dwarf Gadget": "矮人小工具",
    "Dwarvish Helm": "矮人头盔",
    "Dwarf Scroll I": "矮人卷轴 I",
    "Dwarf Scroll II": "矮人卷轴 II",
    "Dwarf Scroll III": "矮人卷轴 III",
    "Dwarf Scroll IV": "矮人卷轴 IV",
    "Elvish Jewelry": "精灵珠宝",
    "Glass Shards": "玻璃碎片",
    "Golden Mask": "黄金面具",
    "Golden Relic": "黄金遗物",
    "Ornamental Fan": "装饰扇子",
    "Prehistoric Rib": "史前肋骨",
    "Prehistoric Skull": "史前头骨",
    "Prehistoric Tool": "史前工具",
    "Rusty Spoon": "生锈的勺子",
    "Rusty Spur": "生锈的马刺",
    "Rusty Cog": "生锈的齿轮",
    "Rare Disc": "稀有圆盘",
    "Skeletal Hand": "骷髅手部",
    "Skeletal Tail": "骷髅尾部",
    "Amphibian Fossil": "两栖动物化石",
    "Palm Fossil": "棕榈化石",
    "Trilobite": "三叶虫",
    "Bone Fragment": "骨头碎片",
    "Dried Starfish": "干海星",
    "Large Animal Fossil": "大型动物化石",
    "Prehistoric Tibia": "史前胫骨",
    "Prehistoric Vertebra": "史前脊椎",
    "Snake Skull": "蛇头骨",
    "Snake Vertebrae": "蛇脊椎",
    "Strange Doll (green)": "诡异玩偶(绿)",
    "Strange Doll (yellow)": "诡异玩偶(黄)",
    "Ancient Drum": "古代鼓",
    "Ancient Sword": "古剑",
    "Anchor": "船锚",
    "Chipped Amphora": "碎双耳瓶",
    "Nautilus Fossil": "鹦鹉螺化石",
    "Prehistoric Handaxe": "史前手斧",
    "Prehistoric Scapula": "史前肩胛骨",
    # === 菜品 ===
    "Fried Egg": "煎鸡蛋",
    "Omelet": "欧姆蛋",
    "Salad": "沙拉",
    "Cheese Cauliflower": "乳酪花椰菜",
    "Baked Fish": "烤鱼",
    "Parsnip Soup": "防风草汤",
    "Vegetable Medley": "混合蔬菜",
    "Complete Breakfast": "完美早餐",
    "Fried Calamari": "炸鱿鱼",
    "Strange Bun": "奇怪的小面包",
    "Lucky Lunch": "幸运午餐",
    "Fried Mushroom": "炒蘑菇",
    "Pizza": "披萨",
    "Bean Hotpot": "豆类火锅",
    "Glazed Yams": "琉璃山药",
    "Carp Surprise": "惊奇鲤鱼",
    "Hashbrowns": "薯饼",
    "Pancakes": "薄煎饼",
    "Mango Sticky Rice": "芒果糯米饭",
    "Rhubarb Pie": "大黄派",
    "Cranberry Sauce": "蔓越莓酱",
    "Stuffing": "塞料面包",
    "Coleslaw": "卷心菜沙拉",
    "Autumn's Bounty": "秋日恩赐",
    "Bruschetta": "意式烤面包",
    "Chocolate Cake": "巧克力蛋糕",
    "Pumpkin Pie": "南瓜派",
    "Rabbit's Stew": "烩兔肉",
    "Fish Taco": "鱼肉卷",
    "Crispy Bass": "香酥鲈鱼",
    "Plum Pudding": "葡萄干布丁",
    "Chowder": "蛤蜊浓汤",
    "Trout Soup": "鳟鱼汤",
    "Ice Cream": "冰淇淋",
    "Crab Cakes": "蟹肉糕",
    "Bouillabaisse": "法式海鲜汤",
    "Algae Soup": "清汤",
    "Pale Broth": "清炖肉汤",
    "Pumpkin Soup": "南瓜汤",
    "Tom Kha Soup": "冬阴功汤",
    "Maple Bar": "枫糖棒",
    "Pink Cake": "粉红蛋糕",
    "Rice Pudding": "大米布丁",
    "Maki Roll": "生鱼寿司",
    "Sashimi": "生鱼片",
    "Tortilla": "墨西哥薄饼",
    "Triple Shot Espresso": "三倍浓缩咖啡",
    "Seafoam Pudding": "海泡布丁",
    "Dish O' The Sea": "海鲜杂烩",
    "Farmer's Lunch": "农夫午餐",
    "Survival Burger": "救生汉堡",
    "Pepper Poppers": "爆炒青椒",
    "Bread": "面包",
    "Cookie": "饼干",
    "Spaghetti": "意大利面",
    "Eggplant Parmesan": "帕尔玛茄子",
    "Stir Fry": "爆炒",
    "Blackberry Cobbler": "黑莓脆皮饼",
    "Cranberry Candy": "蔓越莓糖果",
    "Blueberry Tart": "蓝莓挞",
    "Fiddlehead Risotto": "蕨菜炖饭",
    "Salmon Dinner": "三文鱼晚餐",
    "Fish Stew": "鱼汤",
    "Red Plate": "红之盛宴",
    "Lobster Bisque": "龙虾浓汤",
    "Escargot": "蜗牛沙拉",
    "Mango Poppyseed Muffin": "芒果松饼",
    "Poppyseed Muffin": "松饼",
    "Tropical Curry": "热带咖喱",
    "Squid Ink Ravioli": "鱿鱼墨汁意饺",
    "Ginger Ale": "姜汁汽水",
    "Banana Pudding": "香蕉布丁",
    "Spicy Eel": "香辣鳗鱼",
    "Fried Eel": "炸鳗鱼",
    "Roasted Hazelnuts": "烤榛子",
    "Radish Salad": "萝卜沙拉",
    "Roots Platter": "块茎拼盘",
    "Shrimp Cocktail": "鲜虾开胃菜",
    "Super Meal": "超级餐",
    "Miner's Treat": "矿工小吃",
    "Moss Soup": "苔藓汤",
    "Poi": "芋泥",
    "Fruit Salad": "水果沙拉",
    "Artichoke Dip": "洋蓟蘸酱",
    "Fish Stew": "鱼汤",
    # === 渔具 ===
    "Barbed Hook": "倒刺钩",
    "Cork Bobber": "软木塞浮标",
    "Curiosity Lure": "好奇心鱼饵",
    "Dressed Spinner": "装饰旋转亮片",
    "Lead Bobber": "铅制浮标",
    "Quality Bobber": "优质浮标",
    "Sonar Bobber": "声纳浮标",
    "Spinner": "旋转亮片",
    "Trap Bobber": "陷阱浮标",
    "Treasure Hunter": "寻宝者",
    "Magnet": "磁铁",
    "Wild Bait": "野生鱼饵",
    "Bait": "鱼饵",
    "Challenge Bait": "挑战鱼饵",
    # === 武器 ===
    "Rusty Sword": "生锈的剑",
    "Silver Saber": "银剑",
    "Dark Sword": "黑暗之剑",
    "Crystal Sword": "水晶剑",
    "Holy Blade": "神圣之剑",
    "Lava Katana": "熔岩武士刀",
    "Galaxy Sword": "银河剑",
    "Infinity Blade": "无限之剑",
    "Wooden Blade": "木剑",
    "Iron Dirk": "铁短剑",
    "Burglar's Shank": "窃贼匕首",
    "Shadow Dagger": "暗影匕首",
    "Galaxy Dagger": "银河匕首",
    "Infinity Dagger": "无限匕首",
    "Insect Head": "昆虫头部",
    "Steel Smallsword": "钢制轻剑",
    "Cutlass": "短弯刀",
    "Claymore": "双刃大剑",
    "Templar's Blade": "圣殿骑士剑",
    "Obsidian Edge": "黑曜石之刃",
    "Bone Sword": "骨剑",
    "Galaxy Hammer": "银河锤",
    "Infinity Gavel": "无限之锤",
    "Wood Club": "木棒",
    "Iron Edge": "铁刃",
    "Lead Rod": "铅棒",
    "Slingshot": "弹弓",
    "Master Slingshot": "高级弹弓",
    "Galaxy Slingshot": "银河弹弓",
    "Femur": "股骨",
    "Ossified Blade": "骨化剑",
    "Yeti Tooth": "雪怪牙",
    # === 帽子 ===
    "Cowboy Hat": "牛仔帽",
    "Bowler Hat": "圆顶礼帽",
    "Top Hat": "大礼帽",
    "Fedora": "软呢帽",
    "Cowgal Hat": "女牛仔帽",
    "Skeleton Mask": "骷髅面具",
    "Goggles": "护目镜",
    "Eye Mask": "眼罩",
    "Straw Hat": "草帽",
    "Sombrero": "宽边帽",
    "Hard Hat": "安全帽",
    "Hunter's Cap": "猎人帽",
    "Knight's Helmet": "骑士头盔",
    "Wizard Hat": "巫师帽",
    "Party Hat": "派对帽",
    "Santa Hat": "圣诞帽",
    "Trucker Hat": "卡车司机帽",
    "Propeller Hat": "螺旋桨帽",
    "Archer's Cap": "箭术帽",
    "Miner's Helmet": "矿工头盔",
    # === 鞋类 ===
    "Leather Boots": "皮靴",
    "Work Boots": "工作靴",
    "Combat Boots": "战斗靴",
    "Tundra Boots": "冻土靴",
    "Crystal Shoes": "水晶鞋",
    "Space Boots": "太空靴",
    "Firewalker Boots": "蹈火者靴",
    "Dragonscale Boots": "龙鳞靴",
    "Emily's Magic Boots": "艾米丽的魔法靴",
    "Genie Shoes": "精灵鞋",
    "Prismatic Shoes": "五彩靴",
    # === 戒指 ===
    "Small Glow Ring": "小型辉光戒指",
    "Glow Ring": "辉光戒指",
    "Small Magnet Ring": "小型磁铁戒指",
    "Magnet Ring": "磁铁戒指",
    "Slime Charmer Ring": "史莱姆克星戒指",
    "Warrior Ring": "战士戒指",
    "Vampire Ring": "吸血戒指",
    "Yoba Ring": "由巴之戒",
    "Sturdy Ring": "结实戒指",
    "Burglar's Ring": "窃贼戒指",
    "Iridium Band": "铱环",
    "Jade Ring": "翡翠戒指",
    "Amethyst Ring": "紫水晶戒指",
    "Topaz Ring": "黄水晶戒指",
    "Aquamarine Ring": "海蓝宝石戒指",
    "Ruby Ring": "红宝石戒指",
    "Emerald Ring": "绿宝石戒指",
    "Hot Java Ring": "热咖啡戒指",
    "Glowstone Ring": "发光石戒指",
    "Thorns Ring": "荆棘戒指",
    "Ring of Yoba": "由巴之戒",
    "Sturdy Ring": "结实戒指",
    "Savage Ring": "野蛮戒指",
    "Immunity Band": "免疫环",
    "Napalm Ring": "凝固汽油弹戒指",
    "Phoenix Ring": "凤凰戒指",
    "Soul Sapper Ring": "吸魂戒指",
    "Ring of Forging": "锻造戒指",
    "Lucky Ring": "幸运戒指",
    "Ring of Fates": "命运戒指",
    # === 书 ===
    "Book of Stars": "星辰之书",
    "Queen of Sauce Cookbook": "酱料女皇食谱",
    "Woodskip": "木跃鱼",
    # === 武器 ===
    "Forest Sword": "森林剑",
    "Tempered Broadsword": "回火宽刃剑",
    "Steel Falchion": "钢制弯刀",
    "Wicked Kris": "邪恶匕首",
    "Wind Spire": "风之利刃",
    "Dragontooth Cutlass": "龙牙弯刀",
    "Dragontooth Shiv": "龙牙匕首",
    "Dragontooth Club": "龙牙棒",
    "Ibis Hook": "鹮钩",
    "Rapier": "细剑",
    # === 怪物战利品 ===
    "Bat Wing": "蝙蝠翅膀",
    "Bug Meat": "虫肉",
    "Solar Essence": "太阳精华",
    "Void Essence": "虚空精华",
    "Spider Eggs": "蜘蛛蛋",
    "Gooey Glob": "粘糊团",
    "Cursed Doll": "诅咒玩偶",
    # === 农场工具 ===
    "Basic Fertilizer": "基础肥料",
    "Basic Retaining Soil": "基础保湿土壤",
    "Deluxe Fertilizer": "高级肥料",
    "Deluxe Retaining Soil": "高级保湿土壤",
    "Deluxe Speed-Gro": "高级生长激素",
    "Hyper Speed-Gro": "超速生长激素",
    "Quality Fertilizer": "优质肥料",
    "Quality Retaining Soil": "优质保湿土壤",
    "Speed-Gro": "生长激素",
    "Tree Fertilizer": "树肥",
    # === 种子 ===
    "Mixed Seeds": "混合种子",
    "Mixed Flower Seeds": "混合花卉种子",
    "Oak Resin": "橡树树脂",
    "Pine Tar": "松焦油",
    "Maple Syrup": "枫糖浆",
    "Sap": "树液",
    "Acorn": "橡子",
    "Maple Seed": "枫树种子",
    "Pine Cone": "松果",
    "Mahogany Seed": "桃花心木种子",
    "Mushroom Tree Seed": "蘑菇树种",
    "Mystic Tree Seed": "神秘树种",
    "Cactus Seeds": "仙人掌种子",
    "Fiber Seeds": "纤维种子",
    "Qi Bean": "齐豆",
    "Tea Sapling": "茶苗",
    "Mossy Seed": "苔藓种子",
    # === 资源 ===
    "Battery Pack": "电池组",
    "Bone Fragment": "骨头碎片",
    "Cinder Shard": "煤渣碎片",
    "Clay": "粘土",
    "Hardwood": "硬木",
    "Stone": "石头",
    "Wood": "木材",
    "Fiber": "纤维",
    # === 怪物战利品 ===
    "Bat Wing": "蝙蝠翅膀",
    "Bug Meat": "虫肉",
    "Solar Essence": "太阳精华",
    "Void Essence": "虚空精华",
    "Cursed Doll": "诅咒玩偶",
    "Gooey Glob": "粘糊团",
    "Spider Eggs": "蜘蛛蛋",
}

def get_zh_name(name):
    """Get Chinese name for an item, or return the English name if not found"""
    if name in EN_TO_ZH_NAMES:
        return EN_TO_ZH_NAMES[name]
    # Check if it already looks Chinese (has any CJK characters)
    import unicodedata
    for ch in name:
        if 'CJK' in unicodedata.name(ch, ''):
            return name
    return name

def is_chinese_string(s):
    """Check if a string contains Chinese characters"""
    import unicodedata
    for ch in s:
        cat = unicodedata.category(ch)
        if cat.startswith('Lo'):  # Other_Letter (CJK ideographs)
            return True
    return False

def reorganize_data():
    print("Loading items_gift.json...")
    data = load_json('items_gift.json')
    print(f"  Found {len(data)} items")
    
    # Verify the categories in the data
    orig_cats = sorted(set(i.get('category', '') for i in data))
    print(f"  Original categories: {orig_cats}")
    
    # Map all items to new categories
    new_items = []
    
    for item in data:
        name = item['name']
        orig_cat = item.get('category', '')
        price = item.get('price', 0)
        
        # Map category
        if orig_cat in CATEGORY_MAP:
            new_cat = CATEGORY_MAP[orig_cat]
        else:
            new_cat = orig_cat  # Keep as-is if not mapped
        
        # Get Chinese name
        zh_name = get_zh_name(name)
        
        # Determine if this category has quality
        has_quality = new_cat in QUALITY_CATEGORIES
        
        # Calculate quality prices (星露谷官方规则)
        # 普通: 基本价格
        # 银星: ×1.25
        # 金星: ×1.50
        # 铱星: ×2.00
        quality_prices = {}
        if has_quality and price > 0:
            quality_prices = {
                "普通": price,
                "银星": int(price * 1.25),
                "金星": int(price * 1.5),
                "铱星": int(price * 2.0)
            }
        
        # Build new item
        new_item = {
            "id": item['id'],
            "name": zh_name,
            "name_en": name if zh_name != name else "",
            "category": new_cat,
            "category_orig": orig_cat,
            "price": price if price > 0 else 0,
            "has_quality": has_quality,
            "qualities": quality_prices,
            "image": item.get('image', ''),
            "source": item.get('source', ''),
            "description": item.get('description', ''),
            "ingredients": item.get('ingredients', ''),
            "gifting": item.get('gifting', {"love":[], "like":[], "neutral":[], "dislike":[], "hate":[]})
        }
        new_items.append(new_item)
    
    # 19 requested categories
    requested_categories = [
        "作物", "动物", "果树", "工匠制品", "家具", "墙纸", "地板",
        "矿物", "渔具", "武器", "帽子", "鞋类", "戒指", "菜品",
        "农场工具", "古物", "怪物战利品", "书", "季节采集物"
    ]
    
    # Categorize items
    categorized = {cat: [] for cat in requested_categories}
    other_items = []
    
    for item in new_items:
        cat = item['category']
        if cat in categorized:
            categorized[cat].append(item)
        else:
            other_items.append(item)
    
    # Build final output in requested category order
    final_data = []
    item_id = 1
    
    for cat_name in requested_categories:
        items = categorized[cat_name]
        for item in items:
            item['id'] = item_id
            final_data.append(item)
            item_id += 1
    
    # Add remaining items
    for item in other_items:
        item['id'] = item_id
        final_data.append(item)
        item_id += 1
    
    # Save
    output_path = os.path.join(BASE_DIR, 'items_zh.json')
    save_json(output_path, final_data)
    print(f"\nSaved items_zh.json with {len(final_data)} items")
    
    # Print stats
    stats = {}
    for item in final_data:
        cat = item['category']
        stats[cat] = stats.get(cat, 0) + 1
    
    print("\nCategory breakdown:")
    for cat in requested_categories:
        if cat in stats:
            print(f"  {cat}: {stats[cat]}")
    
    for cat in stats:
        if cat not in requested_categories:
            print(f"  {cat} (未分类): {stats[cat]}")
    
    # Zero price items
    zero_price = [i for i in final_data if i['price'] == 0]
    print(f"\nZero price items: {len(zero_price)}")
    
    return final_data

if __name__ == '__main__':
    reorganize_data()