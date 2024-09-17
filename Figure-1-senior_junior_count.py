import pandas as pd

# 读取CSV文件
df = pd.read_csv('input.csv')

# 1. 过滤出 article_count_before_leave 小于等于 185 且 leave_to 为 1 的行
filtered_df = df[(df['article_count_before_leave'] <= 185) & (df['leave_to'] == 1)]

# 2. 计算筛选后 article_count_before_leave 的 97% 分位数
percentile_97 = filtered_df['article_count_before_leave'].quantile(0.97)
print(percentile_97)

# 3. 判断 article_count_before_leave 是否符合 97% 分位数以上的条件
filtered_df['is_above_97th'] = filtered_df['article_count_before_leave'] >= percentile_97

# 4. 统计每个 leave_year 中符合条件的唯一 author_id 数量，并按 subject 进行分组统计
result = filtered_df[filtered_df['is_above_97th']].groupby(['leave_year', 'subject'])['author_id'].nunique().unstack(fill_value=0)

# 为了更好地处理缺失的 subject 列，我们确保所有 subject（1/2/3/4）都在结果中
result = result.reindex(columns=[1, 2, 3, 4], fill_value=0)

# 计算每年符合条件的唯一 author_id 总数
unique_author_count = filtered_df[filtered_df['is_above_97th']].groupby('leave_year')['author_id'].nunique()

# 合并数据
result['unique_author_count'] = unique_author_count
result = result.reset_index()
result.columns = ['leave_year', 'subject1_count', 'subject2_count', 'subject3_count', 'subject4_count', 'unique_author_count']

# 写入 CSV 文件
result.to_csv('Figure-1-senior_count.csv', index=False)

# 5. 计算 junior=1 且 all_cnus=1 且 leave_to=1 的 author_id 数量
junior_filtered_df = df[(df['junior'] == 1) & (df['all_cnus'] == 1) & (df['leave_to'] == 1)]

# 统计每个 leave_year 中符合条件的唯一 author_id 数量，并按 subject 进行分组统计
junior_result = junior_filtered_df.groupby(['leave_year', 'subject'])['author_id'].nunique().unstack(fill_value=0)

# 确保所有 subject 列存在
junior_result = junior_result.reindex(columns=[1, 2, 3, 4], fill_value=0)

# 计算每年符合条件的唯一 author_id 总数
junior_unique_author_count = junior_filtered_df.groupby('leave_year')['author_id'].nunique()

# 合并数据
junior_result['unique_author_count'] = junior_unique_author_count
junior_result = junior_result.reset_index()
junior_result.columns = ['leave_year', 'subject1_count', 'subject2_count', 'subject3_count', 'subject4_count', 'unique_author_count']

# 保存到 CSV 文件
junior_result.to_csv('Figure-1-junior_count.csv', index=False)
