import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 指定使用的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 如果你使用的是SimHei字体
sns.set(font='SimHei')  # 如果你使用的是SimHei字体

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

    # 定义价格区间的步长
    interval_step = 3000

    # 生成label和size列表
    labels = []
    size_counts = []

    for start_price in range(0, int(average_prices_district['total_price'].max()) + interval_step, interval_step):
        end_price = start_price + interval_step
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
    plt.title(f"Pie Chart for {csv_file}", y=1.08)  # 调整y的值来控制标题的垂直位置
    # 调整标签的字号
    plt.show()
