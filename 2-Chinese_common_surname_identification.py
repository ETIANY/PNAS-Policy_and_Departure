import os
import csv

# 常用姓氏列表
chinese_surname = [
    "au", "bai", "cai", "cao", "chan", "chang", "chao", "chau", "chen", "cheng",
    "cheung", "chia", "chiang", "chiao", "chien", "chin", "ching", "chiu", "cho",
    "choi", "chou", "chow", "chu", "chuang", "chui", "chun", "chung", "cui", "dai",
    "deng", "ding", "dong", "du", "duan", "fan", "fang", "feng", "fong", "foo", "fu",
    "fung", "gao", "gong", "gu", "guo", "ha", "han", "hao", "hau", "he", "heung", "ho",
    "hon", "hong", "hou", "hsia", "hsiang", "hsiao", "hsieh", "hsin", "hsiung", "hsu",
    "hsueh", "hu", "huang", "hui", "hung", "jen", "jia", "jiang", "jin", "ka", "kam",
    "kang", "kao", "ke", "keung", "kiu", "ko", "kok", "kong", "ku", "kung", "kuo",
    "kwok", "lai", "lam", "lau", "lay", "lee", "lei", "leung", "li", "liang", "liao",
    "lin", "liu", "lo", "long", "loong", "lu", "lui", "luk", "lung", "luo", "lv", "lyu",
    "ma", "man", "mang", "mao", "meng", "mo", "mok", "ng", "ngai", "ou", "pai", "pak",
    "pan", "pang", "peng", "poon", "pun", "qian", "qiao", "qin", "qiu", "ren", "san",
    "sham", "shao", "shek", "shen", "sheung", "shi", "shih", "shiu", "shum", "si", "sit",
    "siu", "so", "song", "su", "suen", "sum", "sun", "sung", "sze", "tai", "tam", "tan",
    "tan ", "qin", "tang", "tao", "teng", "tian", "tien", "tin", "ting", "to", "tong",
    "tsai", "tsang", "tsao", "tse", "tseng", "tseung", "tso", "tsong", "tsou", "tsui",
    "tu", "tuan", "tuen", "tung", "wai", "wan", "wang", "wei", "wen", "when", "wong",
    "wu", "xia", "xiang", "xiao", "xie", "xin", "xiong", "xu", "xue", "yam", "yan", "yang",
    "yao", "yau", "ye", "yeh", "yen", "yeung", "yi", "yik", "yim", "yin", "yip", "yiu",
    "yu", "yv", "yuan", "yue", "yuen", "zeng", "zhang", "zhao", "zheng", "zhong", "zhou",
    "zhu", "zhuang", "zou", "hsu", "hsueh", "ko", "yik ", "zuo", "zu", "zong", "zhuo", "zhi",
    "zhen", "zhan", "zha", "zang", "zhai", "shaw", "xyu", "duo", "cha", "yü", "xü",
    "wáng", "xú", "zhèng", "zēng", "yè", "yáo", "lù", "zōu", "léi", "shào", "lǐ", "sūn", "liáng", "péng",
    "jiǎng", "lú", "jīn", "xióng", "lí", "wàn", "zhāng", "mǎ", "xiè", "xiāo", "dù", "fù", "shí", "mèng",
    "shǐ", "qián", "liú", "zhū", "sòng", "cài", "sū", "zhōng", "dài", "qín", "lóng", "yán", "chén", "hú",
    "táng", "pān", "wèi", "jiāng", "jiǎ", "bái", "táo", "lài", "yáng", "lín", "xǔ", "tián", "chéng", "cuī",
    "wéi", "hè", "huáng", "guō", "dèng", "dǒng", "lǚ", "tán", "xià", "gù", "hóng", "wú", "hé", "féng",
    "yuán", "dīng", "liào", "qiū", "xuē", "máo", "wǔ", "zhào", "gāo", "hán", "shěn", "fàn", "fāng",
    "yǐn", "hǎo", "mò", "zhōu", "luó", "cáo", "yú", "rén", "wāng", "hòu", "duàn", "gōng", "kǒng",
    "zan", "yun", "you", "yong", "ying", "xuan", "xiu", "xing", "xian", "xi", "weng", "suo", "sui",
    "shuai", "shu", "sheng", "she", "shang", "sha", "sang", "rui", "ruan", "ru", "rong", "rao", "ran",
    "que", "quan", "qu", "qing", "qiang", "qi", "pu", "ping", "piao", "pi", "pei", "ouyang", "nong",
    "niu", "ning", "nie", "ni", "nan", "na", "mu", "ming", "min", "miao", "mi", "men", "mei", "mai",
    "luan", "lou", "ling", "lian", "leng", "le", "lao", "lang", "lan", "kuang", "kou", "kan", "ju", "jing",
    "jie", "jiao", "jian", "ji", "huo", "hua", "heng", "hang", "hai", "gui", "guan", "gou",
    "geng", "ge", "gan", "gai", "fei", "dou", "diao", "di", "dang", "dan", "cong", "chi", "che", "chai",
    "cen", "bu", "bo", "bin", "bian", "bi", "bao", "ban", "ba", "ao", "an", "ai", "lü", "hwang", "phan",
    "sheu", "baili", "bang", "bei", "ben", "bie", "bing", "cang", "chong", "chunyu", "ci", "da", "shan", "chanyu",
    "tantai", "zhai", "diwu", "dian", "dongfang", "dongguo", "dongmen", "duanmu", "duangan", "nai", "fa", "gang",
    "gongliang", "gongsun", "gongxi", "gongyang", "gongye", "guang", "helian",
    "hei", "huyan", "huai", "xun", "huan", "huangfu", "jiagu", "jiu", "kai", "kuai", "kui", "yuezheng", "liangqiu",
    "lie", "linghu", "lun", "lüqiu", "lü", "mou", "murong", "nagong", "namen", "nian",
    "qidiao", "qie", "rangsi", "seng", "shangguan", "shentu", "shou", "shuang", "shui", "sikong", "sikou", "sima",
    "situ", "tuo", "tuoba", "taishu", "ti", "tie", "wanyan", "moqi", "weisheng", "yuchi",
    "wenren", "wo", "wuma", "ximen", "xiahou", "xianyu", "xuanyuan", "yangshe", "yelǜ", "yuwen", "zai", "zaifu",
    "zao", "zhangsun", "zhongsun", "zhuge", "zhuansun", "zi", "ziche", "zongzheng", "zuoqiu"
]

