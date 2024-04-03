import json

file_paths = {'北京': "./merged_datas/merged_bj1.json",
              '上海': "./merged_datas/merged_sh1.json",
              '广州': "./merged_datas/merged_gz2.json",
              '深圳': "./merged_datas/merged_sz1.json",
              "惠州": "./merged_datas/merged_hui1.json"}

for city, file_path in file_paths.items():
    # 读取JSON文件
    # file_path = "./merged_datas/merged_sh1.json"  # 请替换成你的JSON文件路径
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 统计元素数量
    element_count = len(data)

    # 打印结果
    print(f"城市{city}爬取到的房源数量: {element_count}")
