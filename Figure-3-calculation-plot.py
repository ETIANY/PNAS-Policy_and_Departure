import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取CSV文件
input_file = 'input.csv'
df = pd.read_csv(input_file, low_memory=False)

# 将 '\N' 替换为 NaN
df.replace('\\N', np.nan, inplace=True)

# 解析 leave_to 列，只保留值为 '1' 的行
df['leave_to'] = df['leave_to'].astype(str).apply(lambda x: x == '1')

# 转换 leave_year 列为整数类型
df['leave_year'] = pd.to_numeric(df['leave_year'], errors='coerce')

# 过滤数据
filtered_df = df[(df['leave_to'] == True) & (df['leave_year'] >= 2000) & (df['leave_year'] <= 2023)]

# 确保所有需要计算平均值的列都是数值类型
columns_to_average = [
    'article_count_pre3', 'is_uscncoop_count_pre3', 'is_uscncoop1_count_pre3',
    'is_uscncoop2_count_pre3', 'is_uscncoop3_count_pre3', 'not_uscncoop1_count_pre3',
    'not_uscncoop2_count_pre3', 'not_uscncoop3_count_pre3', 'is_uscncoop_avgjf_pre3',
    'not_uscncoop_avgjf_pre3', 'article_count_aft3', 'is_uscncoop_count_aft3',
    'is_uscncoop1_count_aft3', 'is_uscncoop2_count_aft3', 'is_uscncoop3_count_aft3',
    'not_uscncoop1_count_aft3', 'not_uscncoop2_count_aft3', 'not_uscncoop3_count_aft3',
    'is_uscncoop_avgjf_aft3', 'not_uscncoop_avgjf_aft3'
]

for column in columns_to_average:
    filtered_df.loc[:, column] = pd.to_numeric(filtered_df[column], errors='coerce')

# 定义阶段
stages = {
    '2008-2012': (2008, 2012),
    '2013-2017': (2013, 2017),
    '2018-2022': (2018, 2022),
    '2023': (2023, 2023)
}

# 计算各阶段的年均值
stage_means = {}
for stage, (start, end) in stages.items():
    stage_means[stage] = filtered_df[(filtered_df['leave_year'] >= start) & (filtered_df['leave_year'] <= end)][columns_to_average].mean()

stage_means_df = pd.DataFrame(stage_means).transpose()
stage_means_df.index.name = 'stage'
stage_means_df.reset_index(inplace=True)

# 计算2008-2012年的基准值
baseline = stage_means_df[stage_means_df['stage'] == '2008-2012'].iloc[0]

# 计算标准化值
normalized_values = stage_means_df.copy()
for column in columns_to_average:
    normalized_values[column] = stage_means_df[column] / baseline[column]

# 保存结果到CSV文件
output_file_mean = 'output_stage_means.csv'
output_file_normalized = 'output_normalized_values.csv'
stage_means_df.to_csv(output_file_mean, index=False)
normalized_values.to_csv(output_file_normalized, index=False)
print(f"处理完成，结果已保存到 {output_file_mean} 和 {output_file_normalized}")

# 分组绘图
group_pairs = [
    ('article_count_pre3', 'article_count_aft3', 'is_uscncoop_count_pre3', 'is_uscncoop_count_aft3'),
    ('is_uscncoop1_count_pre3', 'is_uscncoop1_count_aft3', 'not_uscncoop1_count_pre3', 'not_uscncoop1_count_aft3'),
    ('is_uscncoop2_count_pre3', 'is_uscncoop2_count_aft3', 'not_uscncoop2_count_pre3', 'not_uscncoop2_count_aft3'),
    ('is_uscncoop3_count_pre3', 'is_uscncoop3_count_aft3', 'not_uscncoop3_count_pre3', 'not_uscncoop3_count_aft3'),
    ('is_uscncoop_avgjf_pre3', 'is_uscncoop_avgjf_aft3', 'not_uscncoop_avgjf_pre3', 'not_uscncoop_avgjf_aft3')
]

# 绘制平均值图表
plt.figure(figsize=(15, 30))
for i, (pre1, aft1, pre2, aft2) in enumerate(group_pairs, 1):
    plt.subplot(len(group_pairs), 1, i)
    sns.lineplot(data=stage_means_df, x='stage', y=pre1, label=pre1, marker='o', linestyle='-')
    sns.lineplot(data=stage_means_df, x='stage', y=aft1, label=aft1, marker='o', linestyle='-')
    sns.lineplot(data=stage_means_df, x='stage', y=pre2, label=pre2, marker='o', linestyle='--')
    sns.lineplot(data=stage_means_df, x='stage', y=aft2, label=aft2, marker='o', linestyle='--')
    plt.title(f'{pre1}, {aft1}, {pre2}, and {aft2} Over Stages')
    plt.xlabel('Stages')
    plt.ylabel('Average Count')
    plt.legend()

plt.tight_layout()
plt.savefig('output_mean_values_charts.png')
plt.show()
print(f"平均值图表已保存为 output_mean_values_charts.png")

# 绘制标准化值图表
plt.figure(figsize=(15, 30))
for i, (pre1, aft1, pre2, aft2) in enumerate(group_pairs, 1):
    plt.subplot(len(group_pairs), 1, i)
    sns.lineplot(data=normalized_values, x='stage', y=pre1, label=pre1, marker='o', linestyle='-')
    sns.lineplot(data=normalized_values, x='stage', y=aft1, label=aft1, marker='o', linestyle='-')
    sns.lineplot(data=normalized_values, x='stage', y=pre2, label=pre2, marker='o', linestyle='--')
    sns.lineplot(data=normalized_values, x='stage', y=aft2, label=aft2, marker='o', linestyle='--')
    plt.title(f'{pre1}, {aft1}, {pre2}, and {aft2} Normalized Over Stages')
    plt.xlabel('Stages')
    plt.ylabel('Normalized Value')
    plt.legend()

plt.tight_layout()
plt.savefig('output_normalized_values_charts.png')
plt.show()
print(f"标准化值图表已保存为 output_normalized_values_charts.png")
