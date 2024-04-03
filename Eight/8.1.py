import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 城市名称映射
city_names = {'北京_cleaned': '北京', '上海_cleaned': '上海',
              '广州_cleaned': '广州', '深圳_cleaned': '深圳'}

# 指定中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
sns.set(font='SimHei')

def process_directory(directory_path):
    city_data = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            city_name = city_names[os.path.splitext(filename)[0]]  # 使用文件名作为城市名称
            city_data[city_name] = pd.read_csv(file_path, sep=',')  # 假设文件使用逗号作为分隔符
    return city_data

# 读取两个目录中的租赁数据
data_2022_directory = '../merged_data'
data_2023_directory = './2023'

data_2022_cities = process_directory(data_2022_directory)
data_2023_cities = process_directory(data_2023_directory)

# 分析数据变化
changes_summary = {}

for city, data_2022 in data_2022_cities.items():
    data_2023 = data_2023_cities.get(city, pd.DataFrame())  # 获取对应的2023年数据，如果没有则创建一个空的DataFrame
    avg_rent_2022 = data_2022['price_per_m2'].mean()
    avg_rent_2023 = data_2023['price_per_m2'].mean()
    yoy_growth = ((avg_rent_2023 - avg_rent_2022) / avg_rent_2022) * 100

    changes_summary[city] = {
        '平均租金_2022': avg_rent_2022,
        '平均租金_2023': avg_rent_2023,
        '租金变化': avg_rent_2023 - avg_rent_2022,
        '同比增长': yoy_growth
    }

# 用较小的柱形、注释和矢量箭头可视化数据变化
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

for i, (city, values) in enumerate(changes_summary.items()):
    row, col = divmod(i, 2)
    bars = axes[row, col].bar(['2022', '2023'], [values['平均租金_2022'], values['平均租金_2023']], width=0.4)
    axes[row, col].set_title(f'{city}单位面积平均租金变化')
    axes[row, col].set_ylabel('元/平米')  # 添加y轴标签

    # 为每个柱形添加注释
    for bar, value in zip(bars, [values['平均租金_2022'], values['平均租金_2023']]):
        axes[row, col].text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                             f'{value:.2f}', ha='center', va='bottom')

    # 计算两个柱形之间的中点
    midpoint_x = (bars[0].get_x() + bars[0].get_width() + bars[1].get_x()) / 2
    midpoint_y = (bars[0].get_height() + bars[1].get_height()) / 2

    quiver_y = (midpoint_y * 0.4) if values['同比增长'] > 0 else midpoint_y * 0.6
    test = "同比增长" if values['同比增长'] > 0 else '同比下跌'

    # 添加同比增长注释和矢量箭头
    arrow_direction = (1, midpoint_y / 2) if values['同比增长'] > 0 \
        else (1, -midpoint_y / 2)
    values['更改值'] = abs(values['同比增长'])
    axes[row, col].text(midpoint_x, midpoint_y * 0.7, f'{test}: {values["更改值"]:.2f}%', ha='center', va='center')
    axes[row, col].quiver(midpoint_x-0.2 , quiver_y, arrow_direction[0],
                          arrow_direction[1], angles='xy',
                          scale_units='xy',scale=3,
                          color='green' if values['同比增长'] > 0 else 'red'
                          )

plt.tight_layout()
plt.show()
