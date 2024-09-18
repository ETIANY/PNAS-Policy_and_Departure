import pandas as pd

# read the data
file_path = 'input.csv'  # replace with your actual file path
data = pd.read_csv(file_path)

# Create an empty DataFrame to store the transformed data
columns = ['leave_year']
countries = ['Australia', 'Brazil', 'Canada', 'China', 'Chinese Taiwan', 'France', 'Germany', 'Japan', 'Singapore',
             'South Korea', 'UK']
metrics = ['article_count_before_leave', 'article_cite_before_leave', 'h_index', 'i10_index']

# create a column name
for country in countries:
    for metric in metrics:
        columns.append(f'{country}_{metric}')

# create an empty dataframe
result_df = pd.DataFrame(columns=columns)

# handle each leave_year
for year in data['Leave Year'].unique():
    year_data = data[data['Leave Year'] == year]

    # create a row of data
    row_data = {'leave_year': year}

    # populate the values for each country and indicator
    for country in countries:
        country_data = year_data[year_data['Country'] == country]
        for metric in metrics:
            value = country_data[metric].sum() if not country_data.empty else 0
            row_data[f'{country}_{metric}'] = value

    # convert this row of data to a dataframe
    row_df = pd.DataFrame([row_data])

    # Adding to a Result DataFrame Using the Concat Method
    result_df = pd.concat([result_df, row_df], ignore_index=True)

# save the converted data to a new csv file
output_file_path = 'output.csv'  # replace with the path of the file you want to save
result_df.to_csv(output_file_path, index=False)

print(f"data conversion is successfully done and output file is: {output_file_path}")
