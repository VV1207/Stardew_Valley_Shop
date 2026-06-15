import re

with open(r'd:\xampp\htdocs\Stardew_Valley\news.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check current state for each recipe
recipes = {
    '黑莓脆皮饼': '{name:"黑莓",img:"images/Blackberry.png",qty:1},{name:"大麦粉",img:"images/Wheat_Flour.png",qty:1},{name:"糖",img:"images/Sugar.png",qty:1}',
    '蟹黄糕': '{name:"螃蟹",img:"images/Crab.png",qty:1},{name:"大麦粉",img:"images/Wheat_Flour.png",qty:1},{name:"蛋",img:"images/Egg.png",qty:1},{name:"油",img:"images/Oil.png",qty:1}',
    '意式蕨菜炖饭': '{name:"油",img:"images/Oil.png",qty:1},{name:"蕨菜",img:"images/Fiddlehead_Fern.png",qty:1},{name:"蒜",img:"images/Garlic.png",qty:1}',
    '虞美人籽松糕': '{name:"虞美人花",img:"images/Poppy.png",qty:1},{name:"大麦粉",img:"images/Wheat_Flour.png",qty:1},{name:"糖",img:"images/Sugar.png",qty:1}',
    '龙虾浓汤': '{name:"龙虾",img:"images/Lobster.png",qty:1},{name:"牛奶",img:"images/Milk.png",qty:1}',
}

for name, ings in recipes.items():
    # Find the line with this recipe name
    pattern = f'(name:"{re.escape(name)}"[^}}]*img:"images/[^"]*\\.png")\\}}'
    match = re.search(pattern, content)
    if match:
        old = match.group(0)
        new = match.group(1) + ',ingredients:[' + ings + ']}'
        content = content.replace(old, new, 1)
        print(f'Updated: {name}')
    else:
        print(f'NOT FOUND: {name}')

with open(r'd:\xampp\htdocs\Stardew_Valley\news.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('All done')