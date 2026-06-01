#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
星露谷完整物品数据生成器 - 最终版
从零构建完整的19分类数据集
"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_json(filename, data):
    with open(os.path.join(BASE_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 19个标准分类
CATEGORIES = [
    "作物", "动物", "果树", "工匠制品", "家具", "墙纸", "地板",
    "矿物", "渔具", "武器", "帽子", "鞋类", "戒指", "菜品",
    "农场工具", "古物", "怪物战利品", "书", "季节采集物"
]

# 品质分类
QUALITY_CATS = {"作物", "季节采集物"}

# 所有物品的完整数据 (name_en, name_zh, category, price, image)
ALL_ITEMS = [
    # ===== 作物 (Crops) =====
    ("Amaranth", "苋菜", "作物", 150, "Amaranth.png"),
    ("Artichoke", "洋蓟", "作物", 160, "Artichoke.png"),
    ("Beet", "甜菜", "作物", 100, "Beet.png"),
    ("Bok Choy", "大白菜", "作物", 80, "Bok Choy.png"),
    ("Broccoli", "西兰花", "作物", 70, "Broccoli.png"),
    ("Carrot", "胡萝卜", "作物", 60, "Carrot.png"),
    ("Cauliflower", "花椰菜", "作物", 175, "Cauliflower.png"),
    ("Corn", "玉米", "作物", 50, "Corn.png"),
    ("Eggplant", "茄子", "作物", 60, "Eggplant.png"),
    ("Fiddlehead Fern", "蕨菜", "作物", 90, "Fiddlehead Fern.png"),
    ("Garlic", "大蒜", "作物", 60, "Garlic.png"),
    ("Green Bean", "绿豆", "作物", 40, "Green Bean.png"),
    ("Hops", "啤酒花", "作物", 25, "Hops.png"),
    ("Kale", "甘蓝菜", "作物", 110, "Kale.png"),
    ("Parsnip", "防风草", "作物", 35, "Parsnip.png"),
    ("Potato", "土豆", "作物", 80, "Potato.png"),
    ("Pumpkin", "南瓜", "作物", 320, "Pumpkin.png"),
    ("Radish", "萝卜", "作物", 90, "Radish.png"),
    ("Red Cabbage", "红叶卷心菜", "作物", 260, "Red Cabbage.png"),
    ("Taro Root", "芋头", "作物", 100, "Taro Root.png"),
    ("Tea Leaves", "茶叶", "作物", 50, "Tea Leaves.png"),
    ("Tomato", "西红柿", "作物", 60, "Tomato.png"),
    ("Unmilled Rice", "未碾米", "作物", 30, "Unmilled Rice.png"),
    ("Wheat", "小麦", "作物", 25, "Wheat.png"),
    ("Yam", "山药", "作物", 160, "Yam.png"),
    ("Summer Squash", "西葫芦", "作物", 45, "Summer Squash.png"),
    # Fruits (also crops)
    ("Blueberry", "蓝莓", "作物", 50, "Blueberry.png"),
    ("Cactus Fruit", "仙人掌果子", "作物", 75, "Cactus Fruit.png"),
    ("Cranberries", "蔓越莓", "作物", 75, "Cranberries.png"),
    ("Hot Pepper", "辣椒", "作物", 40, "Hot Pepper.png"),
    ("Melon", "甜瓜", "作物", 250, "Melon.png"),
    ("Starfruit", "杨桃", "作物", 750, "Starfruit.png"),
    ("Strawberry", "草莓", "作物", 120, "Strawberry.png"),
    ("Ancient Fruit", "上古水果", "作物", 550, "Ancient Fruit.png"),
    ("Rhubarb", "大黄", "作物", 220, "Rhubarb.png"),
    ("Sweet Gem Berry", "甜宝石", "作物", 3000, "Sweet Gem Berry.png"),
    ("Powdermelon", "粉瓜", "作物", 180, "Powdermelon.png"),
    ("Qi Fruit", "齐瓜", "作物", 1, "Qi Fruit.png"),
    ("Pineapple", "菠萝", "作物", 300, "Pineapple.png"),
    # Flowers (also crops)
    ("Blue Jazz", "蓝爵", "作物", 50, "Blue Jazz.png"),
    ("Fairy Rose", "玫瑰仙子", "作物", 290, "Fairy Rose.png"),
    ("Poppy", "虞美人花", "作物", 140, "Poppy.png"),
    ("Summer Spangle", "夏季亮片", "作物", 90, "Summer Spangle.png"),
    ("Sunflower", "向日葵", "作物", 80, "Sunflower.png"),
    ("Tulip", "郁金香", "作物", 30, "Tulip.png"),
    ("Coffee Bean", "咖啡豆", "作物", 15, "Coffee Bean.png"),
    
    # ===== 动物产品 (Animal Products) =====
    ("Brown Egg", "棕色鸡蛋", "动物", 50, "Brown Egg.png"),
    ("White Egg", "白色鸡蛋", "动物", 50, "White Egg.png"),
    ("Duck Egg", "鸭蛋", "动物", 80, "Duck Egg.png"),
    ("Void Egg", "虚空蛋", "动物", 300, "Void Egg.png"),
    ("Golden Egg", "金蛋", "动物", 2000, "Golden Egg.png"),
    ("Large Brown Egg", "大棕色鸡蛋", "动物", 75, "Large Brown Egg.png"),
    ("Large White Egg", "大白色鸡蛋", "动物", 75, "Large White Egg.png"),
    ("Egg", "鸡蛋", "动物", 50, "Egg.png"),
    ("Large Egg", "大鸡蛋", "动物", 75, "Large Egg.png"),
    ("Milk", "牛奶", "动物", 125, "Milk.png"),
    ("Large Milk", "大壶牛奶", "动物", 175, "Large Milk.png"),
    ("Goat Milk", "羊奶", "动物", 225, "Goat Milk.png"),
    ("Large Goat Milk", "大壶羊奶", "动物", 300, "Large Goat Milk.png"),
    ("Ostrich Egg", "鸵鸟蛋", "动物", 600, "Ostrich Egg.png"),
    ("Duck Feather", "鸭毛", "动物", 250, "Duck Feather.png"),
    ("Rabbit's Foot", "兔子的脚", "动物", 565, "Rabbit's Foot.png"),
    ("Wool", "动物毛", "动物", 340, "Wool.png"),
    ("Truffle", "松露", "动物", 625, "Truffle.png"),
    
    # ===== 果树 (Fruit Trees) =====
    ("Apple", "苹果", "果树", 100, "Apple.png"),
    ("Apricot", "杏子", "果树", 50, "Apricot.png"),
    ("Banana", "香蕉", "果树", 150, "Banana.png"),
    ("Cherry", "樱桃", "果树", 80, "Cherry.png"),
    ("Mango", "芒果", "果树", 130, "Mango.png"),
    ("Orange", "橙子", "果树", 100, "Orange.png"),
    ("Peach", "桃子", "果树", 140, "Peach.png"),
    ("Pomegranate", "石榴", "果树", 140, "Pomegranate.png"),
    
    # ===== 工匠制品 (Artisan Goods) =====
    ("Aged Roe", "陈酿鱼子酱", "工匠制品", 400, "Aged Roe.png"),
    ("Beer", "啤酒", "工匠制品", 200, "Beer.png"),
    ("Caviar", "鱼子酱", "工匠制品", 500, "Caviar.png"),
    ("Cheese", "奶酪", "工匠制品", 230, "Cheese.png"),
    ("Cloth", "布料", "工匠制品", 470, "Cloth.png"),
    ("Coffee", "咖啡", "工匠制品", 150, "Coffee.png"),
    ("Dinosaur Mayonnaise", "恐龙蛋黄酱", "工匠制品", 800, "Dinosaur Mayonnaise.png"),
    ("Dried Fruit", "水果干", "工匠制品", 100, "Dried Fruit.png"),
    ("Dried Mushrooms", "蘑菇干", "工匠制品", 100, "Dried Mushrooms.png"),
    ("Duck Mayonnaise", "鸭蛋黄酱", "工匠制品", 375, "Duck Mayonnaise.png"),
    ("Goat Cheese", "羊奶酪", "工匠制品", 375, "Goat Cheese.png"),
    ("Green Tea", "绿茶", "工匠制品", 100, "Green Tea.png"),
    ("Honey", "蜂蜜", "工匠制品", 100, "Honey.png"),
    ("Juice", "果汁", "工匠制品", 75, "Juice.png"),
    ("Maple Syrup", "枫糖浆", "工匠制品", 200, "Maple Syrup.png"),
    ("Mayonnaise", "蛋黄酱", "工匠制品", 190, "Mayonnaise.png"),
    ("Mead", "蜜蜂酒", "工匠制品", 300, "Mead.png"),
    ("Mystic Syrup", "神秘糖浆", "工匠制品", 4000, "Mystic Syrup.png"),
    ("Oak Resin", "橡树树脂", "工匠制品", 150, "Oak Resin.png"),
    ("Oil", "油", "工匠制品", 100, "Oil.png"),
    ("Pale Ale", "淡啤酒", "工匠制品", 300, "Pale Ale.png"),
    ("Pine Tar", "松焦油", "工匠制品", 100, "Pine Tar.png"),
    ("Raisins", "葡萄干", "工匠制品", 600, "Raisins.png"),
    ("Roe", "鱼子", "工匠制品", 100, "Roe.png"),
    ("Smoked Fish", "熏鱼", "工匠制品", 100, "Smoked Fish.png"),
    ("Truffle Oil", "松露油", "工匠制品", 1065, "Truffle Oil.png"),
    ("Void Mayonnaise", "虚空蛋黄酱", "工匠制品", 275, "Void Mayonnaise.png"),
    ("Wine", "果酒", "工匠制品", 400, "Wine.png"),
    
    # ===== 家具 (Furniture) =====
    ("Chest", "箱子", "家具", 0, "Chest.png"),
    ("Stone Chest", "石箱", "家具", 0, "Stone Chest.png"),
    ("Bed", "床", "家具", 0, "Bed.png"),
    ("Chair", "椅子", "家具", 0, "Chair.png"),
    ("Table", "桌子", "家具", 0, "Table.png"),
    ("Lamp", "灯", "家具", 0, "Lamp.png"),
    ("Rug", "地毯", "家具", 0, "Rug.png"),
    ("TV", "电视机", "家具", 0, "TV.png"),
    ("Stove", "炉灶", "家具", 0, "Stove.png"),
    ("Refrigerator", "冰箱", "家具", 0, "Refrigerator.png"),
    ("Sofa", "沙发", "家具", 0, "Sofa.png"),
    ("Dresser", "梳妆台", "家具", 0, "Dresser.png"),
    ("Bookshelf", "书架", "家具", 0, "Bookshelf.png"),
    ("End Table", "茶几", "家具", 0, "End Table.png"),
    ("Potted Plant", "盆栽", "家具", 0, "Potted Plant.png"),
    ("Window", "窗户", "家具", 0, "Window.png"),
    ("Wall Decoration", "墙饰", "家具", 0, "Wall Decoration.png"),
    ("Fish Tank", "鱼缸", "家具", 0, "Fish Tank.png"),
    ("Candle", "蜡烛", "家具", 0, "Candle.png"),
    
    # ===== 墙纸 (Wallpaper) =====
    ("Wallpaper (Plain)", "素色墙纸", "墙纸", 100, "Wallpaper.png"),
    ("Wallpaper (Floral)", "碎花墙纸", "墙纸", 100, "Wallpaper Floral.png"),
    ("Wallpaper (Striped)", "条纹墙纸", "墙纸", 100, "Wallpaper Striped.png"),
    ("Wallpaper (Plaid)", "格子墙纸", "墙纸", 100, "Wallpaper Plaid.png"),
    ("Wallpaper (Brick)", "砖纹墙纸", "墙纸", 100, "Wallpaper Brick.png"),
    
    # ===== 地板 (Floor) =====
    ("Wood Floor", "木地板", "地板", 100, "Wood Floor.png"),
    ("Stone Floor", "石地板", "地板", 100, "Stone Floor.png"),
    ("Crystal Floor", "水晶地板", "地板", 100, "Crystal Floor.png"),
    ("Brick Floor", "砖地板", "地板", 100, "Brick Floor.png"),
    ("Path", "小路", "地板", 100, "Path.png"),
    ("Cobblestone Path", "卵石路", "地板", 100, "Cobblestone Path.png"),
    ("Stepping Stone Path", "踏石路", "地板", 100, "Stepping Stone Path.png"),
    
    # ===== 矿物 (Minerals) =====
    ("Diamond", "钻石", "矿物", 750, "Diamond.png"),
    ("Prismatic Shard", "五彩碎片", "矿物", 2000, "Prismatic Shard.png"),
    ("Aquamarine", "海蓝宝石", "矿物", 180, "Aquamarine.png"),
    ("Emerald", "绿宝石", "矿物", 250, "Emerald.png"),
    ("Jade", "翡翠", "矿物", 200, "Jade.png"),
    ("Ruby", "红宝石", "矿物", 300, "Ruby.png"),
    ("Amethyst", "紫水晶", "矿物", 100, "Amethyst.png"),
    ("Topaz", "黄水晶", "矿物", 120, "Topaz.png"),
    ("Earth Crystal", "地晶", "矿物", 200, "Earth Crystal.png"),
    ("Frozen Tear", "泪晶", "矿物", 200, "Frozen Tear.png"),
    ("Fire Quartz", "火石英", "矿物", 120, "Fire Quartz.png"),
    ("Quartz", "石英", "矿物", 50, "Quartz.png"),
    
    # ===== 渔具 (Fishing Tackle) =====
    ("Barbed Hook", "倒刺钩", "渔具", 500, "Barbed Hook.png"),
    ("Cork Bobber", "软木塞浮标", "渔具", 750, "Cork Bobber.png"),
    ("Curiosity Lure", "好奇心鱼饵", "渔具", 500, "Curiosity Lure.png"),
    ("Dressed Spinner", "装饰旋转亮片", "渔具", 500, "Dressed Spinner.png"),
    ("Lead Bobber", "铅制浮标", "渔具", 200, "Lead Bobber.png"),
    ("Quality Bobber", "优质浮标", "渔具", 750, "Quality Bobber.png"),
    ("Sonar Bobber", "声纳浮标", "渔具", 300, "Sonar Bobber.png"),
    ("Spinner", "旋转亮片", "渔具", 250, "Spinner.png"),
    ("Trap Bobber", "陷阱浮标", "渔具", 400, "Trap Bobber.png"),
    ("Treasure Hunter", "寻宝者", "渔具", 400, "Treasure Hunter.png"),
    ("Magnet", "磁铁", "渔具", 1000, "Magnet.png"),
    ("Wild Bait", "野生鱼饵", "渔具", 5, "Wild Bait.png"),
    ("Bait", "鱼饵", "渔具", 5, "Bait.png"),
    ("Challenge Bait", "挑战鱼饵", "渔具", 5, "Challenge Bait.png"),
    
    # ===== 武器 (Weapons) =====
    ("Rusty Sword", "生锈的剑", "武器", 100, "Rusty Sword.png"),
    ("Silver Saber", "银剑", "武器", 750, "Silver Saber.png"),
    ("Dark Sword", "黑暗之剑", "武器", 800, "Dark Sword.png"),
    ("Galaxy Sword", "银河剑", "武器", 5000, "Galaxy Sword.png"),
    ("Lava Katana", "熔岩武士刀", "武器", 2500, "Lava Katana.png"),
    ("Bone Sword", "骨剑", "武器", 600, "Bone Sword.png"),
    ("Galaxy Hammer", "银河锤", "武器", 3500, "Galaxy Hammer.png"),
    ("Galaxy Dagger", "银河匕首", "武器", 3500, "Galaxy Dagger.png"),
    ("Obsidian Edge", "黑曜石之刃", "武器", 1200, "Obsidian Edge.png"),
    ("Claymore", "双刃大剑", "武器", 700, "Claymore.png"),
    ("Templar's Blade", "圣殿骑士剑", "武器", 1500, "Templar's Blade.png"),
    ("Steel Falchion", "钢制弯刀", "武器", 2000, "Steel Falchion.png"),
    ("Wicked Kris", "邪恶匕首", "武器", 800, "Wicked Kris.png"),
    ("Forest Sword", "森林剑", "武器", 900, "Forest Sword.png"),
    ("Wooden Blade", "木剑", "武器", 50, "Wooden Blade.png"),
    ("Slingshot", "弹弓", "武器", 500, "Slingshot.png"),
    ("Master Slingshot", "高级弹弓", "武器", 1000, "Master Slingshot.png"),
    ("Galaxy Slingshot", "银河弹弓", "武器", 5000, "Galaxy Slingshot.png"),
    
    # ===== 帽子 (Hats) =====
    ("Cowboy Hat", "牛仔帽", "帽子", 2000, "Cowboy Hat.png"),
    ("Straw Hat", "草帽", "帽子", 2000, "Straw Hat.png"),
    ("Top Hat", "大礼帽", "帽子", 4000, "Top Hat.png"),
    ("Wizard Hat", "巫师帽", "帽子", 4000, "Wizard Hat.png"),
    ("Fedora", "软呢帽", "帽子", 3000, "Fedora.png"),
    ("Hard Hat", "安全帽", "帽子", 4000, "Hard Hat.png"),
    ("Hunter's Cap", "猎人帽", "帽子", 1500, "Hunter's Cap.png"),
    ("Knight's Helmet", "骑士头盔", "帽子", 4000, "Knight's Helmet.png"),
    ("Santa Hat", "圣诞帽", "帽子", 4000, "Santa Hat.png"),
    ("Miner's Helmet", "矿工头盔", "帽子", 1500, "Miner's Helmet.png"),
    ("Skeleton Mask", "骷髅面具", "帽子", 3000, "Skeleton Mask.png"),
    
    # ===== 鞋类 (Boots/Shoes) =====
    ("Leather Boots", "皮靴", "鞋类", 500, "Leather Boots.png"),
    ("Work Boots", "工作靴", "鞋类", 500, "Work Boots.png"),
    ("Combat Boots", "战斗靴", "鞋类", 750, "Combat Boots.png"),
    ("Tundra Boots", "冻土靴", "鞋类", 1000, "Tundra Boots.png"),
    ("Crystal Shoes", "水晶鞋", "鞋类", 1250, "Crystal Shoes.png"),
    ("Space Boots", "太空靴", "鞋类", 1250, "Space Boots.png"),
    ("Firewalker Boots", "蹈火者靴", "鞋类", 1500, "Firewalker Boots.png"),
    ("Dragonscale Boots", "龙鳞靴", "鞋类", 2000, "Dragonscale Boots.png"),
    ("Emily's Magic Boots", "艾米丽的魔法靴", "鞋类", 2500, "Emily's Magic Boots.png"),
    ("Prismatic Shoes", "五彩靴", "鞋类", 3000, "Prismatic Shoes.png"),
    
    # ===== 戒指 (Rings) =====
    ("Small Glow Ring", "小型辉光戒指", "戒指", 100, "Small Glow Ring.png"),
    ("Glow Ring", "辉光戒指", "戒指", 250, "Glow Ring.png"),
    ("Small Magnet Ring", "小型磁铁戒指", "戒指", 100, "Small Magnet Ring.png"),
    ("Magnet Ring", "磁铁戒指", "戒指", 250, "Magnet Ring.png"),
    ("Slime Charmer Ring", "史莱姆克星戒指", "戒指", 1500, "Slime Charmer Ring.png"),
    ("Warrior Ring", "战士戒指", "戒指", 1000, "Warrior Ring.png"),
    ("Vampire Ring", "吸血戒指", "戒指", 1500, "Vampire Ring.png"),
    ("Iridium Band", "铱环", "戒指", 5000, "Iridium Band.png"),
    ("Burglar's Ring", "窃贼戒指", "戒指", 1000, "Burglar's Ring.png"),
    ("Lucky Ring", "幸运戒指", "戒指", 7500, "Lucky Ring.png"),
    ("Napalm Ring", "凝固汽油弹戒指", "戒指", 5000, "Napalm Ring.png"),
    ("Phoenix Ring", "凤凰戒指", "戒指", 5000, "Phoenix Ring.png"),
    ("Hot Java Ring", "热咖啡戒指", "戒指", 2500, "Hot Java Ring.png"),
    ("Glowstone Ring", "发光石戒指", "戒指", 2000, "Glowstone Ring.png"),
    ("Ring of Yoba", "由巴之戒", "戒指", 1500, "Ring of Yoba.png"),
    ("Savage Ring", "野蛮戒指", "戒指", 1500, "Savage Ring.png"),
    ("Sturdy Ring", "结实戒指", "戒指", 1500, "Sturdy Ring.png"),
    ("Thorns Ring", "荆棘戒指", "戒指", 1500, "Thorns Ring.png"),
    
    # ===== 菜品 (Cooking) =====
    ("Fried Egg", "煎鸡蛋", "菜品", 35, "Fried Egg.png"),
    ("Omelet", "欧姆蛋", "菜品", 125, "Omelet.png"),
    ("Salad", "沙拉", "菜品", 110, "Salad.png"),
    ("Cheese Cauliflower", "乳酪花椰菜", "菜品", 300, "Cheese Cauliflower.png"),
    ("Baked Fish", "烤鱼", "菜品", 100, "Baked Fish.png"),
    ("Parsnip Soup", "防风草汤", "菜品", 85, "Parsnip Soup.png"),
    ("Vegetable Medley", "混合蔬菜", "菜品", 120, "Vegetable Medley.png"),
    ("Complete Breakfast", "完美早餐", "菜品", 350, "Complete Breakfast.png"),
    ("Fried Calamari", "炸鱿鱼", "菜品", 150, "Fried Calamari.png"),
    ("Strange Bun", "奇怪的小面包", "菜品", 75, "Strange Bun.png"),
    ("Lucky Lunch", "幸运午餐", "菜品", 250, "Lucky Lunch.png"),
    ("Fried Mushroom", "炒蘑菇", "菜品", 200, "Fried Mushroom.png"),
    ("Pizza", "披萨", "菜品", 300, "Pizza.png"),
    ("Bean Hotpot", "豆类火锅", "菜品", 100, "Bean Hotpot.png"),
    ("Glazed Yams", "琉璃山药", "菜品", 200, "Glazed Yams.png"),
    ("Carp Surprise", "惊奇鲤鱼", "菜品", 150, "Carp Surprise.png"),
    ("Hashbrowns", "薯饼", "菜品", 120, "Hashbrowns.png"),
    ("Pancakes", "薄煎饼", "菜品", 80, "Pancakes.png"),
    ("Rhubarb Pie", "大黄派", "菜品", 400, "Rhubarb Pie.png"),
    ("Cranberry Sauce", "蔓越莓酱", "菜品", 120, "Cranberry Sauce.png"),
    ("Stuffing", "塞料面包", "菜品", 165, "Stuffing.png"),
    ("Coleslaw", "卷心菜沙拉", "菜品", 200, "Coleslaw.png"),
    ("Autumn's Bounty", "秋日恩赐", "菜品", 350, "Autumn's Bounty.png"),
    ("Chocolate Cake", "巧克力蛋糕", "菜品", 200, "Chocolate Cake.png"),
    ("Pumpkin Pie", "南瓜派", "菜品", 385, "Pumpkin Pie.png"),
    ("Fish Taco", "鱼肉卷", "菜品", 500, "Fish Taco.png"),
    ("Crispy Bass", "香酥鲈鱼", "菜品", 150, "Crispy Bass.png"),
    ("Chowder", "蛤蜊浓汤", "菜品", 135, "Chowder.png"),
    ("Ice Cream", "冰淇淋", "菜品", 120, "Ice Cream.png"),
    ("Crab Cakes", "蟹肉糕", "菜品", 250, "Crab Cakes.png"),
    ("Algae Soup", "清汤", "菜品", 100, "Algae Soup.png"),
    ("Pumpkin Soup", "南瓜汤", "菜品", 250, "Pumpkin Soup.png"),
    ("Tom Kha Soup", "冬阴功汤", "菜品", 250, "Tom Kha Soup.png"),
    ("Maki Roll", "生鱼寿司", "菜品", 220, "Maki Roll.png"),
    ("Sashimi", "生鱼片", "菜品", 75, "Sashimi.png"),
    ("Tortilla", "墨西哥薄饼", "菜品", 50, "Tortilla.png"),
    ("Triple Shot Espresso", "三倍浓缩咖啡", "菜品", 450, "Triple Shot Espresso.png"),
    ("Seafoam Pudding", "海泡布丁", "菜品", 300, "Seafoam Pudding.png"),
    ("Bread", "面包", "菜品", 60, "Bread.png"),
    ("Cookie", "饼干", "菜品", 140, "Cookie.png"),
    ("Spaghetti", "意大利面", "菜品", 120, "Spaghetti.png"),
    ("Eggplant Parmesan", "帕尔玛茄子", "菜品", 200, "Eggplant Parmesan.png"),
    ("Stir Fry", "爆炒", "菜品", 200, "Stir Fry.png"),
    ("Blueberry Tart", "蓝莓挞", "菜品", 150, "Blueberry Tart.png"),
    ("Salmon Dinner", "三文鱼晚餐", "菜品", 300, "Salmon Dinner.png"),
    ("Lobster Bisque", "龙虾浓汤", "菜品", 500, "Lobster Bisque.png"),
    ("Escargot", "蜗牛沙拉", "菜品", 175, "Escargot.png"),
    ("Spicy Eel", "香辣鳗鱼", "菜品", 175, "Spicy Eel.png"),
    ("Super Meal", "超级餐", "菜品", 450, "Super Meal.png"),
    ("Miner's Treat", "矿工小吃", "菜品", 200, "Miner's Treat.png"),
    
    # ===== 农场工具 (Farm Tools / Fertilizer / Seeds) =====
    ("Basic Fertilizer", "基础肥料", "农场工具", 10, "Basic Fertilizer.png"),
    ("Basic Retaining Soil", "基础保湿土壤", "农场工具", 10, "Basic Retaining Soil.png"),
    ("Deluxe Fertilizer", "高级肥料", "农场工具", 40, "Deluxe Fertilizer.png"),
    ("Deluxe Retaining Soil", "高级保湿土壤", "农场工具", 20, "Deluxe Retaining Soil.png"),
    ("Deluxe Speed-Gro", "高级生长激素", "农场工具", 80, "Deluxe Speed-Gro.png"),
    ("Hyper Speed-Gro", "超速生长激素", "农场工具", 100, "Hyper Speed-Gro.png"),
    ("Quality Fertilizer", "优质肥料", "农场工具", 20, "Quality Fertilizer.png"),
    ("Quality Retaining Soil", "优质保湿土壤", "农场工具", 10, "Quality Retaining Soil.png"),
    ("Speed-Gro", "生长激素", "农场工具", 20, "Speed-Gro.png"),
    ("Tree Fertilizer", "树肥", "农场工具", 25, "Tree Fertilizer.png"),
    ("Mixed Seeds", "混合种子", "农场工具", 20, "Mixed Seeds.png"),
    ("Mixed Flower Seeds", "混合花卉种子", "农场工具", 30, "Mixed Flower Seeds.png"),
    ("Acorn", "橡子", "农场工具", 20, "Acorn.png"),
    ("Maple Seed", "枫树种子", "农场工具", 20, "Maple Seed.png"),
    ("Pine Cone", "松果", "农场工具", 20, "Pine Cone.png"),
    ("Mahogany Seed", "桃花心木种子", "农场工具", 50, "Mahogany Seed.png"),
    ("Tea Sapling", "茶苗", "农场工具", 500, "Tea Sapling.png"),
    ("Cactus Seeds", "仙人掌种子", "农场工具", 150, "Cactus Seeds.png"),
    ("Fiber Seeds", "纤维种子", "农场工具", 25, "Fiber Seeds.png"),
    
    # ===== 古物 (Artifacts) =====
    ("Ancient Doll", "古代玩偶", "古物", 250, "Ancient Doll.png"),
    ("Ancient Seed", "古代种子", "古物", 0, "Ancient Seed.png"),
    ("Arrowhead", "箭头", "古物", 100, "Arrowhead.png"),
    ("Bone Flute", "骨笛", "古物", 200, "Bone Flute.png"),
    ("Chicken Statue", "鸡雕像", "古物", 200, "Chicken Statue.png"),
    ("Chewing Stick", "咀嚼棒", "古物", 100, "Chewing Stick.png"),
    ("Dwarf Gadget", "矮人小工具", "古物", 200, "Dwarf Gadget.png"),
    ("Dwarvish Helm", "矮人头盔", "古物", 200, "Dwarvish Helm.png"),
    ("Dwarf Scroll I", "矮人卷轴 I", "古物", 10, "Dwarf Scroll I.png"),
    ("Dwarf Scroll II", "矮人卷轴 II", "古物", 10, "Dwarf Scroll II.png"),
    ("Dwarf Scroll III", "矮人卷轴 III", "古物", 10, "Dwarf Scroll III.png"),
    ("Dwarf Scroll IV", "矮人卷轴 IV", "古物", 10, "Dwarf Scroll IV.png"),
    ("Elvish Jewelry", "精灵珠宝", "古物", 300, "Elvish Jewelry.png"),
    ("Glass Shards", "玻璃碎片", "古物", 10, "Glass Shards.png"),
    ("Golden Mask", "黄金面具", "古物", 500, "Golden Mask.png"),
    ("Golden Relic", "黄金遗物", "古物", 500, "Golden Relic.png"),
    ("Ornamental Fan", "装饰扇子", "古物", 300, "Ornamental Fan.png"),
    ("Rusty Spoon", "生锈的勺子", "古物", 50, "Rusty Spoon.png"),
    ("Rusty Spur", "生锈的马刺", "古物", 50, "Rusty Spur.png"),
    ("Rusty Cog", "生锈的齿轮", "古物", 50, "Rusty Cog.png"),
    ("Rare Disc", "稀有圆盘", "古物", 300, "Rare Disc.png"),
    ("Skeletal Hand", "骷髅手部", "古物", 100, "Skeletal Hand.png"),
    ("Skeletal Tail", "骷髅尾部", "古物", 100, "Skeletal Tail.png"),
    ("Amphibian Fossil", "两栖动物化石", "古物", 100, "Amphibian Fossil.png"),
    ("Palm Fossil", "棕榈化石", "古物", 100, "Palm Fossil.png"),
    ("Trilobite", "三叶虫", "古物", 150, "Trilobite.png"),
    ("Dried Starfish", "干海星", "古物", 50, "Dried Starfish.png"),
    ("Large Animal Fossil", "大型动物化石", "古物", 150, "Large Animal Fossil.png"),
    ("Snake Skull", "蛇头骨", "古物", 150, "Snake Skull.png"),
    ("Snake Vertebrae", "蛇脊椎", "古物", 100, "Snake Vertebrae.png"),
    ("Strange Doll (green)", "诡异玩偶(绿)", "古物", 1000, "Strange Doll Green.png"),
    ("Strange Doll (yellow)", "诡异玩偶(黄)", "古物", 1000, "Strange Doll Yellow.png"),
    ("Ancient Drum", "古代鼓", "古物", 200, "Ancient Drum.png"),
    ("Ancient Sword", "古剑", "古物", 200, "Ancient Sword.png"),
    ("Anchor", "船锚", "古物", 100, "Anchor.png"),
    ("Chipped Amphora", "碎双耳瓶", "古物", 100, "Chipped Amphora.png"),
    ("Nautilus Fossil", "鹦鹉螺化石", "古物", 100, "Nautilus Fossil.png"),
    ("Prehistoric Handaxe", "史前手斧", "古物", 100, "Prehistoric Handaxe.png"),
    ("Prehistoric Scapula", "史前肩胛骨", "古物", 100, "Prehistoric Scapula.png"),
    ("Prehistoric Vertebra", "史前脊椎", "古物", 100, "Prehistoric Vertebra.png"),
    
    # ===== 怪物战利品 (Monster Loot) =====
    ("Bat Wing", "蝙蝠翅膀", "怪物战利品", 15, "Bat Wing.png"),
    ("Bug Meat", "虫肉", "怪物战利品", 30, "Bug Meat.png"),
    ("Solar Essence", "太阳精华", "怪物战利品", 80, "Solar Essence.png"),
    ("Void Essence", "虚空精华", "怪物战利品", 80, "Void Essence.png"),
    ("Spider Eggs", "蜘蛛蛋", "怪物战利品", 50, "Spider Eggs.png"),
    ("Gooey Glob", "粘糊团", "怪物战利品", 100, "Gooey Glob.png"),
    ("Cursed Doll", "诅咒玩偶", "怪物战利品", 1000, "Cursed Doll.png"),
    
    # ===== 书 (Books) =====
    ("Book of Stars", "星辰之书", "书", 20000, "Book of Stars.png"),
    ("Queen of Sauce Cookbook", "酱料女皇食谱", "书", 5000, "Queen of Sauce Cookbook.png"),
    ("Stardew Valley Almanac", "星露谷物语年鉴", "书", 20000, "Stardew Valley Almanac.png"),
    
    # ===== 季节采集物 (Seasonal Forage) =====
    ("Wild Horseradish", "野山葵", "季节采集物", 50, "Wild Horseradish.png"),
    ("Spice Berry", "香料浆果", "季节采集物", 80, "Spice Berry.png"),
    ("Spring Onion", "大葱", "季节采集物", 8, "Spring Onion.png"),
    ("Leek", "韭菜", "季节采集物", 60, "Leek.png"),
    ("Dandelion", "蒲公英", "季节采集物", 40, "Dandelion.png"),
    ("Salmonberry", "美洲大树莓", "季节采集物", 5, "Salmonberry.png"),
    ("Morel", "羊肚菌", "季节采集物", 150, "Morel.png"),
    ("Common Mushroom", "普通蘑菇", "季节采集物", 40, "Common Mushroom.png"),
    ("Hazelnut", "榛子", "季节采集物", 90, "Hazelnut.png"),
    ("Wild Plum", "野梅", "季节采集物", 80, "Wild Plum.png"),
    ("Blackberry", "黑莓", "季节采集物", 20, "Blackberry.png"),
    ("Chanterelle", "鸡油菌", "季节采集物", 160, "Chanterelle.png"),
    ("Red Mushroom", "红蘑菇", "季节采集物", 75, "Red Mushroom.png"),
    ("Purple Mushroom", "紫蘑菇", "季节采集物", 250, "Purple Mushroom.png"),
    ("Coconut", "椰子", "季节采集物", 100, "Coconut.png"),
    ("Coral", "珊瑚", "季节采集物", 80, "Coral.png"),
    ("Sea Urchin", "海胆", "季节采集物", 160, "Sea Urchin.png"),
    ("Snow Yam", "雪山药", "季节采集物", 100, "Snow Yam.png"),
    ("Winter Root", "冬根", "季节采集物", 70, "Winter Root.png"),
    ("Crystal Fruit", "水晶果", "季节采集物", 150, "Crystal Fruit.png"),
    ("Holly", "冬青树", "季节采集物", 80, "Holly.png"),
    ("Ginger", "姜", "季节采集物", 160, "Ginger.png"),
    ("Magma Cap", "熔岩菇", "季节采集物", 400, "Magma Cap.png"),
    ("Rainbow Shell", "彩虹贝壳", "季节采集物", 300, "Rainbow Shell.png"),
    ("Nautilus Shell", "鹦鹉螺", "季节采集物", 120, "Nautilus Shell.png"),
    ("Fossilized Leg", "化石腿", "季节采集物", 100, "Fossilized Leg.png"),
    ("Fossilized Ribs", "化石肋骨", "季节采集物", 100, "Fossilized Ribs.png"),
    ("Fossilized Skull", "化石头骨", "季节采集物", 100, "Fossilized Skull.png"),
    ("Fossilized Spine", "化石脊柱", "季节采集物", 100, "Fossilized Spine.png"),
    ("Fossilized Tail", "化石尾巴", "季节采集物", 100, "Fossilized Tail.png"),
]

def main():
    print("=" * 60)
    print("星露谷完整物品数据生成器 - 最终版")
    print("=" * 60)
    
    # Load existing data for gifting info
    existing = load_json('items_zh.json')
    gifting_lookup = {}
    for item in existing:
        name = item.get('name', '')
        name_en = item.get('name_en', '')
        gifting = item.get('gifting', {})
        if name:
            gifting_lookup[name] = gifting
        if name_en:
            gifting_lookup[name_en] = gifting
    
    print(f"Loaded {len(existing)} existing items for gifting info")
    
    # Build final dataset
    item_id = 1
    final_data = []
    
    for cat in CATEGORIES:
        cat_items = [x for x in ALL_ITEMS if x[2] == cat]
        for name_en, name_zh, category, price, image in cat_items:
            has_quality = category in QUALITY_CATS and price > 0
            qualities = {}
            if has_quality:
                qualities = {
                    "普通": price,
                    "银星": int(price * 1.25),
                    "金星": int(price * 1.5),
                    "铱星": int(price * 2.0)
                }
            
            # Get gifting from lookup
            gifting = gifting_lookup.get(name_zh, gifting_lookup.get(name_en, {"love":[], "like":[], "neutral":[], "dislike":[], "hate":[]}))
            
            item = {
                "id": item_id,
                "name": name_zh,
                "name_en": name_en,
                "category": category,
                "price": price,
                "has_quality": has_quality,
                "qualities": qualities,
                "image": f"images/{image}",
                "source": "",
                "description": "",
                "gifting": gifting
            }
            final_data.append(item)
            item_id += 1
    
    # Check for items in existing data that aren't in our list
    existing_names = {x[0] for x in ALL_ITEMS}
    for item in existing:
        name_en = item.get('name_en', '')
        if name_en and name_en not in existing_names:
            # Add it
            name_zh = item.get('name', name_en)
            cat = item.get('category', '其他')
            price = item.get('price', 0)
            
            if cat not in CATEGORIES:
                # Try to map
                cat_map = {
                    "蔬菜": "作物", "水果": "作物", "种子": "作物",
                    "动物制品": "动物", "工匠制品": "工匠制品",
                    "烹饪": "菜品", "肥料": "农场工具",
                    "资源": "资源", "垃圾": "垃圾",
                    "果树": "果树", "季节采集物": "季节采集物",
                }
                cat = cat_map.get(cat, cat)
            
            if cat not in CATEGORIES:
                print(f"  Skipping uncategorized: {name_zh} ({name_en}) [{cat}]")
                continue
            
            has_quality = cat in QUALITY_CATS and price > 0
            qualities = {}
            if has_quality:
                qualities = {
                    "普通": price,
                    "银星": int(price * 1.25),
                    "金星": int(price * 1.5),
                    "铱星": int(price * 2.0)
                }
            
            item = {
                "id": item_id,
                "name": name_zh,
                "name_en": name_en,
                "category": cat,
                "price": price,
                "has_quality": has_quality,
                "qualities": qualities,
                "image": item.get('image', ''),
                "source": item.get('source', ''),
                "description": item.get('description', ''),
                "gifting": item.get('gifting', {"love":[], "like":[], "neutral":[], "dislike":[], "hate":[]})
            }
            final_data.append(item)
            item_id += 1
    
    # Save
    output = os.path.join(BASE_DIR, 'items_complete.json')
    save_json(output, final_data)
    print(f"\nSaved {len(final_data)} items to items_complete.json")
    
    # Print stats
    print("\nCategory breakdown:")
    for cat in CATEGORIES:
        count = sum(1 for i in final_data if i['category'] == cat)
        print(f"  {cat}: {count}")
    
    other = sum(1 for i in final_data if i['category'] not in CATEGORIES)
    if other:
        print(f"  其他: {other}")
    
    # Zero price items
    zero = [i for i in final_data if i['price'] == 0]
    print(f"\nZero price items: {len(zero)}")
    for item in zero:
        print(f"  {item['name']} ({item.get('name_en','')}) [{item['category']}]")
    
    # Quality items
    quality = sum(1 for i in final_data if i['has_quality'])
    print(f"\nItems with quality: {quality}")
    
    # Also save simple version for frontend use
    simple = []
    for item in final_data:
        s = {
            "id": item["id"],
            "name": item["name"],
            "category": item["category"],
            "price": item["price"],
            "has_quality": item["has_quality"],
            "qualities": item["qualities"],
            "image": item["image"],
        }
        simple.append(s)
    
    simple_path = os.path.join(BASE_DIR, 'items_for_frontend.json')
    save_json(simple_path, simple)
    print(f"\nSaved simple version ({len(simple)} items) to items_for_frontend.json")

if __name__ == '__main__':
    main()