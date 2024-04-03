import os
import pandas as pd
import json
import re


# 将JSON转换为CSV的函数
def json_to_csv(json_file_path, output_csv_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 转换为DataFrame
    df = pd.DataFrame(data)

    # 使用正则表达式将 'layout' 列拆分为 '房间'、'室'、'厅'、'卫'
    room_pattern = re.compile(r'(\d+房间)?(\d+室)?(\d+厅)?(\d+卫)')

    df[['房间', '室', '厅', '卫']] = df['layout'].apply(lambda x: pd.Series(
        room_pattern.search(x).groups() if room_pattern.search(x) else (
        0, 0, 0, 0)
    ))
    df['房间'] = df['房间'].astype(str).str.extract('(\d+)').fillna(0)
    df['室'] = df['室'].astype(str).str.extract('(\d+)').fillna(0)
    df['厅'] = df['厅'].astype(str).str.extract('(\d+)').fillna(0)
    df['卫'] = df['卫'].astype(str).str.extract('(\d+)').fillna(0)

    # 删除原始 'layout' 列
    df = df.drop('layout', axis=1)

    # 添加均价列
    df['price_per_m2'] = df['total_price'] / df['area']

    # 保存为CSV
    df.to_csv(output_csv_path, index=False)


# 指定输入和输出目录
'''
input_directory = 'D:\Python_homework\Two\merged_dara_json'
output_directory = './merged_data'
'''

input_directory = '../RawData'
output_directory = '../merged_data'

# 确保输出目录存在
os.makedirs(output_directory, exist_ok=True)

# 遍历输入目录中的每个文件
for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        json_file_path = os.path.join(input_directory, filename)

        # 生成相应的CSV文件名
        csv_file_name = os.path.splitext(filename)[0] + '.csv'
        output_csv_path = os.path.join(output_directory, csv_file_name)

        # 将JSON转换为CSV
        json_to_csv(json_file_path, output_csv_path)

print("转换完成。")