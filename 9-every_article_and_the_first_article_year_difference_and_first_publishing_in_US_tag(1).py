import csv

input_file = "input.csv"
output_file = "output.csv"

# initialize the collection of unique author ids
distinct_author_ids = set()

# Initialize the dictionary to store the publication year and place of the first article corresponding to each author ID
first_publication_info = {}

# open the input file
with open(input_file, "r", encoding="utf-8") as input_csv:
    csv_reader = csv.reader(input_csv)

    # iterate through each line of the input file
    for row in csv_reader:
        try:
            # Obtain the author ID, publication location, and year of publication
            author_id = row[0]
            publication_place = row[14].strip().lower()
            publication_year = int(row[7]) if row[7] not in ['0', '\\N'] else float('inf')

            # If the author ID is not in the collection, it is added to the collection
            if author_id not in distinct_author_ids:
                distinct_author_ids.add(author_id)
                # Record the year and place of publication of the first article corresponding to each author ID
                first_publication_info[author_id] = (publication_year, publication_place)

        except (IndexError, ValueError):
            # If the number of columns in the row is incorrect or cannot be converted to an integer, the row is skipped
            pass

# open the input file
with open(input_file, "r", encoding="utf-8") as input_csv:
    csv_reader = csv.reader(input_csv)

    # open the output file
    with open(output_file, "w", encoding="utf-8", newline='') as output_csv:
        csv_writer = csv.writer(output_csv)

        # iterate through each line of the input file
        for row in csv_reader:
            try:
                # Obtain the author ID, publication location, and year of publication
                author_id = row[0]
                publication_place = row[14].strip().lower()  # 去除首尾空格并转换为小写
                publication_year = int(row[7]) if row[7] not in ['0', '\\N'] else float('inf')  # 排除0和/N

                # Calculate the year difference from the year in which the first article was published
                first_publication_year = first_publication_info[author_id][0]
                year_difference = publication_year - first_publication_year

                # write the year difference to column 24
                row.append(str(year_difference))

                # Determine whether it is cultivated in the United States
                if publication_place == "us":
                    # If the first article is published in the United States, it is marked as 1, otherwise it is marked as 0
                    if publication_year == first_publication_info[author_id][0]:
                        row.append("1")
                    else:
                        row.append("0")
                else:
                    row.append("0")

                # write to the output file
                csv_writer.writerow(row)

            except (IndexError, ValueError):
                # If the number of columns in the row is incorrect or cannot be converted to an integer, the row is skipped
                pass

# Calculate the number of distinct author IDs in column 25 with 1
count_author_ids_with_1 = sum(1 for author_id in distinct_author_ids if first_publication_info[author_id][1] == "us")

# Output the number of distinct author IDs in column 25 with 1
print(f"the number of distinct author IDs in column 25 with 1：{count_author_ids_with_1}")
