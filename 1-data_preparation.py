import os
import pandas as pd
from tqdm import tqdm

# Define input and output folders
input_folder = "input"
output_folder = "output"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define batch size
batch_size = 100000


# Function to process each group of rows with the same work_id
def process_group(group):
    if 'CN' in group[14].values:  # Check if 'CN' is present in the fifteenth column
        return group
    else:
        return None


# Iterate over all CSV files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        input_filepath = os.path.join(input_folder, filename)
        output_filepath = os.path.join(output_folder, filename)

        # Use tqdm to track progress
        with tqdm(desc=f"Processing {filename}") as pbar:
            # Read the CSV file in chunks
            chunks = pd.read_csv(input_filepath, chunksize=batch_size, header=None, encoding='utf-8')
            # Initialize an empty list to store filtered rows
            filtered_rows = []
            # Iterate through each chunk
            for chunk in chunks:
                # Group rows by the sixth column ('work_id')
                grouped = chunk.groupby(5)
                # Process each group
                for _, group in grouped:
                    filtered_group = process_group(group)
                    if filtered_group is not None:
                        filtered_rows.append(filtered_group)
                # Update progress bar
                pbar.update(len(chunk))

        # Concatenate all filtered rows into a single DataFrame
        if filtered_rows:
            filtered_df = pd.concat(filtered_rows)
            # Save the filtered DataFrame to a CSV file without headers using UTF-8 encoding
            filtered_df.to_csv(output_filepath, index=False, header=False, encoding='utf-8')