# 获取当前工作目录中的所有 CSV 文件
csv_folder = "D:\openalex\pythonProject\china-sci\\2-all_8_china2"
csv_files = [file for file in os.listdir(csv_folder) if file.endswith(".csv")]

for csv_file in csv_files:
    csv_file_path = os.path.join(csv_folder, csv_file)
    rows = []

    # 打开原始 CSV 文件
    with open(csv_file_path, "r", encoding="utf-8") as f:
        # 读取 CSV 文件内容
        csv_reader = csv.reader(f)

        # 读取每一行数据，同时写入处理后的结果
        for row in csv_reader:
            # 检查姓名中是否包含中文字符
            if any('\u4e00' <= char <= '\u9fff' for char in row[1]):
                if row[18] in ["JP", "KR", "SG"] and row[14] in ["JP", "KR", "SG"]:
                    row.append("0")
                else:
                    row.append("1")

            else:
                # 处理姓名列，替换点号为空格并拆分成单词
                name_tokens = row[1].replace(".", " ").replace("-", " ").split()
                # 遍历姓名中的每个单词，检查是否都在关键词列表中，是则将第21列置为2
                if any(token.lower() in chinese_surname for token in name_tokens):
                    row.append("1")
                else:
                    row.append("0")

            rows.append(row)

    # 打开原始 CSV 文件，并写入处理后的结果
    with open(csv_file_path, "w", encoding="utf-8", newline='') as f:
        # 创建 CSV 写入对象
        csv_writer = csv.writer(f)
        # 将处理后的每一行写入原始文件
        csv_writer.writerows(rows)
    # 打印处理完的文件名
    print(f"{csv_file} 处理完")

print("Processing completed!")