import pandas as pd

# Read a CSV file (assuming the file name is 5_all_8.csv and no headers)
df = pd.read_csv('4-按年份排序authorid_year_chiname1_chiname3_countag.csv', header=None, encoding='utf-8')

# Sort by column 1 (author ID) and column 8 (year of publication).
df_sorted = df.sort_values(by=[0, 1])

# Calculate the difference in years between adjacent works
df_sorted['年份差'] = df_sorted.groupby(0)[1].diff()

# write the results to column 8
df_sorted[7] = df_sorted['年份差']

# write the results to a new file
df_sorted.to_csv('5-8列year-difference.csv', index=False, header=False, encoding='utf-8')