import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# read the csv file
input_file = 'input.csv'  # please replace it with your actual file path
df = pd.read_csv(input_file, low_memory=False)

# replace '\N' as NaN
df.replace('\\N', np.nan, inplace=True)

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
    df[column] = pd.to_numeric(df[column], errors='coerce')

# The average of the experimental group and the control group in each change_year was calculated by group
grouped = df.groupby(['leave_to', 'change_year'])[columns_to_average].mean().reset_index()

# save the results to a new csv file
output_file = 'output.csv'
grouped.to_csv(output_file, index=False)
print(f"The processing is complete and the results have been saved in {output_file}")

# sets the drawing style
sns.set(style="whitegrid")

# grouped drawings
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

    #draw a chart
for pre, aft in group_pairs:
    plt.figure(figsize=(12, 6))

    # draw experimental groups
    sns.lineplot(data=grouped[grouped['leave_to'] == 1], x='change_year', y=pre, label=f'实验组 {pre}', marker='o',
                 linestyle='-', linewidth=2, color='red')
    sns.lineplot(data=grouped[grouped['leave_to'] == 1], x='change_year', y=aft, label=f'实验组 {aft}', marker='o',
                 linestyle='--', linewidth=2, color='red')

    # draw the control group
    sns.lineplot(data=grouped[grouped['leave_to'] == 0], x='change_year', y=pre, label=f'对照组 {pre}', marker='o',
                 linestyle='-', linewidth=1, color='blue')
    sns.lineplot(data=grouped[grouped['leave_to'] == 0], x='change_year', y=aft, label=f'对照组 {aft}', marker='o',
                 linestyle='--', linewidth=1, color='blue')

    plt.title(f'{pre} 和 {aft} 在各 change_year 中的表现')
    plt.xlabel('Change Year')
    plt.ylabel('mean value')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'24-3-{pre}_and_{aft}_performance.png')
    plt.show()

print(f"all charts have been generated and saved")
