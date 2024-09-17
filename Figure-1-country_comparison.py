import pandas as pd

# 读取数据
file_path = 'j-6-11-4-country_metrics.csv'  # 替换为你的实际文件路径
data = pd.read_csv(file_path)

# 创建一个空的 DataFrame 用于存储转换后的数据
columns = ['leave_year']
countries = ['Australia', 'Brazil', 'Canada', 'China', 'Chinese Taiwan', 'France', 'Germany', 'Japan', 'Singapore',
             'South Korea', 'UK']
metrics = ['article_count_before_leave', 'article_cite_before_leave', 'h_index', 'i10_index']

# 创建列名
for country in countries:
    for metric in metrics:
        columns.append(f'{country}_{metric}')

# 创建一个空的 DataFrame
result_df = pd.DataFrame(columns=columns)

# 对每一个 leave_year 进行处理
for year in data['Leave Year'].unique():
    year_data = data[data['Leave Year'] == year]

    # 创建一行数据
    row_data = {'leave_year': year}

    # 填充每个国家和指标的值
    for country in countries:
        country_data = year_data[year_data['Country'] == country]
        for metric in metrics:
            value = country_data[metric].sum() if not country_data.empty else 0
            row_data[f'{country}_{metric}'] = value

    # 将这一行数据转换为 DataFrame
    row_df = pd.DataFrame([row_data])

    # 使用 concat 方法添加到结果 DataFrame
    result_df = pd.concat([result_df, row_df], ignore_index=True)

# 保存转换后的数据到新的 CSV 文件
output_file_path = 'j-6-11-4-country_metrics--transformed_data.csv'  # 替换为你想要保存的文件路径
result_df.to_csv(output_file_path, index=False)

print(f"数据已成功转换并保存到 {output_file_path}")
