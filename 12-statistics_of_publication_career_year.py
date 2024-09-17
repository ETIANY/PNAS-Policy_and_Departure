import csv
import pandas as pd
import statistics


# 读取CSV文件
def read_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


# 统计academic_year
def count_academic_year(data):
    df = pd.DataFrame(data)
    academic_years = df.groupby(10)[0].nunique().reset_index(name='count')  # 统计每个academic_year年份下不同的ID数量
    academic_years.columns = ['academic_year', 'count']
    return academic_years


# 输出统计结果
def output_statistics(academic_years):
    # 计算中位数
    median = statistics.median(academic_years['count'])

    # 计算众数
    mode = statistics.mode(academic_years['count'])

    # 计算平均值
    mean = statistics.mean(academic_years['count'])

    # 计算方差
    variance = statistics.variance(academic_years['count'])

    # 计算最大值
    maximum = max(academic_years['count'])

    # 计算最小值
    minimum = min(academic_years['count'])

    # 计算四分位数
    quartiles = academic_years['count'].quantile([0.25, 0.5, 0.75])

    return median, mode, mean, variance, maximum, minimum, quartiles


# 写入统计结果到CSV文件
def write_csv(output_filename, academic_year_counts):
    academic_year_counts.to_csv(output_filename, index=False)


# 主函数
def main(input_filename, output_filename):
    # 读取CSV文件
    data = read_csv(input_filename)

    # 统计academic_year
    academic_year_counts = count_academic_year(data)

    # 写入统计结果到CSV文件
    write_csv(output_filename, academic_year_counts)

    # 输出统计信息
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
    input_filename = "9-1-列11学术生涯-使用了6-1的代码-年份乱序.csv"  # 输入的CSV文件名
    output_filename = "9-3-学术生涯统计.csv"  # 输出的CSV文件名
    main(input_filename, output_filename)
