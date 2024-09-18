import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# read the csv file
input_file = 'input.csv'
df = pd.read_csv(input_file, low_memory=False)

# replace '\N' as NaN
df.replace('\\N', np.nan, inplace=True)

# Parse the leave_to column, keeping only the rows with a value of '1'
df['leave_to'] = df['leave_to'].astype(str).apply(lambda x: x == '1')

# convert leave_year column to an integer type
df['leave_year'] = pd.to_numeric(df['leave_year'], errors='coerce')

# filter the data
filtered_df = df[(df['leave_to'] == True) & (df['leave_year'] >= 2000) & (df['leave_year'] <= 2023)]

# Make sure that all the columns that need to be averaged are of the numeric type
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

# define the stage
stages = {
    '2008-2012': (2008, 2012),
    '2013-2017': (2013, 2017),
    '2018-2022': (2018, 2022),
    '2023': (2023, 2023)
}

# calculate the annual average for each period
stage_means = {}
for stage, (start, end) in stages.items():
    stage_means[stage] = filtered_df[(filtered_df['leave_year'] >= start) & (filtered_df['leave_year'] <= end)][columns_to_average].mean()

stage_means_df = pd.DataFrame(stage_means).transpose()
stage_means_df.index.name = 'stage'
stage_means_df.reset_index(inplace=True)

# baseline values for 2008 2012 were calculated
baseline = stage_means_df[stage_means_df['stage'] == '2008-2012'].iloc[0]

# normalized values are calculated
normalized_values = stage_means_df.copy()
for column in columns_to_average:
    normalized_values[column] = stage_means_df[column] / baseline[column]

# save the results to a csv file
output_file_mean = 'output_stage_means.csv'
output_file_normalized = 'output_normalized_values.csv'
stage_means_df.to_csv(output_file_mean, index=False)
normalized_values.to_csv(output_file_normalized, index=False)
print(f"results are in {output_file_mean} and {output_file_normalized}")

# grouped drawings
group_pairs = [
    ('article_count_pre3', 'article_count_aft3', 'is_uscncoop_count_pre3', 'is_uscncoop_count_aft3'),
    ('is_uscncoop1_count_pre3', 'is_uscncoop1_count_aft3', 'not_uscncoop1_count_pre3', 'not_uscncoop1_count_aft3'),
    ('is_uscncoop2_count_pre3', 'is_uscncoop2_count_aft3', 'not_uscncoop2_count_pre3', 'not_uscncoop2_count_aft3'),
    ('is_uscncoop3_count_pre3', 'is_uscncoop3_count_aft3', 'not_uscncoop3_count_pre3', 'not_uscncoop3_count_aft3'),
    ('is_uscncoop_avgjf_pre3', 'is_uscncoop_avgjf_aft3', 'not_uscncoop_avgjf_pre3', 'not_uscncoop_avgjf_aft3')
]

# plot a chart of averages
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
print(f"figure is in output_mean_values_charts.png")

# chart normalized values
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
print(f"figure is in output_normalized_values_charts.png")
