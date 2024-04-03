import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# 指定使用的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
sns.set(font='SimHei')

# 指定CSV文件所在的目录
directory_2022_path = '../merged_data'
directory_2023_path = './2023'
conversion_table = {'北京_cleaned.csv': '北京', '上海_cleaned.csv': '上海',
                    '广州_cleaned.csv': '广州', '深圳_cleaned.csv': '深圳'}

# 获取2022年目录下的所有CSV文件
csv_files_2022 = [file for file in os.listdir(directory_2022_path) if file.endswith('.csv')]

# 存储每个城市的房价信息
city_data = {'城市': [], '户型': [], '均价': [], '年份': []}

# 遍历每个城市
for i, csv_file_2022 in enumerate(csv_files_2022):
    # 构建CSV文件的完整路径
    file_path_2022 = os.path.join(directory_2022_path, csv_file_2022)
    city_name = conversion_table[csv_file_2022]

    # 读取2022年数据
    df_2022 = pd.read_csv(file_path_2022)

    # 遍历每种户型
    for room_type in [1, 2, 3]:
        # 筛选2022年数据
        df_room_2022 = df_2022[df_2022['室'] == room_type]

        # 计算2022年均价
        avg_price_2022 = df_room_2022['total_price'].mean()

        # 存储数据
        city_data['城市'].append(city_name)
        city_data['户型'].append(f'{room_type}居室')
        city_data['均价'].append(avg_price_2022)
        city_data['年份'].append('2022')


# 获取2023年目录下的所有CSV文件
csv_files_2023 = [file for file in os.listdir(directory_2023_path) if file.endswith('.csv')]

# 遍历每个城市
for i, csv_file_2023 in enumerate(csv_files_2023):
    # 构建CSV文件的完整路径
    file_path_2023 = os.path.join(directory_2023_path, csv_file_2023)
    city_name = conversion_table[csv_file_2023]

    # 读取2023年数据
    df_2023 = pd.read_csv(file_path_2023)

    # 遍历每种户型
    for room_type in [1, 2, 3]:
        # 筛选2023年数据
        df_room_2023 = df_2023[df_2023['室'] == room_type]

        # 计算2023年均价
        avg_price_2023 = df_room_2023['total_price'].mean()

        # 存储数据
        city_data['城市'].append(city_name)
        city_data['户型'].append(f'{room_type}居室')
        city_data['均价'].append(avg_price_2023)
        city_data['年份'].append('2023')

# 创建DataFrame
city_df = pd.DataFrame(city_data)

# 遍历每个城市
for city_name in conversion_table.values():
    # 筛选数据
    df_city = city_df[city_df['城市'] == city_name]

    # 使用Seaborn的catplot进行比较
    g = sns.catplot(x='户型', y='均价', hue='年份', data=df_city, kind='bar', height=5, aspect=1.5)

    # 在每个柱上添加数字
    for ax in g.axes.flat:
        for p in ax.patches:
            ax.text(p.get_x() + p.get_width() / 2., p.get_height(), f'{p.get_height():.2f}',
                    fontsize=14, color='black', ha='center', va='bottom')

    # 添加单位到y轴标签
    plt.ylabel('均价（元）')
    # 显示图表
    plt.title(f'{city_name}各户型平均租金变化')
    plt.show()
