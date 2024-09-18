import pandas as pd
from tqdm import tqdm

# read a csv file without a header
df = pd.read_csv('inout.csv', header=None)

# grouping is based on the first column id
grouped = df.groupby(0)

# create a function to find the year of departure
def find_leave_year(group):
    # Find the maximum value of all third columns in this group, which is the most recent published year
    latest_year = group[2].max()

    # Find the maximum value for all the years in this group where column 3 has a value of 2
    us_maxyear = group[group[2] == 2][1].max()

    # the initialization departure year is 0
    leave_year = 0

    # If the maximum year of US is equal to the latest year, the departure year is 0, otherwise the judgment continues
    leave_year = 0 if us_maxyear == latest_year else leave_year

    # Find the third column corresponding to the year +1, +2, etc. (minimum increase) for this year, which is no longer the minimum year of "2", as the departure year leave_year for this group
    for i in range(1, 6):  # let s say look back 5 years
        if (us_maxyear + i) in group[1].values:
            if group[group[1] == (us_maxyear + i)][2].values[0] != 2:
                leave_year = us_maxyear + i
                break

    return leave_year

# use tqdm to display a progress bar
for author_id, group in tqdm(grouped, total=len(grouped), desc="Processing groups"):
    leave_year = find_leave_year(group)
    # Write leave_year to column 8 of all rows in the group
    df.loc[group.index, 7] = leave_year

    # If the year of departure is not 0, write the institution code in the corresponding third column to column 12
    if leave_year != 0:
        inst_codes = group[group[1] == leave_year][2].astype(str).unique()  # get a unique organization code
        if len(inst_codes) > 0:
            df.loc[group.index, 11] = ','.join(inst_codes)  # All unique institution codes are stored as comma-separated strings
        else:
            df.loc[group.index, 11] = '0'  # The institution code for the corresponding year was not found, so set column 12 to 0
    else:
        df.loc[group.index, 11] = '0'  # The departure year is 0, and the 12th column is set to 0
# Write the results to a new CSV file without the headers
df.to_csv('output.csv', header=False, index=False)