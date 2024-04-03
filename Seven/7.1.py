import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 指定使用的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
sns.set(font='SimHei')

# 指定包含CSV文件的目录路径
directory_path = '../Two/cleaned_data/'

# 获取目录下所有CSV文件的文件名
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
city_names = {'北京_cleaned': '北京', '上海_cleaned': '上海', '广州_cleaned': '广州',
              '深圳_cleaned': '深圳', '惠州_cleaned': '惠州'}

# 存储每个城市的平均每平米租金
avg_price_per_m2 = {}

# 存储每个城市的总价和每平米租金的数据点
all_data_points = pd.DataFrame(columns=['total_price', 'price_per_m2', 'city'])

# 循环处理每个CSV文件
for csv_file in csv_files:
    # 拼接完整文件路径
    file_path = os.path.join(directory_path, csv_file)

    # 读取CSV文件
    data = pd.read_csv(file_path, delimiter=',')

    # 存储每个城市的平均每平米租金
    avg_price_per_m2[city_names[csv_file.split('.')[0]]] = data['price_per_m2'].mean()

    # 添加城市信息列
    data['city'] = city_names[csv_file.split('.')[0]]

    # 将数据点添加到总数据集
    all_data_points = pd.concat([all_data_points, data[['total_price', 'price_per_m2', 'city']]])



# 工资数据
average_wage = {'北京': 17414.75, '上海': 17706.33, '广州': 12693.67, '深圳': 13729.50, '惠州': 8158.33}

# 将数据转换为DataFrame
df = pd.DataFrame(list(avg_price_per_m2.items()), columns=['City', 'Avg_Price_Per_M2'])
df['Average_Wage'] = df['City'].map(average_wage)

# 计算每个城市的平均每平米租金和平均工资的均值
avg_price_per_m2_mean = df['Avg_Price_Per_M2'].mean()
average_wage_mean = df['Average_Wage'].mean()

# 计算avg_slope
avg_slope = average_wage_mean / avg_price_per_m2_mean

# 绘制拟合线
x_range = np.linspace(df['Avg_Price_Per_M2'].min(), df['Avg_Price_Per_M2'].max(), 100)
y_range = avg_slope * x_range

# 绘制散点图，交换横轴和纵轴坐标
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Avg_Price_Per_M2', y='Average_Wage', hue='City', s=100)
plt.title('工资与单位面积租金的关系')
plt.xlabel('平均每平米租金')
plt.ylabel('平均工资')

for index, row in df.iterrows():
    x_offset = 1  # 水平方向的偏移量

    # 根据城市类型设置不同的垂直方向偏移量
    if row['City'] == '北京':
        y_offset = 1000
    elif row['City'] == '上海':
        y_offset = -1000
    else:
        y_offset = 0

    # 遍历每个城市，标记坐标和y/x值
    plt.text(row['Avg_Price_Per_M2'] + x_offset,
             row['Average_Wage'] + y_offset,
             f"{row['City']} ({row['Avg_Price_Per_M2']:.2f}, {row['Average_Wage']:.2f})"
             f"\n工资与租金比值: {row['Average_Wage']/row['Avg_Price_Per_M2']:.2f}")


plt.plot(x_range, y_range, label=f'工资/每平米租金均值: {avg_slope:.2f}', linestyle='--', color='black')

plt.legend(title='城市')
plt.show()
