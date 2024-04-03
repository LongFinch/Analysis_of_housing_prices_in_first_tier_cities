import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# 指定使用的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 如果你使用的是SimHei字体
sns.set(font='SimHei')  # 如果你使用的是SimHei字体

# 指定CSV文件所在的目录
directory_path = '../Two/cleaned_data'

# 获取目录下的所有CSV文件
csv_files = [file for file in os.listdir(directory_path) if
             file.endswith('.csv')]
conversion_table = {'北京_cleaned.csv': '北京', '上海_cleaned.csv': '上海',
                    '广州_cleaned.csv': '广州', '深圳_cleaned.csv': '深圳',
                    '惠州_cleaned.csv': '惠州'}

# 存储每个城市的房价信息
city_data = {'城市': [], '户型': [], '最高价': []}

# 遍历每个CSV文件
for csv_file in csv_files:
    # 构建CSV文件的完整路径
    file_path = os.path.join(directory_path, csv_file)
    city_name = conversion_table[csv_file]
    # 读取数据
    df = pd.read_csv(file_path)

    # 遍历每种户型
    for room_type in [1, 2, 3]:
        # 筛选数据
        df_room = df[df['室'] == room_type]

        # 计算最高价
        max_price = df_room['total_price'].max()

        # 存储数据
        city_data['城市'].append(city_name)
        city_data['户型'].append(f'{room_type}居室')
        city_data['最高价'].append(max_price)

# 创建DataFrame
city_df = pd.DataFrame(city_data)

# 绘制图表
plt.figure(figsize=(12, 8))

# Bar plot for maximum prices of one-bedroom, two-bedroom, and three-bedroom apartments for each city
sns.barplot(x='城市', y='最高价', hue='户型', data=city_df)

# 设置图表标题和标签
plt.title('各城市不同户型的最高租金')
plt.xlabel('城市')
plt.ylabel('最高租金(元)')

# 在每个柱子上加上数字
for p in plt.gca().patches:
    plt.gca().annotate(f'{p.get_height():.2f}',
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha='center', va='center', fontsize=10, color='black',
                       xytext=(0, 5),
                       textcoords='offset points')

# 显示图例
plt.legend(title='户型')

# 显示图表
plt.show()
