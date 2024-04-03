import json

def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    '''
    for item in data:
        if 'area' in item and isinstance(item['area'], list) and len(item['area']) == 1:
            item['area'] = float(item['area'][0])
        elif 'area' in item:
            del item['area']
    '''
    for item in data:
        if 'total_price' in item:
            item['total_price'] = float(item['total_price'])
        elif 'total_price' in item:
            del item['total_price']

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

# 示例使用
'''
json_file_path = './original_data/sz/sz_data7.json'  # 替换为实际的JSON文件路径
'''
json_file_path = 'merged_dara_json/merged_gz.json'  # 替换为实际的JSON文件路径
process_json_file(json_file_path)

