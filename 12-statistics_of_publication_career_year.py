import csv
import pandas as pd
import statistics


# read the csv file
def read_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


# statistical academic_year
def count_academic_year(data):
    df = pd.DataFrame(data)
    academic_years = df.groupby(10)[0].nunique().reset_index(name='count')  # 统计每个academic_year年份下不同的ID数量
    academic_years.columns = ['academic_year', 'count']
    return academic_years


# output statistical results
def output_statistics(academic_years):
    # calculate the median
    median = statistics.median(academic_years['count'])

    # calculate the mode
    mode = statistics.mode(academic_years['count'])

    # calculate the average
    mean = statistics.mean(academic_years['count'])

    # calculate the variance
    variance = statistics.variance(academic_years['count'])

    # calculate the maximum value
    maximum = max(academic_years['count'])

    # calculate the minimum value
    minimum = min(academic_years['count'])

    # quartile quantiles are calculated
    quartiles = academic_years['count'].quantile([0.25, 0.5, 0.75])

    return median, mode, mean, variance, maximum, minimum, quartiles


# write statistics to a csv file
def write_csv(output_filename, academic_year_counts):
    academic_year_counts.to_csv(output_filename, index=False)


# main function
def main(input_filename, output_filename):
    # read the csv file
    data = read_csv(input_filename)

    # 统计academic_year
    academic_year_counts = count_academic_year(data)

    # write statistics to a csv file
    write_csv(output_filename, academic_year_counts)

    # output statistics
    median, mode, mean, variance, maximum, minimum, quartiles = output_statistics(academic_year_counts)
    print("Median:", median)
    print("Mode:", mode)
    print("Mean:", mean)
    print("Variance:", variance)
    print("Maximum:", maximum)
    print("Minimum:", minimum)
    print("Quartiles:")
    print(quartiles)


if __name__ == "__main__":
    input_filename = "input.csv"  # enter the name of the csv file
    output_filename = "output.csv"  # the name of the output csv file
    main(input_filename, output_filename)
