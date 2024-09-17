import pandas as pd

# 读取CSV文件
file_path = '20-leave_to只有一个国家且concept_0唯一.csv'
df = pd.read_csv(file_path)

# 处理/N为空值
df.replace('', pd.NA, inplace=True)

# 定义根据 concept_0 判断 subject 的函数
def categorize_subject(concept):
    if concept in ['41008148', '127413603']:
        return 'Engineering and computer science'
    elif concept in ['71924100', '86803240', '39432304']:
        return 'Life science'
    elif concept in ['121332964', '127313418', '33923547', '185592680', '192562407', '205649164']:
        return 'Mathematics and physical science'
    elif concept in ['138885662', '142362112', '144024400', '144133560', '162324750', '15744967', '95457728', '17744445']:
        return 'Social sciences and others'
    else:
        return 'Other'

# 根据 concept_0 判断 subject 并新增一列
df['subject'] = df['concept_0'].astype(str).apply(categorize_subject)

# 保存修改后的 DataFrame 到 CSV 文件中
df.to_csv('21-leave_to只有一个国家且concept_0唯一-subject.csv', index=False)
