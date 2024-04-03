import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 指定使用的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
sns.set(font='SimHei')

# 指定包含CSV文件的目录路径
directory_path = '../Two/cleaned_data/'

# 获取目录下所有CSV文件的文件名
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# 循环处理每个CSV文件
for csv_file in csv_files:
    # 拼接完整文件路径
    file_path = os.path.join(directory_path, csv_file)

    # 读取CSV文件
    data = pd.read_csv(file_path)

    # 按district计算均价
    average_prices_district = data.groupby('district')['total_price'].mean().reset_index()

    # 手动指定价格区间的起始和结束值
    price_ranges = [(0, 1500), (1500, 4500), (4500, 9000), (9000, 15000), (15000, float('inf'))]

    # 生成label和size列表
    labels = []
    size_counts = []

    for price_range in price_ranges:
        start_price, end_price = price_range
        mask = (average_prices_district['total_price'] >= start_price) & (average_prices_district['total_price'] < end_price)
        districts_in_interval = average_prices_district.loc[mask, 'district'].tolist()

        if districts_in_interval:
            formatted_districts = [f"{district}\n" if (i + 1) % 6 == 0 else district for i, district in enumerate(districts_in_interval)]
            labels.append(f"{start_price}~{end_price - 1}区间：{' '.join(formatted_districts)}")
            size_counts.append(len(districts_in_interval))

    # 绘制饼状图
    plt.pie(size_counts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # 移动标题到上方
    plt.title(f"Pie Chart for {csv_file}", y=1.08)
    # 调整标签的字号
    plt.show()
