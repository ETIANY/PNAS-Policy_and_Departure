import csv

input_file = "input.csv"
output_file = "output.csv"

# Initialize the number of processed rows and the number of different columns 1
processed_rows = 0
distinct_column_1 = set()

# Initialize the dictionary to store all rows for each author ID and the earliest and latest publication year
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

            # check if the publication_year is valid
            if row[7] == "" or row[7] == "\\N":
                continue

            # add column 1 of the current row to the collection
            distinct_column_1.add(row[0])

            # update the author information dictionary
            author_id = row[0]
            publication_year = int(row[7])
            if author_id in author_info:
                author_info[author_id]["rows"].append(row)
                # update the earliest and latest publication year
                if publication_year < author_info[author_id]["earliest_year"]:
                    author_info[author_id]["earliest_year"] = publication_year
                if publication_year > author_info[author_id]["latest_year"]:
                    author_info[author_id]["latest_year"] = publication_year
            else:
                author_info[author_id] = {
                    "rows": [row],
                    "earliest_year": publication_year,
                    "latest_year": publication_year
                }
        except (IndexError, ValueError):
            # If the number of columns in the row is incorrect or cannot be converted to an integer, the row is skipped
            pass

# Manipulate the author information dictionary and add the academic career length column
with open(output_file, "w", encoding="utf-8", newline='') as output_csv:
    csv_writer = csv.writer(output_csv)

    for author_id, info in author_info.items():
        # If there is only one year of publication, the length of academic career is 0
        if info["earliest_year"] == info["latest_year"]:
            career_length = 0
        else:
            # calculate the length of an academic career
            career_length = info["latest_year"] - info["earliest_year"]

        for row in info["rows"]:
            # add the academic career length column
            row.append(str(career_length))
            csv_writer.writerow(row)
            processed_rows += 1

# the number of unique author ids that are printed
print(f"the number of unique author ids：{len(distinct_column_1)}")