import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob

# 指定使用的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 如果你使用的是SimHei字体
sns.set(font='SimHei')  # 如果你使用的是SimHei字体

# 指定目录路径
directory_path = '../Two/cleaned_data'

# 获取目录中所有的 CSV 文件
csv_files = glob(os.path.join(directory_path, '*.csv'))

# 定义价格区间
price_bins = [0, 3000, 4500, 6000, 7500, 9000, 10500, float('inf')]
price_labels = ['0-3000', '3001-4500', '4501-6000', '6001-7500', '7501-9000', '9001-10500', '10501+']

# 存储各价格区间的district名称的列表
districts_by_price_range = []

# 遍历每个 CSV 文件
for csv_file in csv_files:
    # 读取 CSV 文件
    data = pd.read_csv(csv_file)

    # 将 'total_price' 列转换为数值类型，忽略非数值的值
    data['total_price'] = pd.to_numeric(data['total_price'], errors='coerce')

    # 进行你的数据处理
    avg_price_by_district = data.groupby('district')['total_price'].mean()

    # 划分价格区间并统计各区间的数量
    price_distribution = pd.cut(avg_price_by_district, bins=price_bins, labels=price_labels).value_counts()

    # 移除饼图中数量为0的部分
    price_distribution = price_distribution[price_distribution > 0]

    # 存储各个价格区间的district名称
    districts_in_range = []

    for label in price_distribution.index:
        try:
            lower, upper = map(int, label.split('-'))
            districts = avg_price_by_district[(avg_price_by_district >= lower) & (avg_price_by_district <= upper)].index
            districts_in_range.extend(districts)
        except ValueError:
            # 处理 '10501+' 这样的特殊情况
            districts_in_range.append(label)

    # 将当前文件的结果存储到总的列表中
    districts_by_price_range.append(districts_in_range)

    # 绘制饼状图
    if not price_distribution.empty:
        plt.figure(figsize=(12, 10))
        patches, texts, autotexts = plt.pie(price_distribution, labels=price_distribution.index, autopct='%1.1f%%', startangle=140,
                                           labeldistance=0.7, pctdistance=1.2)  # 调整pctdistance参数

        # 在饼图上添加区名
        for label, autotext in zip(price_distribution.index, autotexts):
            try:
                lower, upper = map(int, label.split('-'))
                district_names = avg_price_by_district[
                    (avg_price_by_district >= lower) & (
                                avg_price_by_district <= upper)].index

                # Group district names into rows of seven, separated by commas
                district_names_display = [', '.join(district_names[i:i + 5])
                                          for i in
                                          range(0, len(district_names), 5)]

                autotext.set_text('\n'.join(district_names_display))
                # 缩小字号
                autotext.set_fontsize(8)  # 根据需要调整数值
            except ValueError:
                # 处理 '10501+' 这样的特殊情况
                autotext.set_text(label)
        # 在饼图旁边标注板块名
        plt.title(f'各区租金价格分布 - {os.path.basename(csv_file)}')

        plt.show()

# 输出各价格区间的district名称的列表
print(districts_by_price_range)
