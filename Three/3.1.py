import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# 指定使用的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
sns.set(font='SimHei')

# 指定CSV文件所在的目录
directory_path = '../Two/cleaned_data'

# 获取目录下的所有CSV文件
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
conversion_table = {'北京_cleaned': '北京', '上海_cleaned': '上海', '广州_cleaned': '广州', '深圳_cleaned': '深圳', '惠州_cleaned': '惠州'}

# 创建空字典，用于存储各城市的平均租金数据
city_avg_prices = {}

for csv_file in csv_files:
    # 构建CSV文件的完整路径
    file_path = os.path.join(directory_path, csv_file)

    # 将CSV文件读取到pandas DataFrame中，指定逗号为分隔符
    df = pd.read_csv(file_path, delimiter=',')

    # 从文件名中提取城市名称
    city_name = conversion_table[csv_file.split('.')[0]]

    # 计算平均租金
    avg_price = df['total_price'].mean()

    # 存储到字典中
    city_avg_prices[city_name] = avg_price

# 将字典转换为DataFrame
avg_prices_df = pd.DataFrame(list(city_avg_prices.items()), columns=['City', 'Average Rent'])

# 画图展示不同城市的平均租金
plt.figure(figsize=(10, 6))
bars = plt.bar(avg_prices_df['City'], avg_prices_df['Average Rent'], color='skyblue')
plt.xlabel('城市')
plt.ylabel('平均租金(元)')
plt.title('不同城市的平均租金')
plt.xticks(rotation=0, ha='right')

# 在每个柱形的顶部添加数字标签
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

plt.show()
