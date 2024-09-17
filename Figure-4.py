import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取CSV文件
input_file = 'input.csv'  # 请替换为你的实际文件路径
df = pd.read_csv(input_file, low_memory=False)

# 将 '\N' 替换为 NaN
df.replace('\\N', np.nan, inplace=True)

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
    df[column] = pd.to_numeric(df[column], errors='coerce')

# 分组计算实验组和对照组在各change_year中的平均值
grouped = df.groupby(['leave_to', 'change_year'])[columns_to_average].mean().reset_index()

# 将结果保存到新的CSV文件中
output_file = 'output.csv'
grouped.to_csv(output_file, index=False)
print(f"处理完成，结果已保存到 {output_file}")

# 设置绘图风格
sns.set(style="whitegrid")

# 分组绘图
group_pairs = [
    ('article_count_pre3', 'article_count_aft3'),
    ('is_uscncoop_count_pre3', 'is_uscncoop_count_aft3'),
    ('is_uscncoop1_count_pre3', 'is_uscncoop1_count_aft3'),
    ('is_uscncoop2_count_pre3', 'is_uscncoop2_count_aft3'),
    ('is_uscncoop3_count_pre3', 'is_uscncoop3_count_aft3'),
    ('not_uscncoop1_count_pre3', 'not_uscncoop1_count_aft3'),
    ('not_uscncoop2_count_pre3', 'not_uscncoop2_count_aft3'),
    ('not_uscncoop3_count_pre3', 'not_uscncoop3_count_aft3'),
    ('is_uscncoop_avgjf_pre3', 'is_uscncoop_avgjf_aft3'),
    ('not_uscncoop_avgjf_pre3', 'not_uscncoop_avgjf_aft3')
]

# 绘制图表
for pre, aft in group_pairs:
    plt.figure(figsize=(12, 6))

    # 绘制实验组
    sns.lineplot(data=grouped[grouped['leave_to'] == 1], x='change_year', y=pre, label=f'实验组 {pre}', marker='o',
                 linestyle='-', linewidth=2, color='red')
    sns.lineplot(data=grouped[grouped['leave_to'] == 1], x='change_year', y=aft, label=f'实验组 {aft}', marker='o',
                 linestyle='--', linewidth=2, color='red')

    # 绘制对照组
    sns.lineplot(data=grouped[grouped['leave_to'] == 0], x='change_year', y=pre, label=f'对照组 {pre}', marker='o',
                 linestyle='-', linewidth=1, color='blue')
    sns.lineplot(data=grouped[grouped['leave_to'] == 0], x='change_year', y=aft, label=f'对照组 {aft}', marker='o',
                 linestyle='--', linewidth=1, color='blue')

    plt.title(f'{pre} 和 {aft} 在各 change_year 中的表现')
    plt.xlabel('Change Year')
    plt.ylabel('平均值')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'24-3-{pre}_and_{aft}_performance.png')
    plt.show()

print(f"所有图表已生成并保存。")
