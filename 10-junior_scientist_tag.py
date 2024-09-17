import pandas as pd

# 读取CSV文件
df = pd.read_csv('14-all.csv', header=None)


# 定义函数进行判断
def process_group(group):
    # 初始化标志列为0
    group[31] = 0

    # 获取第一行的年份
    n = group.iloc[0, 7]

    # 找到所有26列为1的行
    rows_with_one = group[(group[25] == 1) & (group[24] != 0)]

    for index, row in rows_with_one.iterrows():
        # 获取第30列的年份
        m_values = group[group[29].notna()][29].tolist()

        # 找到所有m-n小于等于5的行，并且第15列为'CN'
        valid_rows = group[(group[29] - n <= 5) & (group[14] == 'CN')]

        # 找到25列的年份
        x = row[24]

        # 如果存在满足条件的行，并且25列的年份减去n小于等于7
        if not valid_rows.empty and x - n <= 7:
            # 将31列标注为1
            group.at[index, 31] = 1

    return group


# 按author_id分组并应用处理函数
df = df.groupby(0).apply(process_group)

# 将结果写入CSV文件
df.to_csv('15-junior标记-us1且5年内CN七年内离开.csv', index=False, header=False)
