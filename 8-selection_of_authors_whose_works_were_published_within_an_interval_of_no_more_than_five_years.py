import pandas as pd

# Read the CSV file (assuming the file name is 6-2_test.csv and no headers)
df = pd.read_csv('input.csv', header=None, encoding='utf-8')

# replace the null value in column 23 with 0
df[22].fillna(0, inplace=True)

# they are grouped by the first column author id
grouped = df.groupby(0)

# Create an empty DataFrame to store rows that meet the criteria
selected_rows = pd.DataFrame()

# go through each author s work
for name, group in grouped:
    # Check all the author's works have a value of 5 or less in column 23
    if (group[22] <= 5).all():
        # If so, then add all the rows of that author to the selected_rows
        selected_rows = pd.concat([selected_rows, group])

# Save the rows that match the criteria to the new file 7-2_test.csv
selected_rows.to_csv('output.csv', index=False, header=False, encoding='utf-8')