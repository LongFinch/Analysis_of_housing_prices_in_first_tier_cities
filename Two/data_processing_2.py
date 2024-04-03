import pandas as pd
import os

# 指定CSV文件所在的目录
directory_path = '.\merged_data'

# 获取目录下的所有CSV文件
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
conversion_table = {'merged_bj': '北京', 'merged_sh': '上海', 'merged_gz': '广州', 'merged_sz': '深圳', 'merged_hui': '惠州'}

for csv_file in csv_files:
    # 构建CSV文件的完整路径
    file_path = os.path.join(directory_path, csv_file)
    print(file_path)
    # 将CSV文件读取到pandas DataFrame中，指定逗号为分隔符
    df = pd.read_csv(file_path, delimiter=',')

    # 计算统计信息
    avg_price = df['price_per_m2'].mean()
    print(avg_price)
    std_dev_price = df['price_per_m2'].std()

    # 数据清洗：删除租金超过均价两倍标准差的数据
    cleaned_df = df[abs(df['price_per_m2'] - avg_price) <= 2 * std_dev_price]

    # 从文件名中提取城市名称
    city_name = conversion_table[csv_file.split('.')[0]]

    # 计算删除的数据数量
    deleted_rows = len(df) - len(cleaned_df)

    # 打印删除的数据数量
    print(f"{city_name}删除的数据行数：{deleted_rows}")

    # 打印清洗前后的数据行数
    print(f"{city_name}数据清洗前数据行数：{len(df)}")
    print(f"{city_name}数据清洗后数据行数：{len(cleaned_df)}")

    # 计算清洗后的统计信息
    cleaned_avg_price = cleaned_df['total_price'].mean()
    cleaned_max_price = cleaned_df['total_price'].max()
    cleaned_min_price = cleaned_df['total_price'].min()
    cleaned_median_price = cleaned_df['total_price'].median()

    cleaned_avg_price_per_area = cleaned_df['price_per_m2']
    cleaned_avg_price_per_area_mean = cleaned_avg_price_per_area.mean()
    cleaned_avg_price_per_area_max = cleaned_avg_price_per_area.max()
    cleaned_avg_price_per_area_min = cleaned_avg_price_per_area.min()
    cleaned_avg_price_per_area_median = cleaned_avg_price_per_area.median()

    # 打印清洗后的统计结果
    print(f"{city_name}清洗后的统计信息：")
    print(f"平均租金：{cleaned_avg_price}")
    print(f"最高租金：{cleaned_max_price}")
    print(f"最低租金：{cleaned_min_price}")
    print(f"中位数租金：{cleaned_median_price}")

    print(f"单位面积租金均价：{cleaned_avg_price_per_area_mean}")
    print(f"单位面积租金最高价：{cleaned_avg_price_per_area_max}")
    print(f"单位面积租金最低价：{cleaned_avg_price_per_area_min}")
    print(f"单位面积租金中位数：{cleaned_avg_price_per_area_median}")

    # 将清洗后的数据保存为新的CSV文件
    cleaned_df.to_csv(os.path.join('./cleaned_data',
                                   f'{city_name}_cleaned.csv'), index=False)

