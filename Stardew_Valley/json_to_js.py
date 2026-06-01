import json, os, sys

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'items_complete.json')
out_path = os.path.join(base_dir, 'items_data.js')

os.chdir(base_dir)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(out_path, 'w', encoding='utf-8') as out:
    out.write('// 星露谷全物品数据 - 自动生成\n')
    out.write('window.ITEMS_DATA = ')
    json.dump(data, out, ensure_ascii=False, indent=2)
    out.write(';\n')

print(f'OK - items_data.js generated, {len(data)} items')
