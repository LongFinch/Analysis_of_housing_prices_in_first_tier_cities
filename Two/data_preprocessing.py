import os
import json


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_content = file.read()
    return json_content


def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def merge_and_remove_duplicates(input_directory, output_json_path):
    # 获取目录下所有 JSON 文件的路径
    json_files = [f for f in os.listdir(input_directory) if f.endswith('.json')]

    # 初始化一个空列表来保存所有 JSON 文件的数据
    all_data = []

    # 逐个读取每个 JSON 文件的内容并合并到 all_data 列表中
    for json_file in json_files:
        json_path = os.path.join(input_directory, json_file)
        json_content = read_json_file(json_path)
        data = json.loads(json_content)
        all_data.extend(data)

    # 将每个项表示为元组，以便进行比较
    tuple_data = [tuple(item.items()) for item in all_data]

    # 根据元组去重
    unique_data = list(set(tuple_data))

    # 将去重后的结果转换为字典格式
    unique_data_dicts = [dict(item) for item in unique_data]

    print(len(unique_data_dicts))
    # 将结果写入新的 JSON 文件
    write_json_file(output_json_path, unique_data_dicts)

    print("合并和去重完成，并保存到 {} 文件中。".format(output_json_path))

merge_and_remove_duplicates('./original_data/sz',
                            'merged_datas/merged_sz.json')
