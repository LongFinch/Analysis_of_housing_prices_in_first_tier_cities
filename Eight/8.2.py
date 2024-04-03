import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

city_names = {'北京_cleaned': '北京', '上海_cleaned': '上海',
              '广州_cleaned': '广州', '深圳_cleaned': '深圳'}

# Specify the Chinese font to be used
plt.rcParams['font.sans-serif'] = ['SimHei']
sns.set(font='SimHei')

def process_directory(directory_path):
    city_data = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            city_name = city_names[os.path.splitext(filename)[0]]  # Use the filename as the city name
            city_data[city_name] = pd.read_csv(file_path, sep=',')  # Assuming the file uses a comma as the separator
    return city_data

# Read the rental data from the two directories
data_2022_directory = '../merged_data'
data_2023_directory = './2023'

data_2022_cities = process_directory(data_2022_directory)
data_2023_cities = process_directory(data_2023_directory)

# Analyze data changes
changes_summary = {}

for city, data_2022 in data_2022_cities.items():
    data_2023 = data_2023_cities.get(city, pd.DataFrame())  # Get the corresponding data for 2023, create an empty DataFrame if not available
    avg_rent_2022 = data_2022['total_price'].mean()
    avg_rent_2023 = data_2023['total_price'].mean()
    yoy_growth = ((avg_rent_2023 - avg_rent_2022) / avg_rent_2022) * 100

    changes_summary[city] = {
        '平均租金_2022': avg_rent_2022,
        '平均租金_2023': avg_rent_2023,
        '租金变化': avg_rent_2023 - avg_rent_2022,
        '同比增长': yoy_growth
    }

# Visualize data changes with smaller bars, annotations, and quiver arrows
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

for i, (city, values) in enumerate(changes_summary.items()):
    row, col = divmod(i, 2)
    bars = axes[row, col].bar(['2022', '2023'], [values['平均租金_2022'], values['平均租金_2023']], width=0.4)
    axes[row, col].set_title(f'{city}平均租金变化')
    axes[row, col].set_ylabel('元')  # Add y-axis label

    # Add annotations for each bar
    for bar, value in zip(bars, [values['平均租金_2022'], values['平均租金_2023']]):
        axes[row, col].text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                             f'{value:.2f}', ha='center', va='bottom')

    # Calculate the midpoint between the bars
    midpoint_x = (bars[0].get_x() + bars[0].get_width() + bars[1].get_x()) / 2
    midpoint_y = (bars[0].get_height() + bars[1].get_height()) / 2

    quiver_y = (midpoint_y * 0.4) if values['同比增长'] > 0 else midpoint_y * 0.6
    test = "同比增长" if values['同比增长'] > 0 else '同比下跌'

    # Add year-over-year growth annotation with quiver arrow
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

# Print summary
for city, values in changes_summary.items():
    print(f'{city}: 平均租金由{values["平均租金_2022"]}上升到{values["平均租金_2023"]}'
          f', 变化为{values["租金变化"]}, 同比增长: {values["同比增长"]:.2f}%')
