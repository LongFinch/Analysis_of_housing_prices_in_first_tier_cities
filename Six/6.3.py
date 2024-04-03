import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 指定使用的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
sns.set(font='SimHei')

# 存储所有城市的数据的列表
all_city_data = []

# 指定城市文件所在的目录
directory_path = '../Two/cleaned_data/'

# 获取目录中所有文件的文件名列表
city_files = os.listdir(directory_path)

# 遍历每个文件
for city_file in city_files:
    # 拼接文件的完整路径
    file_path = os.path.join(directory_path, city_file)

    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 处理朝向
    def process_direction(row):
        directions = row['direction'].split('/')
        if not set(directions).issubset(
                {'东', '西', '南', '北', '东南', '西南', '东北', '西北'}):
            name_directions = row['name'].split()[-1].replace('卧', '').split('/')
            return name_directions
        else:
            return directions

    # 应用处理朝向的函数
    df['processed_direction'] = df.apply(process_direction, axis=1)

    # 拆分处理后的朝向
    df_expanded = df.explode('processed_direction')

    # 以板块和朝向分组，计算每个板块内每个朝向对应的平均租金
    grouped_result = df_expanded.groupby(['district', 'processed_direction'])['price_per_m2'].mean().reset_index()

    # 找出每个板块最贵的朝向
    most_expensive_directions = grouped_result.loc[grouped_result.groupby('district')['price_per_m2'].idxmax()]
    direction_district_num = {'东': 0, '西': 0, '南': 0, '北': 0, '东南': 0, '东北': 0, '西南': 0, '西北': 0}

    # 更新字典
    for index, row in most_expensive_directions.iterrows():
        direction_district_num[row['processed_direction']] += 1

    # 过滤掉值为0的项
    direction_district_num = {key: value for key, value in direction_district_num.items() if value != 0}

    # 定义数据
    labels = direction_district_num.keys()
    sizes = direction_district_num.values()

    # 绘制饼状图
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title(f'{city_file[0:2]}在各朝向租金最贵的板块数量分布')
    plt.show()
