import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv('@0811-2-trimmed-2000-2023-095-output.csv')

# 1. 筛选出 senior 作者
senior_df = df[df['article_count_before_leave'] >= 148]


# 2. 每个 leave_year 中 subject=1/2/3/4 的不重复 author_id 数量
subject_map = {1: 'Engineering and Computer Science',
               2: 'Life Science',
               3: 'Mathematics and Physical Science',
               4: 'Social Sciences and Others'}

subject_count = senior_df[senior_df['subject'].isin(subject_map.keys())]
subject_count = subject_count.groupby(['leave_year', 'subject'])['author_id'].nunique().reset_index()
subject_count['subject'] = subject_count['subject'].map(subject_map)

# 写入 CSV 文件
subject_count.to_csv('subject_count-senior.csv', index=False)

# 绘图
plt.figure(figsize=(12, 8))
for subject in subject_map.values():
    subset = subject_count[subject_count['subject'] == subject]
    plt.plot(subset['leave_year'], subset['author_id'], marker='o', label=subject)

plt.xlabel('Leave Year')
plt.ylabel('Unique senior Author Count')
plt.title('Unique senior Author Count by Subject and Leave Year')
plt.legend()
plt.grid(True)
plt.savefig('subject_count_senior.png')
plt.show()

# 3. 每个 leave_year 中 leave_to=1 和 leave_to 不等于1且不等于0 的不重复 author_id 数量
def map_leave_to(value):
    if value in [1 , 28]:
        return 'China'
    elif value not in [0, 1, 18, 28] and pd.notna(value):
        return 'Other'
    else:
        return None

# 打印唯一 leave_to 值以进行调试
print("Unique leave_to values before mapping:", senior_df['leave_to'].unique())

# 过滤并映射 leave_to
leave_to_count = senior_df[senior_df['leave_to'].notna()]
leave_to_count['leave_to'] = leave_to_count['leave_to'].map(map_leave_to)
leave_to_count = leave_to_count.dropna(subset=['leave_to'])

# 统计每个 leave_year 中 leave_to 分类的唯一 author_id 数量
leave_to_count = leave_to_count.groupby(['leave_year', 'leave_to'])['author_id'].nunique().reset_index()

# 写入 CSV 文件
leave_to_count.to_csv('leave_to_count_senior.csv', index=False)

# 绘图
plt.figure(figsize=(12, 8))
for leave_to in leave_to_count['leave_to'].unique():
    subset = leave_to_count[leave_to_count['leave_to'] == leave_to]
    plt.plot(subset['leave_year'], subset['author_id'], marker='o', label=leave_to)

plt.xlabel('Leave Year')
plt.ylabel('Unique senior Author Count')
plt.title('Unique senior Author Count by Leave To and Leave Year')
plt.legend()
plt.grid(True)
plt.savefig('leave_to_count_senior.png')
plt.show()
