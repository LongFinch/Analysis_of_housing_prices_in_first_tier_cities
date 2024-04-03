import pandas as pd

# 读取数据
df = pd.read_csv('.\cleaned_data\广州_cleaned.csv')

# 删除price_per_m2小于3的表项
df_cleaned = df[df['price_per_m2'] >= 6]

# 打印删除前后的数据行数
print(f"数据清洗前数据行数：{len(df)}")
print(f"数据清洗后数据行数：{len(df_cleaned)}")

# 打印清洗后的数据
print(df_cleaned)

# 将清洗后的数据保存为新的CSV文件
df_cleaned.to_csv('广州_cleaned.csv', index=False)
