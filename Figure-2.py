import pandas as pd

# 读取数据到数据框 df 中
df = pd.read_csv('@0811-2-trimmed-2000-2023-095-output.csv')

# 定义要分析的列
columns_to_analyze = [
    'article_count_before_leave', 'position1_count', 'position2_count',
    'position3_count', 'article_cite_before_leave', 'articlely_cite_before_leave',
    'articlely_jif_before_leave', 'h_index'
]

# 定义学科映射字典
subject_mapping = {
    1: 'Engineering and Computer Science',
    2: 'Life Science',
    3: 'Mathematics and Physical Science',
    4: 'Social Sciences and Others'
}

# 替换学科编号为名称
df['subject'] = df['subject'].map(subject_mapping)

# 将 'leave_year' 转换为字符串
df['leave_year'] = df['leave_year'].astype(str)

# 计算2008-2012年的标准值
standard_years = ['2008', '2009', '2010', '2011', '2012']
standard_values = {}

for col in columns_to_analyze:
    avg_data = df.groupby(['subject', 'leave_year'])[col].mean().unstack(fill_value=0)

    # 计算2008-2012年的平均值作为标准值
    if all(year in avg_data.columns for year in standard_years):
        standard_values[col] = avg_data[standard_years].mean(axis=1)
    else:
        print(f"Cannot calculate standard values for {col} because some standard_years are missing in columns.")

# 标准化其他年份的数据
standardized_data = {col: pd.DataFrame() for col in columns_to_analyze}

for col in columns_to_analyze:
    avg_data = df.groupby(['subject', 'leave_year'])[col].mean().unstack(fill_value=0)

    # 确保标准值存在
    if col in standard_values:
        # 定义标准化阶段
        periods = {
            '2008-2012': ['2008', '2009', '2010', '2011', '2012'],
            '2013-2017': ['2013', '2014', '2015', '2016', '2017'],
            '2018-2022': ['2018', '2019', '2020', '2021', '2022'],
            '2023': ['2023']
        }

        # 创建一个新的 DataFrame 来存储标准化后的数据
        standardized_df = pd.DataFrame(index=avg_data.index, columns=periods.keys())

        # 对每个阶段进行标准化处理
        for period, years in periods.items():
            # 计算该阶段的均值
            if any(year in avg_data.columns for year in years):
                period_mean = avg_data[years].mean(axis=1)
                # 标准化
                standardized_df[period] = period_mean / standard_values[col]

        # 保存标准化后的数据到 CSV 文件
        file_name = f'0811-3-095-{col}__standardized_extended.csv'
        standardized_df.to_csv(file_name, header=True)
        print(f"Standardized data for {col} saved to {file_name}")
    else:
        print(f"Standard values not found for {col}.")

print("Standardization process completed.")
