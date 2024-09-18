import pandas as pd

# read the csv file
df = pd.read_csv('input.csv')

# 1. Filter out rows with article_count_before_leave less than or equal to 185 and a leave_to of 1
filtered_df = df[(df['article_count_before_leave'] <= 185) & (df['leave_to'] == 1)]

# 2. The 97th percentile of article_count_before_leave after screening was calculated
percentile_97 = filtered_df['article_count_before_leave'].quantile(0.97)
print(percentile_97)

# 3. Determine if article_count_before_leave meets the criteria above the 97th percentile
filtered_df['is_above_97th'] = filtered_df['article_count_before_leave'] >= percentile_97

# 4. Count the number of unique author_id that meet the requirements in each leave_year, and group them by subject
result = filtered_df[filtered_df['is_above_97th']].groupby(['leave_year', 'subject'])['author_id'].nunique().unstack(fill_value=0)

# To better handle the missing subject columns, we make sure that all subjects (1/2/3/4) are in the results
result = result.reindex(columns=[1, 2, 3, 4], fill_value=0)

# Calculate the total number of eligible unique author_id per year
unique_author_count = filtered_df[filtered_df['is_above_97th']].groupby('leave_year')['author_id'].nunique()

# merge data
result['unique_author_count'] = unique_author_count
result = result.reset_index()
result.columns = ['leave_year', 'subject1_count', 'subject2_count', 'subject3_count', 'subject4_count', 'unique_author_count']

# write to a csv file
result.to_csv('Figure-1-senior_count.csv', index=False)

# 5. Calculate the number of author_id with junior=1 and all_cnus=1 and leave_to=1
junior_filtered_df = df[(df['junior'] == 1) & (df['all_cnus'] == 1) & (df['leave_to'] == 1)]

# Count the number of unique author_id that meet the requirements in each leave_year, and group them by subject
junior_result = junior_filtered_df.groupby(['leave_year', 'subject'])['author_id'].nunique().unstack(fill_value=0)

# make sure all subject columns exist
junior_result = junior_result.reindex(columns=[1, 2, 3, 4], fill_value=0)

# Calculate the total number of eligible unique author_id per year
junior_unique_author_count = junior_filtered_df.groupby('leave_year')['author_id'].nunique()

# merge data
junior_result['unique_author_count'] = junior_unique_author_count
junior_result = junior_result.reset_index()
junior_result.columns = ['leave_year', 'subject1_count', 'subject2_count', 'subject3_count', 'subject4_count', 'unique_author_count']

# save to a csv file
junior_result.to_csv('Figure-1-junior_count.csv', index=False)
