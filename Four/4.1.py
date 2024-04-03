import pandas as pd
import os

# 指定CSV文件所在的目录
directory_path = '../Two/cleaned_data'

# 获取目录下的所有CSV文件
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
conversion_table = {'北京_cleaned.csv': '北京', '上海_cleaned.csv': '上海', '广州_cleaned.csv': '广州', '深圳_cleaned.csv': '深圳', '惠州_cleaned.csv': '惠州'}

# 遍历每个CSV文件
for csv_file in csv_files:
    # 构建CSV文件的完整路径
    file_path = os.path.join(directory_path, csv_file)
    city_name = conversion_table[csv_file]
    # 读取数据
    df = pd.read_csv(file_path)

    # 分别筛选室为1、2、3的数据
    df_1_room = df[df['室'] == 1]
    df_2_room = df[df['室'] == 2]
    df_3_room = df[df['室'] == 3]

    # 计算均价、最低价、最高价和中位数
    avg_price_1_room = df_1_room['total_price'].mean()
    min_price_1_room = df_1_room['total_price'].min()
    max_price_1_room = df_1_room['total_price'].max()
    median_price_1_room = df_1_room['total_price'].median()

    avg_price_2_room = df_2_room['total_price'].mean()
    min_price_2_room = df_2_room['total_price'].min()
    max_price_2_room = df_2_room['total_price'].max()
    median_price_2_room = df_2_room['total_price'].median()

    avg_price_3_room = df_3_room['total_price'].mean()
    min_price_3_room = df_3_room['total_price'].min()
    max_price_3_room = df_3_room['total_price'].max()
    median_price_3_room = df_3_room['total_price'].median()

    # 打印结果
    print(f"城市：{city_name}")
    print("一居室的统计信息：")
    print(f"均价：{avg_price_1_room}")
    print(f"最低价：{min_price_1_room}")
    print(f"最高价：{max_price_1_room}")
    print(f"中位数：{median_price_1_room}")


    print("二居室的统计信息：")
    print(f"均价：{avg_price_2_room}")
    print(f"最低价：{min_price_2_room}")
    print(f"最高价：{max_price_2_room}")
    print(f"中位数：{median_price_2_room}")

    print("三居室的统计信息：")
    print(f"均价：{avg_price_3_room}")
    print(f"最低价：{min_price_3_room}")
    print(f"最高价：{max_price_3_room}")
    print(f"中位数：{median_price_3_room}")
    print("\n")
