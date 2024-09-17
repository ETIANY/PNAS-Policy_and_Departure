import pandas as pd
from tqdm import tqdm

# 读取无表头的CSV文件
df = pd.read_csv('9-8补充抽取tag4.csv', header=None)

# 根据第一列ID进行分组
grouped = df.groupby(0)

# 创建一个函数来查找离开年份
def find_leave_year(group):
    # 找到这一组中所有第三列的最大值，也就是最新发表的年份
    latest_year = group[2].max()

    # 找到这一组中所有第3列值为2的年份的最大值
    us_maxyear = group[group[2] == 2][1].max()

    # 初始化离开年为0
    leave_year = 0

    # 如果US最大年份等于最新年份，则离开年为0，否则继续判断
    leave_year = 0 if us_maxyear == latest_year else leave_year

    # 找到这个年份+1，+2等等（最小增加）的年份对应的第三列不再是“2”的最小年份，作为这一组的离开年leave_year
    for i in range(1, 6):  # 假设向后查找5年
        if (us_maxyear + i) in group[1].values:
            if group[group[1] == (us_maxyear + i)][2].values[0] != 2:
                leave_year = us_maxyear + i
                break

    return leave_year

# 使用 tqdm 显示进度条
for author_id, group in tqdm(grouped, total=len(grouped), desc="Processing groups"):
    leave_year = find_leave_year(group)
    # 将 leave_year 写入该组的所有行的第8列
    df.loc[group.index, 7] = leave_year

    # 如果离开年不为0，则将对应的第三列的机构代码写入第12列
    if leave_year != 0:
        inst_codes = group[group[1] == leave_year][2].astype(str).unique()  # 获取唯一的机构代码
        if len(inst_codes) > 0:
            df.loc[group.index, 11] = ','.join(inst_codes)  # 以逗号分隔的字符串形式存储所有唯一的机构代码
        else:
            df.loc[group.index, 11] = '0'  # 没有找到对应年份的机构代码，将第12列设为0
    else:
        df.loc[group.index, 11] = '0'  # 离开年为0，将第12列设为0
# 将结果写入新的CSV文件，不包含表头
df.to_csv('10-列8离开年列12离开去向数组-补充tag4.csv', header=False, index=False)