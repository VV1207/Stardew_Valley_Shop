#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
星露谷完整物品数据重建 - 修正所有问题
"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))

def save_json(filename, data):
    with open(os.path.join(BASE, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

CATEGORIES = [
    "作物", "动物", "果树", "工匠制品", "家具", "墙纸", "地板",
    "矿物", "渔具", "武器", "帽子", "鞋类", "戒指", "菜品",
    "农场工具", "古物", "怪物战利品", "书", "季节采集物"
]

def find_image(name_en, name_zh):
    """Find the best matching image in the images folder"""
    images_dir = os.path.join(BASE, 'images')
    if not os.path.isdir(images_dir):
        return ""
    existing = os.listdir(images_dir)
    existing_lower = {f.lower(): f for f in existing}
    
    # Generate candidate filenames
    clean_en = name_en.replace(' ', '_').replace("'", '').replace('(', '').replace(')', '')
    
    # Build candidate filenames
    uc = name_en.replace(' ', '_')
    uc2 = name_en.replace(' ', '_').replace("'", '_').replace('(', '').replace(')', '')
    candidates = []
    for base in [uc, uc2]:
        candidates.append(f"{base}.png")
        candidates.append(f"24px-{base}.png")
    
    # Remove duplicates while preserving order
    seen = set()
    candidates_nodup = []
    for c in candidates:
        cl = c.lower()
        if cl not in seen:
            seen.add(cl)
            candidates_nodup.append(c)
    
    for c in candidates_nodup:
        cl = c.lower()
        if cl in existing_lower:
            return f"images/{existing_lower[cl]}"
    
    # Broader search: try matching any image that contains the name_en
    base_parts = name_en.lower().replace(' ', '_').replace("'", '_').replace('(', '_').replace(')', '_').split('_')
    for ef in existing:
        ef_lower = ef.lower().replace('.png', '')
        # Check if all significant parts match
        matches = sum(1 for part in base_parts if part and len(part) > 2 and part in ef_lower)
        if matches >= len([p for p in base_parts if len(p) > 2]):
            return f"images/{ef}"
    
    return ""

# ALL_ITEMS: (name_en, name_zh, category, base_price, has_quality)
ALL_ITEMS = [
    # ===== 作物 =====
    ("Amaranth", "苋菜", "作物", 150, True),
    ("Artichoke", "洋蓟", "作物", 160, True),
    ("Beet", "甜菜", "作物", 100, True),
    ("Bok Choy", "大白菜", "作物", 80, True),
    ("Broccoli", "西兰花", "作物", 70, True),
    ("Carrot", "胡萝卜", "作物", 60, True),
    ("Cauliflower", "花椰菜", "作物", 175, True),
    ("Corn", "玉米", "作物", 50, True),
    ("Eggplant", "茄子", "作物", 60, True),
    ("Fiddlehead Fern", "蕨菜", "作物", 90, True),
    ("Garlic", "大蒜", "作物", 60, True),
    ("Green Bean", "绿豆", "作物", 40, True),
    ("Hops", "啤酒花", "作物", 25, True),
    ("Kale", "甘蓝菜", "作物", 110, True),
    ("Parsnip", "防风草", "作物", 35, True),
    ("Potato", "土豆", "作物", 80, True),
    ("Pumpkin", "南瓜", "作物", 320, True),
    ("Radish", "萝卜", "作物", 90, True),
    ("Red Cabbage", "红叶卷心菜", "作物", 260, True),
    ("Taro Root", "芋头", "作物", 100, True),
    ("Tea Leaves", "茶叶", "作物", 50, True),
    ("Tomato", "西红柿", "作物", 60, True),
    ("Unmilled Rice", "未碾米", "作物", 30, True),
    ("Wheat", "小麦", "作物", 25, True),
    ("Yam", "山药", "作物", 160, True),
    ("Summer Squash", "西葫芦", "作物", 45, True),
    ("Blueberry", "蓝莓", "作物", 50, True),
    ("Cactus Fruit", "仙人掌果子", "作物", 75, True),
    ("Cranberries", "蔓越莓", "作物", 75, True),
    ("Hot Pepper", "辣椒", "作物", 40, True),
    ("Melon", "甜瓜", "作物", 250, True),
    ("Starfruit", "杨桃", "作物", 750, True),
    ("Strawberry", "草莓", "作物", 120, True),
    ("Ancient Fruit", "上古水果", "作物", 550, True),
    ("Rhubarb", "大黄", "作物", 220, True),
    ("Sweet Gem Berry", "甜宝石", "作物", 3000, True),
    ("Powdermelon", "粉瓜", "作物", 180, True),
    ("Qi Fruit", "齐瓜", "作物", 1, True),
    ("Pineapple", "菠萝", "作物", 300, True),
    ("Blue Jazz", "蓝爵", "作物", 50, True),
    ("Fairy Rose", "玫瑰仙子", "作物", 290, True),
    ("Poppy", "虞美人花", "作物", 140, True),
    ("Summer Spangle", "夏季亮片", "作物", 90, True),
    ("Sunflower", "向日葵", "作物", 80, True),
    ("Tulip", "郁金香", "作物", 30, True),
    ("Coffee Bean", "咖啡豆", "作物", 15, False),
    
    # ===== 动物 =====
    ("Brown Egg", "棕色鸡蛋", "动物", 50, False),
    ("White Egg", "白色鸡蛋", "动物", 50, False),
    ("Duck Egg", "鸭蛋", "动物", 80, False),
    ("Void Egg", "虚空蛋", "动物", 300, False),
    ("Golden Egg", "金蛋", "动物", 2000, False),
    ("Large Brown Egg", "大棕色鸡蛋", "动物", 75, False),
    ("Large White Egg", "大白色鸡蛋", "动物", 75, False),
    ("Egg", "鸡蛋", "动物", 50, False),
    ("Large Egg", "大鸡蛋", "动物", 75, False),
    ("Milk", "牛奶", "动物", 125, False),
    ("Large Milk", "大壶牛奶", "动物", 175, False),
    ("Goat Milk", "羊奶", "动物", 225, False),
    ("Large Goat Milk", "大壶羊奶", "动物", 300, False),
    ("Ostrich Egg", "鸵鸟蛋", "动物", 600, False),
    ("Duck Feather", "鸭毛", "动物", 250, False),
    ("Rabbit's Foot", "兔子的脚", "动物", 565, False),
    ("Wool", "动物毛", "动物", 340, False),
    ("Truffle", "松露", "动物", 625, False),
    
    # ===== 果树 =====
    ("Apple", "苹果", "果树", 100, False),
    ("Apricot", "杏子", "果树", 50, False),
    ("Banana", "香蕉", "果树", 150, False),
    ("Cherry", "樱桃", "果树", 80, False),
    ("Mango", "芒果", "果树", 130, False),
    ("Orange", "橙子", "果树", 100, False),
    ("Peach", "桃子", "果树", 140, False),
    ("Pomegranate", "石榴", "果树", 140, False),
    
    # ===== 工匠制品 =====
    ("Aged Roe", "陈酿鱼子酱", "工匠制品", 400, False),
    ("Beer", "啤酒", "工匠制品", 200, False),
    ("Caviar", "鱼子酱", "工匠制品", 500, False),
    ("Cheese", "奶酪", "工匠制品", 230, False),
    ("Cloth", "布料", "工匠制品", 470, False),
    ("Coffee", "咖啡", "工匠制品", 150, False),
    ("Dinosaur Mayonnaise", "恐龙蛋黄酱", "工匠制品", 800, False),
    ("Dried Fruit", "水果干", "工匠制品", 100, False),
    ("Dried Mushrooms", "蘑菇干", "工匠制品", 100, False),
    ("Duck Mayonnaise", "鸭蛋黄酱", "工匠制品", 375, False),
    ("Goat Cheese", "羊奶酪", "工匠制品", 375, False),
    ("Green Tea", "绿茶", "工匠制品", 100, False),
    ("Honey", "蜂蜜", "工匠制品", 100, False),
    ("Juice", "果汁", "工匠制品", 75, False),
    ("Maple Syrup", "枫糖浆", "工匠制品", 200, False),
    ("Mayonnaise", "蛋黄酱", "工匠制品", 190, False),
    ("Mead", "蜜蜂酒", "工匠制品", 300, False),
    ("Mystic Syrup", "神秘糖浆", "工匠制品", 4000, False),
    ("Oak Resin", "橡树树脂", "工匠制品", 150, False),
    ("Oil", "油", "工匠制品", 100, False),
    ("Pale Ale", "淡啤酒", "工匠制品", 300, False),
    ("Pine Tar", "松焦油", "工匠制品", 100, False),
    ("Raisins", "葡萄干", "工匠制品", 600, False),
    ("Roe", "鱼子", "工匠制品", 100, False),
    ("Smoked Fish", "熏鱼", "工匠制品", 100, False),
    ("Truffle Oil", "松露油", "工匠制品", 1065, False),
    ("Void Mayonnaise", "虚空蛋黄酱", "工匠制品", 275, False),
    ("Wine", "果酒", "工匠制品", 400, False),
    
    # ===== 家具 =====
    ("Chest", "箱子", "家具", 150, False),
    ("Stone Chest", "石箱", "家具", 350, False),
    ("Bed", "床", "家具", 2000, False),
    ("Chair", "椅子", "家具", 200, False),
    ("Table", "桌子", "家具", 350, False),
    ("Lamp", "灯", "家具", 200, False),
    ("Rug", "地毯", "家具", 200, False),
    ("TV", "电视机", "家具", 750, False),
    ("Stove", "炉灶", "家具", 2000, False),
    ("Refrigerator", "冰箱", "家具", 3000, False),
    ("Sofa", "沙发", "家具", 1000, False),
    ("Dresser", "梳妆台", "家具", 2000, False),
    ("Bookshelf", "书架", "家具", 800, False),
    ("End Table", "茶几", "家具", 250, False),
    ("Potted Plant", "盆栽", "家具", 200, False),
    ("Window", "窗户", "家具", 300, False),
    ("Wall Decoration", "墙饰", "家具", 150, False),
    ("Fish Tank", "鱼缸", "家具", 2000, False),
    ("Candle", "蜡烛", "家具", 50, False),
    
    # ===== 墙纸 =====
    ("Wallpaper (Plain)", "素色墙纸", "墙纸", 100, False),
    ("Wallpaper (Floral)", "碎花墙纸", "墙纸", 100, False),
    ("Wallpaper (Striped)", "条纹墙纸", "墙纸", 100, False),
    ("Wallpaper (Plaid)", "格子墙纸", "墙纸", 100, False),
    ("Wallpaper (Brick)", "砖纹墙纸", "墙纸", 100, False),
    
    # ===== 地板 =====
    ("Wood Floor", "木地板", "地板", 100, False),
    ("Stone Floor", "石地板", "地板", 100, False),
    ("Crystal Floor", "水晶地板", "地板", 100, False),
    ("Brick Floor", "砖地板", "地板", 100, False),
    ("Path", "小路", "地板", 100, False),
    ("Cobblestone Path", "卵石路", "地板", 100, False),
    ("Stepping Stone Path", "踏石路", "地板", 100, False),
    
    # ===== 矿物 =====
    ("Diamond", "钻石", "矿物", 750, False),
    ("Prismatic Shard", "五彩碎片", "矿物", 2000, False),
    ("Aquamarine", "海蓝宝石", "矿物", 180, False),
    ("Emerald", "绿宝石", "矿物", 250, False),
    ("Jade", "翡翠", "矿物", 200, False),
    ("Ruby", "红宝石", "矿物", 300, False),
    ("Amethyst", "紫水晶", "矿物", 100, False),
    ("Topaz", "黄水晶", "矿物", 120, False),
    ("Earth Crystal", "地晶", "矿物", 200, False),
    ("Frozen Tear", "泪晶", "矿物", 200, False),
    ("Fire Quartz", "火石英", "矿物", 120, False),
    ("Quartz", "石英", "矿物", 50, False),
    
    # ===== 渔具 =====
    ("Barbed Hook", "倒刺钩", "渔具", 500, False),
    ("Cork Bobber", "软木塞浮标", "渔具", 750, False),
    ("Curiosity Lure", "好奇心鱼饵", "渔具", 500, False),
    ("Dressed Spinner", "装饰旋转亮片", "渔具", 500, False),
    ("Lead Bobber", "铅制浮标", "渔具", 200, False),
    ("Quality Bobber", "优质浮标", "渔具", 750, False),
    ("Sonar Bobber", "声纳浮标", "渔具", 300, False),
    ("Spinner", "旋转亮片", "渔具", 250, False),
    ("Trap Bobber", "陷阱浮标", "渔具", 400, False),
    ("Treasure Hunter", "寻宝者", "渔具", 400, False),
    ("Magnet", "磁铁", "渔具", 1000, False),
    ("Wild Bait", "野生鱼饵", "渔具", 5, False),
    ("Bait", "鱼饵", "渔具", 5, False),
    ("Challenge Bait", "挑战鱼饵", "渔具", 5, False),
    
    # ===== 武器 =====
    ("Rusty Sword", "生锈的剑", "武器", 100, False),
    ("Silver Saber", "银剑", "武器", 750, False),
    ("Dark Sword", "黑暗之剑", "武器", 800, False),
    ("Galaxy Sword", "银河剑", "武器", 5000, False),
    ("Lava Katana", "熔岩武士刀", "武器", 2500, False),
    ("Bone Sword", "骨剑", "武器", 600, False),
    ("Galaxy Hammer", "银河锤", "武器", 3500, False),
    ("Galaxy Dagger", "银河匕首", "武器", 3500, False),
    ("Obsidian Edge", "黑曜石之刃", "武器", 1200, False),
    ("Claymore", "双刃大剑", "武器", 700, False),
    ("Templar's Blade", "圣殿骑士剑", "武器", 1500, False),
    ("Steel Falchion", "钢制弯刀", "武器", 2000, False),
    ("Wicked Kris", "邪恶匕首", "武器", 800, False),
    ("Forest Sword", "森林剑", "武器", 900, False),
    ("Wooden Blade", "木剑", "武器", 50, False),
    ("Slingshot", "弹弓", "武器", 500, False),
    ("Master Slingshot", "高级弹弓", "武器", 1000, False),
    ("Galaxy Slingshot", "银河弹弓", "武器", 5000, False),
    
    # ===== 帽子 =====
    ("Cowboy Hat", "牛仔帽", "帽子", 2000, False),
    ("Straw Hat", "草帽", "帽子", 2000, False),
    ("Top Hat", "大礼帽", "帽子", 4000, False),
    ("Wizard Hat", "巫师帽", "帽子", 4000, False),
    ("Fedora", "软呢帽", "帽子", 3000, False),
    ("Hard Hat", "安全帽", "帽子", 4000, False),
    ("Hunter's Cap", "猎人帽", "帽子", 1500, False),
    ("Knight's Helmet", "骑士头盔", "帽子", 4000, False),
    ("Santa Hat", "圣诞帽", "帽子", 4000, False),
    ("Miner's Helmet", "矿工头盔", "帽子", 1500, False),
    ("Skeleton Mask", "骷髅面具", "帽子", 3000, False),
    
    # ===== 鞋类 =====
    ("Leather Boots", "皮靴", "鞋类", 500, False),
    ("Work Boots", "工作靴", "鞋类", 500, False),
    ("Combat Boots", "战斗靴", "鞋类", 750, False),
    ("Tundra Boots", "冻土靴", "鞋类", 1000, False),
    ("Crystal Shoes", "水晶鞋", "鞋类", 1250, False),
    ("Space Boots", "太空靴", "鞋类", 1250, False),
    ("Firewalker Boots", "蹈火者靴", "鞋类", 1500, False),
    ("Dragonscale Boots", "龙鳞靴", "鞋类", 2000, False),
    ("Emily's Magic Boots", "艾米丽的魔法靴", "鞋类", 2500, False),
    ("Prismatic Shoes", "五彩靴", "鞋类", 3000, False),
    
    # ===== 戒指 =====
    ("Small Glow Ring", "小型辉光戒指", "戒指", 100, False),
    ("Glow Ring", "辉光戒指", "戒指", 250, False),
    ("Small Magnet Ring", "小型磁铁戒指", "戒指", 100, False),
    ("Magnet Ring", "磁铁戒指", "戒指", 250, False),
    ("Slime Charmer Ring", "史莱姆克星戒指", "戒指", 1500, False),
    ("Warrior Ring", "战士戒指", "戒指", 1000, False),
    ("Vampire Ring", "吸血戒指", "戒指", 1500, False),
    ("Iridium Band", "铱环", "戒指", 5000, False),
    ("Burglar's Ring", "窃贼戒指", "戒指", 1000, False),
    ("Lucky Ring", "幸运戒指", "戒指", 7500, False),
    ("Napalm Ring", "凝固汽油弹戒指", "戒指", 5000, False),
    ("Phoenix Ring", "凤凰戒指", "戒指", 5000, False),
    ("Hot Java Ring", "热咖啡戒指", "戒指", 2500, False),
    ("Glowstone Ring", "发光石戒指", "戒指", 2000, False),
    ("Ring of Yoba", "由巴之戒", "戒指", 1500, False),
    ("Savage Ring", "野蛮戒指", "戒指", 1500, False),
    ("Sturdy Ring", "结实戒指", "戒指", 1500, False),
    ("Thorns Ring", "荆棘戒指", "戒指", 1500, False),
    
    # ===== 菜品 =====
    ("Fried Egg", "煎鸡蛋", "菜品", 35, False),
    ("Omelet", "欧姆蛋", "菜品", 125, False),
    ("Salad", "沙拉", "菜品", 110, False),
    ("Cheese Cauliflower", "乳酪花椰菜", "菜品", 300, False),
    ("Baked Fish", "烤鱼", "菜品", 100, False),
    ("Parsnip Soup", "防风草汤", "菜品", 85, False),
    ("Vegetable Medley", "混合蔬菜", "菜品", 120, False),
    ("Complete Breakfast", "完美早餐", "菜品", 350, False),
    ("Fried Calamari", "炸鱿鱼", "菜品", 150, False),
    ("Strange Bun", "奇怪的小面包", "菜品", 75, False),
    ("Lucky Lunch", "幸运午餐", "菜品", 250, False),
    ("Fried Mushroom", "炒蘑菇", "菜品", 200, False),
    ("Pizza", "披萨", "菜品", 300, False),
    ("Bean Hotpot", "豆类火锅", "菜品", 100, False),
    ("Glazed Yams", "琉璃山药", "菜品", 200, False),
    ("Carp Surprise", "惊奇鲤鱼", "菜品", 150, False),
    ("Hashbrowns", "薯饼", "菜品", 120, False),
    ("Pancakes", "薄煎饼", "菜品", 80, False),
    ("Rhubarb Pie", "大黄派", "菜品", 400, False),
    ("Cranberry Sauce", "蔓越莓酱", "菜品", 120, False),
    ("Stuffing", "塞料面包", "菜品", 165, False),
    ("Coleslaw", "卷心菜沙拉", "菜品", 200, False),
    ("Autumn's Bounty", "秋日恩赐", "菜品", 350, False),
    ("Chocolate Cake", "巧克力蛋糕", "菜品", 200, False),
    ("Pumpkin Pie", "南瓜派", "菜品", 385, False),
    ("Fish Taco", "鱼肉卷", "菜品", 500, False),
    ("Crispy Bass", "香酥鲈鱼", "菜品", 150, False),
    ("Chowder", "蛤蜊浓汤", "菜品", 135, False),
    ("Ice Cream", "冰淇淋", "菜品", 120, False),
    ("Crab Cakes", "蟹肉糕", "菜品", 250, False),
    ("Algae Soup", "清汤", "菜品", 100, False),
    ("Pumpkin Soup", "南瓜汤", "菜品", 250, False),
    ("Tom Kha Soup", "冬阴功汤", "菜品", 250, False),
    ("Maki Roll", "生鱼寿司", "菜品", 220, False),
    ("Sashimi", "生鱼片", "菜品", 75, False),
    ("Tortilla", "墨西哥薄饼", "菜品", 50, False),
    ("Triple Shot Espresso", "三倍浓缩咖啡", "菜品", 450, False),
    ("Seafoam Pudding", "海泡布丁", "菜品", 300, False),
    ("Bread", "面包", "菜品", 60, False),
    ("Cookie", "饼干", "菜品", 140, False),
    ("Spaghetti", "意大利面", "菜品", 120, False),
    ("Eggplant Parmesan", "帕尔玛茄子", "菜品", 200, False),
    ("Stir Fry", "爆炒", "菜品", 200, False),
    ("Blueberry Tart", "蓝莓挞", "菜品", 150, False),
    ("Salmon Dinner", "三文鱼晚餐", "菜品", 300, False),
    ("Lobster Bisque", "龙虾浓汤", "菜品", 500, False),
    ("Escargot", "蜗牛沙拉", "菜品", 175, False),
    ("Spicy Eel", "香辣鳗鱼", "菜品", 175, False),
    ("Super Meal", "超级餐", "菜品", 450, False),
    ("Miner's Treat", "矿工小吃", "菜品", 200, False),
    
    # ===== 农场工具 =====
    ("Basic Fertilizer", "基础肥料", "农场工具", 10, False),
    ("Basic Retaining Soil", "基础保湿土壤", "农场工具", 10, False),
    ("Deluxe Fertilizer", "高级肥料", "农场工具", 40, False),
    ("Deluxe Retaining Soil", "高级保湿土壤", "农场工具", 20, False),
    ("Deluxe Speed-Gro", "高级生长激素", "农场工具", 80, False),
    ("Hyper Speed-Gro", "超速生长激素", "农场工具", 100, False),
    ("Quality Fertilizer", "优质肥料", "农场工具", 20, False),
    ("Quality Retaining Soil", "优质保湿土壤", "农场工具", 10, False),
    ("Speed-Gro", "生长激素", "农场工具", 20, False),
    ("Tree Fertilizer", "树肥", "农场工具", 25, False),
    ("Mixed Seeds", "混合种子", "农场工具", 20, False),
    ("Mixed Flower Seeds", "混合花卉种子", "农场工具", 30, False),
    ("Acorn", "橡子", "农场工具", 20, False),
    ("Maple Seed", "枫树种子", "农场工具", 20, False),
    ("Pine Cone", "松果", "农场工具", 20, False),
    ("Mahogany Seed", "桃花心木种子", "农场工具", 50, False),
    ("Tea Sapling", "茶苗", "农场工具", 500, False),
    ("Cactus Seeds", "仙人掌种子", "农场工具", 150, False),
    ("Fiber Seeds", "纤维种子", "农场工具", 25, False),
    
    # ===== 古物 =====
    ("Ancient Doll", "古代玩偶", "古物", 250, False),
    ("Ancient Seed", "古代种子", "古物", 0, False),
    ("Arrowhead", "箭头", "古物", 100, False),
    ("Bone Flute", "骨笛", "古物", 200, False),
    ("Chicken Statue", "鸡雕像", "古物", 200, False),
    ("Chewing Stick", "咀嚼棒", "古物", 100, False),
    ("Dwarf Gadget", "矮人小工具", "古物", 200, False),
    ("Dwarvish Helm", "矮人头盔", "古物", 200, False),
    ("Dwarf Scroll I", "矮人卷轴 I", "古物", 10, False),
    ("Dwarf Scroll II", "矮人卷轴 II", "古物", 10, False),
    ("Dwarf Scroll III", "矮人卷轴 III", "古物", 10, False),
    ("Dwarf Scroll IV", "矮人卷轴 IV", "古物", 10, False),
    ("Elvish Jewelry", "精灵珠宝", "古物", 300, False),
    ("Glass Shards", "玻璃碎片", "古物", 10, False),
    ("Golden Mask", "黄金面具", "古物", 500, False),
    ("Golden Relic", "黄金遗物", "古物", 500, False),
    ("Ornamental Fan", "装饰扇子", "古物", 300, False),
    ("Rusty Spoon", "生锈的勺子", "古物", 50, False),
    ("Rusty Spur", "生锈的马刺", "古物", 50, False),
    ("Rusty Cog", "生锈的齿轮", "古物", 50, False),
    ("Rare Disc", "稀有圆盘", "古物", 300, False),
    ("Skeletal Hand", "骷髅手部", "古物", 100, False),
    ("Skeletal Tail", "骷髅尾部", "古物", 100, False),
    ("Amphibian Fossil", "两栖动物化石", "古物", 100, False),
    ("Palm Fossil", "棕榈化石", "古物", 100, False),
    ("Trilobite", "三叶虫", "古物", 150, False),
    ("Dried Starfish", "干海星", "古物", 50, False),
    ("Snake Skull", "蛇头骨", "古物", 150, False),
    ("Snake Vertebrae", "蛇脊椎", "古物", 100, False),
    ("Strange Doll (green)", "诡异玩偶(绿)", "古物", 1000, False),
    ("Strange Doll (yellow)", "诡异玩偶(黄)", "古物", 1000, False),
    ("Ancient Drum", "古代鼓", "古物", 200, False),
    ("Ancient Sword", "古剑", "古物", 200, False),
    ("Anchor", "船锚", "古物", 100, False),
    ("Chipped Amphora", "碎双耳瓶", "古物", 100, False),
    ("Nautilus Fossil", "鹦鹉螺化石", "古物", 100, False),
    ("Prehistoric Handaxe", "史前手斧", "古物", 100, False),
    ("Prehistoric Scapula", "史前肩胛骨", "古物", 100, False),
    ("Prehistoric Vertebra", "史前脊椎", "古物", 100, False),
    ("Prehistoric Rib", "史前肋骨", "古物", 100, False),
    ("Prehistoric Skull", "史前头骨", "古物", 100, False),
    ("Prehistoric Tibia", "史前胫骨", "古物", 100, False),
    ("Prehistoric Tool", "史前工具", "古物", 100, False),
    
    # ===== 怪物战利品 =====
    ("Bat Wing", "蝙蝠翅膀", "怪物战利品", 15, False),
    ("Bug Meat", "虫肉", "怪物战利品", 30, False),
    ("Solar Essence", "太阳精华", "怪物战利品", 80, False),
    ("Void Essence", "虚空精华", "怪物战利品", 80, False),
    ("Slime", "史莱姆泥", "怪物战利品", 5, False),
    ("Spider Eggs", "蜘蛛蛋", "怪物战利品", 50, False),
    
    # ===== 书 =====
    ("Book of Stars", "星辰之书", "书", 20000, False),
    ("Queen of Sauce Cookbook", "酱料女皇食谱", "书", 5000, False),
    ("Stardew Valley Almanac", "星露谷物语年鉴", "书", 20000, False),
    
    # ===== 季节采集物 =====
    ("Wild Horseradish", "野山葵", "季节采集物", 50, True),
    ("Spice Berry", "香料浆果", "季节采集物", 80, True),
    ("Spring Onion", "大葱", "季节采集物", 8, True),
    ("Leek", "韭菜", "季节采集物", 60, True),
    ("Dandelion", "蒲公英", "季节采集物", 40, True),
    ("Salmonberry", "美洲大树莓", "季节采集物", 5, False),
    ("Morel", "羊肚菌", "季节采集物", 150, True),
    ("Common Mushroom", "普通蘑菇", "季节采集物", 40, True),
    ("Hazelnut", "榛子", "季节采集物", 90, True),
    ("Wild Plum", "野梅", "季节采集物", 80, True),
    ("Blackberry", "黑莓", "季节采集物", 20, True),
    ("Chanterelle", "鸡油菌", "季节采集物", 160, True),
    ("Red Mushroom", "红蘑菇", "季节采集物", 75, True),
    ("Purple Mushroom", "紫蘑菇", "季节采集物", 250, True),
    ("Coconut", "椰子", "季节采集物", 100, True),
    ("Coral", "珊瑚", "季节采集物", 80, False),
    ("Sea Urchin", "海胆", "季节采集物", 160, False),
    ("Snow Yam", "雪山药", "季节采集物", 100, True),
    ("Winter Root", "冬根", "季节采集物", 70, True),
    ("Crystal Fruit", "水晶果", "季节采集物", 150, True),
    ("Holly", "冬青树", "季节采集物", 80, False),
    ("Ginger", "姜", "季节采集物", 160, True),
    ("Magma Cap", "熔岩菇", "季节采集物", 400, True),
    ("Rainbow Shell", "彩虹贝壳", "季节采集物", 300, False),
    ("Nautilus Shell", "鹦鹉螺", "季节采集物", 120, False),
    ("Mussel", "贻贝", "季节采集物", 30, False),
    ("Clam", "蛤", "季节采集物", 50, False),
    ("Cockle", "鸟蛤", "季节采集物", 50, False),
    ("Shrimp", "虾", "季节采集物", 60, False),
    ("Crab", "螃蟹", "季节采集物", 100, False),
    ("Lobster", "龙虾", "季节采集物", 120, False),
    ("Crayfish", "小龙虾", "季节采集物", 75, False),
    ("Periwinkle", "玉黍螺", "季节采集物", 20, False),
    ("Oyster", "牡蛎", "季节采集物", 40, False),
    ("Fossilized Leg", "化石腿", "季节采集物", 100, False),
    ("Fossilized Ribs", "化石肋骨", "季节采集物", 100, False),
    ("Fossilized Skull", "化石头骨", "季节采集物", 100, False),
    ("Fossilized Spine", "化石脊柱", "季节采集物", 100, False),
    ("Fossilized Tail", "化石尾巴", "季节采集物", 100, False),
]

def main():
    print("=" * 60)
    print("星露谷物品数据重建")
    print("=" * 60)
    
    # Load gifting data from existing files
    gifting_lookup = {}
    for fname in ['items_complete.json', 'items_zh.json', 'items_gift.json']:
        fpath = os.path.join(BASE, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for item in data:
                for key in ['name', 'name_en']:
                    k = item.get(key, '')
                    g = item.get('gifting', {})
                    if k and g:
                        gifting_lookup[k] = g
            print(f"Loaded gifting from {fname} ({len(data)} items)")
    
    items_data = []
    item_id = 1
    
    for cat in CATEGORIES:
        cat_items = [x for x in ALL_ITEMS if x[2] == cat]
        for name_en, name_zh, category, price, has_quality in cat_items:
            qualities = {}
            if has_quality and price > 0:
                qualities = {
                    "普通": price,
                    "银星": int(price * 1.25),
                    "金星": int(price * 1.5),
                    "铱星": int(price * 2.0)
                }
            
            gifting = gifting_lookup.get(name_zh, gifting_lookup.get(name_en, {}))
            if not gifting:
                gifting = {"love": [], "like": [], "neutral": [], "dislike": [], "hate": []}
            
            image = find_image(name_en, name_zh)
            
            item = {
                "id": item_id,
                "name": name_zh,
                "name_en": name_en,
                "category": category,
                "price": price,
                "has_quality": has_quality,
                "qualities": qualities,
                "image": image,
                "gifting": gifting
            }
            items_data.append(item)
            item_id += 1
    
    save_json('items_complete.json', items_data)
    
    simple = [{
        "id": i["id"], "name": i["name"], "category": i["category"],
        "price": i["price"], "has_quality": i["has_quality"],
        "qualities": i["qualities"], "image": i["image"]
    } for i in items_data]
    save_json('items_for_frontend.json', simple)
    
    print(f"\nTotal: {len(items_data)} items")
    for cat in CATEGORIES:
        count = sum(1 for i in items_data if i['category'] == cat)
        print(f"  {cat}: {count}")
    
    quality_count = sum(1 for i in items_data if i['has_quality'])
    print(f"\nQuality items: {quality_count}")
    
    no_img = [i for i in items_data if not i['image']]
    print(f"Without images: {len(no_img)}")
    if no_img:
        for item in no_img[:5]:
            print(f"  {item['name']} ({item['name_en']})")

if __name__ == '__main__':
    main()