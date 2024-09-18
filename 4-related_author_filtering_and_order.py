import csv

input_file = "input.csv"
output_file = "output.csv"

# Initialize the number of processed rows and the number of different columns 1
processed_rows = 0
distinct_column_1 = set()

# Initialize the dictionary to hold all the rows for each author ID
author_info = {}

# open the input file
with open(input_file, "r", encoding="utf-8") as input_csv:
    csv_reader = csv.reader(input_csv)

    # iterate through each line of the input file
    for row in csv_reader:
        try:
            # handle the values in columns 15 and 19
            column_15 = row[14].lower()
            column_19 = row[18].lower()

            # add column 1 of the current row to the collection
            distinct_column_1.add(row[0])

            # update the author information dictionary
            author_id = row[0]
            if author_id in author_info:
                author_info[author_id].append(row)
            else:
                author_info[author_id] = [row]
        except (IndexError, ValueError):
            # If the number of columns in the row is incorrect or cannot be converted to an integer, the row is skipped
            pass

# Handle the Author Information Dictionary with column 22
with open(output_file, "w", encoding="utf-8", newline='') as output_csv:
    csv_writer = csv.writer(output_csv)

    for author_id, rows in author_info.items():
        # Check whether the 15th and 19th columns of all rows corresponding to the author ID have US and CN
        has_us_cn = any("us" in row[14].lower() and "cn" in row[18].lower() for row in rows)
        # If there are US and CN, write the line marked 1 to the output file
        if has_us_cn:
            # For rows with the same author ID, sort by year from smallest to largest
            sorted_rows = sorted(rows, key=lambda x: int(x[7]))
            for row in sorted_rows:
                # label column 22 of the eligible rows as 1
                row.append('1')
                csv_writer.writerow(row)
                processed_rows += 1

#Print the number of rows marked with 1 in column 22
print(f"the number of rows where column 22 marked 1：{processed_rows}")

# print the number of distinct column 1
print(f"the number of distinct column 1：{len(distinct_column_1)}")
