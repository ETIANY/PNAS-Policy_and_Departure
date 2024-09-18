import csv
import itertools

input_file = "input.csv"
output_file = "output.csv"
memory_buffer = []

# Initialize the collection of the number of processed rows and distinct column 1
processed_rows = 0
distinct_column_1 = set()

# open the input file
with open(input_file, "r", encoding="utf-8") as input_csv:
    csv_reader = csv.reader(input_csv)
    # skip the header
    next(csv_reader)

    # iterate through each line of the input file
    for row in csv_reader:
        try:
            # add column 1 of the current row to the collection
            distinct_column_1.add(row[0])

            # stored in a memory buffer
            memory_buffer.append(row)
        except (IndexError, ValueError):
            # If the number of columns in the row is incorrect or cannot be converted to an integer, the row is skipped
            pass

# The data in the memory buffer is sorted by author ID and year
memory_buffer.sort(key=lambda x: (int(x[0]) if x[0].isdigit() else 0, int(x[7]) if x[7].isdigit() else 0))


# grouping grouped by author id
grouped_data = itertools.groupby(memory_buffer, key=lambda x: x[0])

# Handle the Author Information Dictionary with column 23
with open(output_file, "w", encoding="utf-8", newline='') as output_csv:
    csv_writer = csv.writer(output_csv)

    for author_id, rows in grouped_data:
        rows = list(rows)  # convert rows to lists for easy sorting
        # Check the case in columns 15 and 19 of all rows corresponding to the author ID
        has_only_cn = all("cn" in row[14].lower() and "cn" in row[18].lower() for row in rows)
        has_only_us = all("us" in row[14].lower() and "us" in row[18].lower() for row in rows)
        has_no_uscn = all(
            "us" not in row[14].lower() and "us" not in row[18].lower() and "cn" not in row[14].lower() and "cn" not in
            row[18].lower() for row in rows)
        has_us19_cn15 = any("us" in row[18].lower() and "cn" in row[14].lower() for row in rows)
        has_us19_nocn15 = any("us" in row[18].lower() and "cn" not in row[14].lower() for row in rows)
        has_cn19_us15 = any("cn" in row[18].lower() and "us" in row[14].lower() for row in rows)
        has_cn19_usno15 = any("cn" in row[18].lower() and "us" not in row[14].lower() for row in rows)
        has_other19_cnandus15 = any((("us" not in row[18].lower() and "cn" not in row[18].lower()) and "cn" in row[14].lower()) and (
                        ("us" not in row[18].lower() and "cn" not in row[18].lower()) and "us" in row[14].lower()) for row in rows)
        has_other19_cnandother15 = any(
            (("us" not in row[18].lower() and "cn" not in row[18].lower()) and "cn" in row[14].lower()) and (
                        ("us" not in row[18].lower() and "cn" not in row[18].lower()) and "us" not in row[14].lower())
            for row in rows)
        has_other19_usandother15 = any(
            (("us" not in row[18].lower() and "cn" not in row[18].lower()) and "us" in row[14].lower()) and (
                        ("us" not in row[18].lower() and "cn" not in row[18].lower()) and "cn" not in row[14].lower())
            for row in rows)

        # label column 23 as appropriate
        for row in rows:
            if has_only_cn:
                row.append('1')
            elif has_only_us:
                row.append('9')
            elif has_no_uscn:
                row.append('0')
            elif has_cn19_us15:
                row.append('2')
            elif has_cn19_usno15:
                row.append('3')
            elif has_us19_cn15:
                row.append('4')
            elif has_us19_nocn15:
                row.append('8')
            elif has_other19_cnandus15:
                row.append('5')
            elif has_other19_cnandother15:
                row.append('6')
            elif has_other19_usandother15:
                row.append('7')
            else:
                row.append('10')

            # write processed lines to the output file
            csv_writer.writerow(row)
            processed_rows += 1

# The number of processed rows and the number of distinct columns 1 are printed
print(f"the number of rows processed to complete：{processed_rows}")
print(f"distinct number of column_1：{len(distinct_column_1)}")
