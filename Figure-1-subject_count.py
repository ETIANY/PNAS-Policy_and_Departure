import pandas as pd
import matplotlib.pyplot as plt

# read the csv file
df = pd.read_csv('input.csv')

# 1. filter out Senior author
senior_df = df[df['article_count_before_leave'] >= 148]


# 2. Number of unique author_id in each leave_year with subject=1/2/3/4
subject_map = {1: 'Engineering and Computer Science',
               2: 'Life Science',
               3: 'Mathematics and Physical Science',
               4: 'Social Sciences and Others'}

subject_count = senior_df[senior_df['subject'].isin(subject_map.keys())]
subject_count = subject_count.groupby(['leave_year', 'subject'])['author_id'].nunique().reset_index()
subject_count['subject'] = subject_count['subject'].map(subject_map)

# write to a csv file
subject_count.to_csv('subject_count-senior.csv', index=False)

# Plot
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

# 3. The number of unduplicated author_id in each leave_year where leave_to=1 and leave_to are not equal to 1 and are not equal to 0
def map_leave_to(value):
    if value in [1]:
        return 'China'
    elif value not in [0, 1, 18, 28] and pd.notna(value):
        return 'Other'
    else:
        return None

# print unique leave_to values for debugging
print("Unique leave_to values before mapping:", senior_df['leave_to'].unique())

# filter and map leave_to
leave_to_count = senior_df[senior_df['leave_to'].notna()]
leave_to_count['leave_to'] = leave_to_count['leave_to'].map(map_leave_to)
leave_to_count = leave_to_count.dropna(subset=['leave_to'])

# Count the number of unique author_id for leave_to categories in each leave_year
leave_to_count = leave_to_count.groupby(['leave_year', 'leave_to'])['author_id'].nunique().reset_index()

# write to a csv file
leave_to_count.to_csv('leave_to_count_senior.csv', index=False)

# plot
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
