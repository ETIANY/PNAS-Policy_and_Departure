import pandas as pd

# read the data into the data frame df
df = pd.read_csv('input.csv')

# define the columns to be analyzed
columns_to_analyze = [
    'article_count_before_leave', 'position1_count', 'position2_count',
    'position3_count', 'article_cite_before_leave', 'articlely_cite_before_leave',
    'articlely_jif_before_leave', 'h_index'
]

# define a discipline mapping dictionary
subject_mapping = {
    1: 'Engineering and Computer Science',
    2: 'Life Science',
    3: 'Mathematics and Physical Science',
    4: 'Social Sciences and Others'
}

# replace the discipline number with the name
df['subject'] = df['subject'].map(subject_mapping)

# convert leave_year to a string
df['leave_year'] = df['leave_year'].astype(str)

# the standard values for 2008 2012 were calculated
standard_years = ['2008', '2009', '2010', '2011', '2012']
standard_values = {}

for col in columns_to_analyze:
    avg_data = df.groupby(['subject', 'leave_year'])[col].mean().unstack(fill_value=0)

    # The average value for 2008-2012 was calculated as a standard value
    if all(year in avg_data.columns for year in standard_years):
        standard_values[col] = avg_data[standard_years].mean(axis=1)
    else:
        print(f"Cannot calculate standard values for {col} because some standard_years are missing in columns.")

# normalize data for other years
standardized_data = {col: pd.DataFrame() for col in columns_to_analyze}

for col in columns_to_analyze:
    avg_data = df.groupby(['subject', 'leave_year'])[col].mean().unstack(fill_value=0)

    # make sure that the standard value exists
    if col in standard_values:
        # define the standardization phase
        periods = {
            '2008-2012': ['2008', '2009', '2010', '2011', '2012'],
            '2013-2017': ['2013', '2014', '2015', '2016', '2017'],
            '2018-2022': ['2018', '2019', '2020', '2021', '2022'],
            '2023': ['2023']
        }

        # Create a new DataFrame to store the normalized data
        standardized_df = pd.DataFrame(index=avg_data.index, columns=periods.keys())

        # standardize each stage
        for period, years in periods.items():
            #calculate the mean for that period
            if any(year in avg_data.columns for year in years):
                period_mean = avg_data[years].mean(axis=1)
                # normalize
                standardized_df[period] = period_mean / standard_values[col]

        # save the normalized data to a csv file
        file_name = f'output-{col}__standardized_extended.csv'
        standardized_df.to_csv(file_name, header=True)
        print(f"Standardized data for {col} saved to {file_name}")
    else:
        print(f"Standard values not found for {col}.")

print("Standardization process completed.")
