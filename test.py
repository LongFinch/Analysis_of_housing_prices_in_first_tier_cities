import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 指定使用的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 如果你使用的是SimHei字体
sns.set(font='SimHei')  # 如果你使用的是SimHei字体
# 存储所有城市的数据的列表
all_city_data = []

# 指定城市文件所在的目录
directory_path = './Two/cleaned_data'

# 获取目录中所有文件的文件名列表
file_list = os.listdir(directory_path)

# 遍历每个文件
for file_name in file_list:
    if file_name.endswith('.csv'):  # 确保文件是CSV文件
        # 构建完整的文件路径
        file_path = os.path.join(directory_path, file_name)

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 处理朝向
        def process_direction(row):
            directions = row['direction'].split('/')
            if not set(directions).issubset(
                    {'东', '西', '南', '北', '东南', '西南', '东北', '西北'}):
                name_directions = row['name'].split()[-1].replace('卧',
                                                                  '').split(
                    '/')
                return name_directions
            else:
                return directions

        # 应用处理朝向的函数
        df['processed_direction'] = df.apply(process_direction, axis=1)

        # 计算朝向对应的租金（取平均值）
        df_expanded = df.explode('processed_direction')
        df_expanded['price_per_m2'] = df_expanded['price_per_m2'].astype(float)
        result = df_expanded.groupby('processed_direction')[
            'price_per_m2'].mean().reset_index()

        # 将城市名作为新的一列
        result['city'] = file_name.split('_')[0]

        # 将结果添加到列表中
        all_city_data.append(result)

# 将所有城市的数据合并到一个 DataFrame 中
merged_data = pd.concat(all_city_data, ignore_index=True)

# 创建条状图
fig, ax = plt.subplots(figsize=(12, 6))

# 遍历每个城市，绘制条状图
bar_width = 0.1  # 设置柱子宽度
directions = merged_data['processed_direction'].unique()
for i, direction in enumerate(directions):
    direction_data = merged_data[merged_data['processed_direction'] == direction]
    positions = np.arange(len(direction_data['city'])) + i * (bar_width + 0.02)
    ax.bar(positions, direction_data['price_per_m2'], width=bar_width, label=direction)

    # 添加一位小数数字标签，字号小一号
    for pos, value in zip(positions, direction_data['price_per_m2']):
        ax.text(pos, value + 0.1, f'{value:.1f}', ha='center', va='bottom', fontsize=6)

# 设置图形属性
ax.set_title('均价对比')
ax.set_xlabel('城市')
ax.set_ylabel('均价(元/平米)')
ax.set_xticks(np.arange(len(merged_data['city'].unique())) + (len(directions)-1) * (bar_width + 0.02) / 2)
ax.set_xticklabels(merged_data['city'].unique())
ax.legend()

# 显示图形
plt.show()
