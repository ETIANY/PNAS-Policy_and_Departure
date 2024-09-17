import csv
import itertools

input_file = "C-merged_result-all.csv"
output_file = "C-all0427.csv"
memory_buffer = []

# 初始化处理行数和distinct列1的集合
processed_rows = 0
distinct_column_1 = set()

# 打开输入文件
with open(input_file, "r", encoding="utf-8") as input_csv:
    csv_reader = csv.reader(input_csv)
    # 跳过表头
    next(csv_reader)

    # 遍历输入文件的每一行
    for row in csv_reader:
        try:
            # 将当前行的列1添加到集合中
            distinct_column_1.add(row[0])

            # 存储到内存缓冲区中
            memory_buffer.append(row)
        except (IndexError, ValueError):
            # 如果行中的列数不正确或者无法转换为整数，则跳过该行
            pass

# 对内存缓冲区中的数据按照作者ID和年份排序
memory_buffer.sort(key=lambda x: (int(x[0]) if x[0].isdigit() else 0, int(x[7]) if x[7].isdigit() else 0))


# 分组，按照作者ID分组
grouped_data = itertools.groupby(memory_buffer, key=lambda x: x[0])

# 处理作者信息字典，标注第23列
with open(output_file, "w", encoding="utf-8", newline='') as output_csv:
    csv_writer = csv.writer(output_csv)

    for author_id, rows in grouped_data:
        rows = list(rows)  # 将行转换为列表以便排序
        # 检查作者id对应的所有行的第15列和第19列的情况
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

        # 根据情况标注第23列
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

            # 写入处理后的行到输出文件
            csv_writer.writerow(row)
            processed_rows += 1

# 打印处理完的行数和distinct列1的个数
print(f"处理完成的行数：{processed_rows}")
print(f"distinct列1的个数：{len(distinct_column_1)}")
