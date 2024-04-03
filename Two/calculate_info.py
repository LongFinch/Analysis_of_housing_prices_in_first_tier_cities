import pandas as pd
import os

# 指定CSV文件所在的目录
directory_path = '.\cleaned_data'

# 获取目录下的所有CSV文件
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
conversion_table = {'北京_cleaned': '北京', '上海_cleaned': '上海', '广州_cleaned': '广州', '深圳_cleaned': '深圳', '惠州_cleaned': '惠州'}

for csv_file in csv_files:
    # 构建CSV文件的完整路径
    file_path = os.path.join(directory_path, csv_file)

    # 将CSV文件读取到pandas DataFrame中，指定逗号为分隔符
    df = pd.read_csv(file_path, delimiter=',')
    # 从文件名中提取城市名称
    city_name = conversion_table[csv_file.split('.')[0]]

    # 计算统计信息
    avg_price = df['total_price'].mean()
    max_price = df['total_price'].max()
    min_price = df['total_price'].min()
    median_price = df['total_price'].median()

    avg_price_per_area = df['price_per_m2']
    avg_price_per_area_mean = avg_price_per_area.mean()
    avg_price_per_area_max = avg_price_per_area.max()
    avg_price_per_area_min = avg_price_per_area.min()
    avg_price_per_area_median = avg_price_per_area.median()

    # 打印结果
    print(f"\n{city_name}的统计信息：")
    print(f"平均租金：{avg_price}")
    print(f"最高租金：{max_price}")
    print(f"最低租金：{min_price}")
    print(f"中位数租金：{median_price}")

    print(f"单位面积租金均价：{avg_price_per_area_mean}")
    print(f"单位面积租金最高价：{avg_price_per_area_max}")
    print(f"单位面积租金最低价：{avg_price_per_area_min}")
    print(f"单位面积租金中位数：{avg_price_per_area_median}")
