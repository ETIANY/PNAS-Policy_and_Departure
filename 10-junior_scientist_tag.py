import pandas as pd

# read the csv file
df = pd.read_csv('input.csv', header=None)


# define functions to make judgments
def process_group(group):
    # the initialization flag is listed as 0
    group[31] = 0

    # get the year for the first row
    n = group.iloc[0, 7]

    # find all 26 rows with column 1
    rows_with_one = group[(group[25] == 1) & (group[24] != 0)]

    for index, row in rows_with_one.iterrows():
        # get the year for column 30
        m_values = group[group[29].notna()][29].tolist()

        # Find all rows with m-n less than or equal to 5 and column 15 'CN'
        valid_rows = group[(group[29] - n <= 5) & (group[14] == 'CN')]

        # find the year for 25 columns
        x = row[24]

        # If there are rows that meet the criteria, and the year minus n in 25 columns is less than or equal to 7
        if not valid_rows.empty and x - n <= 7:
            # label 31 columns as 1
            group.at[index, 31] = 1

    return group


# group by author_id and apply processing functions
df = df.groupby(0).apply(process_group)

# write the results to a csv file
df.to_csv('output.csv', index=False, header=False)
