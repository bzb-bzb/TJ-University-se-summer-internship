#本文件实现的功能是数据过滤，处理标题数据、作者数据以及作者研究单位数据
import pandas as pd
from collections import Counter
import re

# 定义常用词汇
stopwords = {'a', 'do', 'does', 'an', 'is', 'with', 'on', 'by', 'using',
             'for', 'of', 'and', 'in', 'to', 'the', 'from', 'be', 'can'}

# 定义一个函数来处理标题数据
def process_title(title):
    # 转换为小写
    title = title.lower()
    # 去除标点符号
    title = title.replace('-', ' ').replace(':', '').replace('?', '').replace('!', '').replace(',', '')
    # 分割成单词列表
    words = title.split(' ')
    # 去除常用词汇
    words = [word for word in words if word not in stopwords]
    # # 将处理后的单词列表重新拼接为字符串
    # processed_title = ' '.join(words)
    return words

# 导入 CSV 文件
df = pd.read_csv('cvpr_2022_papers.csv')

# 对 'title' 列进行数据处理
df['processed_title'] = df['title'].apply(lambda title: process_title(title))

# # 保存处理后的数据到新的 CSV 文件
# df.to_csv('processed_cvpr_2022_papers.csv', index=False)
all_words = []

df['processed_title'].apply(lambda words: all_words.extend(words))

# 统计词频
word_freq = Counter(all_words)

# 将词频结果保存到txt文件
with open('word_frequency.txt', 'w', encoding='utf8') as file_word_count:
    for word, count in word_freq.most_common():
        file_word_count.write(f'{word}: {count}\n')

print("Word frequency count saved to word_frequency.txt")
# 统计每个作者发表的论文数
author_list = df['authors'].str.replace('\n', ', ') \
                           .str.replace('[', '') \
                           .str.replace(']', '') \
                           .str.split(', ') \
                           .explode()
author_paper = author_list.value_counts().to_dict()

# 排序后保存为文件
author_paper = sorted(author_paper.items(), key=lambda e: e[1], reverse=True)
with open('author_paper_count.txt', 'w', encoding='utf8') as file_author_count:
    for author, count in author_paper:
        file_author_count.write(f'{author}: {count}\n')

print("Author paper count saved to author_paper_count.txt")

# 导入 CSV 文件
df = pd.read_csv('cvpr_2022_papers.csv')

# 定义一个函数来处理研究机构数据
def process_institution(institution_str):
    # 去除 [ 和 ] 符号
    institution_str = institution_str.strip('[]').replace("'", "")    # 使用逗号分隔机构
    institutions = [inst.strip() for inst in institution_str.split(',')]
    return institutions

# 对 'authors_research_institution' 列进行数据处理并统计机构频率
all_institutions = []
df['processed_institution'] = df['author\'s research institution'].apply(lambda inst: process_institution(inst))
df['processed_institution'].apply(lambda institutions: all_institutions.extend(institutions))

# 统计机构频率
institution_freq = Counter(all_institutions)

# 将机构频率按出现次数进行排序
sorted_institution_freq = institution_freq.most_common()

# 将结果保存到txt文件
with open('institution_frequency.txt', 'w', encoding='utf8') as file_inst_count:
    for institution, count in sorted_institution_freq:
        file_inst_count.write(f'{institution}: {count}\n')

print("Institution frequency count saved to institution_frequency.txt")
