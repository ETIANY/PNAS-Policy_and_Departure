import pandas as pd

# read the csv file
file_path = 'input.csv'
df = pd.read_csv(file_path)

# handle n as a null value
df.replace('', pd.NA, inplace=True)

# Define a function that judges a subject based on concept_0
def categorize_subject(concept):
    if concept in ['41008148', '127413603']:
        return 'Engineering and computer science'
    elif concept in ['71924100', '86803240', '39432304']:
        return 'Life science'
    elif concept in ['121332964', '127313418', '33923547', '185592680', '192562407', '205649164']:
        return 'Mathematics and physical science'
    elif concept in ['138885662', '142362112', '144024400', '144133560', '162324750', '15744967', '95457728', '17744445']:
        return 'Social sciences and others'
    else:
        return 'Other'

# Judge the subject based on concept_0 and add a new column
df['subject'] = df['concept_0'].astype(str).apply(categorize_subject)

# save the modified dataframe to a csv file
df.to_csv('output.csv', index=False)
