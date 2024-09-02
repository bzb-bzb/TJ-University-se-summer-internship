# 读取数据
author_paper_counts = {}

with open('author_paper_count.txt', 'r', encoding='utf-8') as file:
    for line in file:
        author, count = line.strip().split(': ')
        author_paper_counts[author] = int(count)

# 按论文数量排序并取前10位
sorted_authors = sorted(author_paper_counts.items(), key=lambda x: x[1], reverse=True)[:10]

import matplotlib.pyplot as plt

# 提取作者姓名和对应的论文数量
authors = [author for author, _ in sorted_authors]
counts = [count for _, count in sorted_authors]

# 创建水平条形图
plt.figure(figsize=(10, 6))
plt.barh(authors, counts, color='skyblue')
plt.xlabel('Number of Papers Published')
plt.ylabel('Authors')
plt.title('Top 10 Authors by Number of Papers Published in 2022')
plt.gca().invert_yaxis()  # 反转Y轴，使得数量最多的作者在顶部

# 显示图表
plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict

# 读取 author_paper_count.txt 文件
with open('author_paper_count.txt', 'r', encoding='utf-8') as file:
    author_counts = {}
    for line in file:
        author, count = line.strip().split(': ')
        author_counts[author.strip("'")] = int(count)

# 筛选出发表篇数>=1的作者
selected_authors = {author for author, count in author_counts.items() if count >=1}


# 读取 cvpr_2022_papers.csv 文件
df = pd.read_csv('cvpr_2022_papers.csv')

# 初始化作者之间的合作矩阵
cooperation_matrix = defaultdict(lambda: defaultdict(int))

# 统计作者之间的合作关系
for authors in df['authors']:
    author_list = [author.strip() for author in authors.split(',')]
    filtered_authors = [author for author in author_list if author in selected_authors]
    
    for i in range(len(filtered_authors)):
        for j in range(i + 1, len(filtered_authors)):
            author1, author2 = filtered_authors[i], filtered_authors[j]
            cooperation_matrix[author1][author2] += 1
            cooperation_matrix[author2][author1] += 1

# 转换为 DataFrame 以便于绘图
cooperation_df = pd.DataFrame(cooperation_matrix).fillna(0)

# 绘制热力图
plt.figure(figsize=(10, 8))
sns.heatmap(cooperation_df, annot=True, cmap='YlGnBu', fmt='g', linewidths=.5)
plt.title('Collaboration Between Authors')
plt.show()

