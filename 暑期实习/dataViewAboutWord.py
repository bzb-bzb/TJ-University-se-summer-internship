import pandas as pd
import numpy as np
from math import log
from pyecharts.charts import Graph
from pyecharts import options as opts

# 读取标题数据
df = pd.read_csv('processed_cvpr_2022_papers.csv')
titles = df['processed_title'].tolist()

# 读取词频数据
word_frequencies = {}
with open('word_frequency.txt', 'r', encoding='utf-8') as file:
    for line in file:
        word, freq = line.split(': ')
        word_frequencies[word] = int(freq)

# 筛选出词频大于的热点词汇
word_list = [word for word, freq in word_frequencies.items() if freq > 17]

# 计算词汇之间的关联次数
relations = {}
for title in titles:
    words_in_title = [word for word in word_list if word in title]
    for i in range(len(words_in_title)):
        for j in range(i + 1, len(words_in_title)):
            pair = tuple(sorted([words_in_title[i], words_in_title[j]]))
            if pair not in relations:
                relations[pair] = 0
            relations[pair] += 1

# 计算节点大小和连接线线宽
nodes = []
edges = []

max_relation = max(relations.values())
min_relation = min(relations.values())

for word in word_list:
    sum_value = sum([relations.get(tuple(sorted([word, other_word])), 0) for other_word in word_list if other_word != word])
    node_size = log(sum_value + 1) * 100 - 450
    nodes.append({"name": word, "symbolSize": max(node_size, 10)})  # 设置最小节点大小为10

for (word1, word2), relation_value in relations.items():
    line_width = np.exp(3 * (relation_value - min_relation) / (max_relation - min_relation))
    edges.append({"source": word1, "target": word2, "lineStyle": {"width": line_width}})

# 创建网络关系图
graph = Graph()

graph.add(
    "",
    nodes=nodes,
    links=edges,
    repulsion=8000,
    linestyle_opts=opts.LineStyleOpts(curve=0.2),
)

graph.set_global_opts(
    title_opts=opts.TitleOpts(title="热点词汇网络关系图"),
    toolbox_opts=opts.ToolboxOpts(),
    tooltip_opts=opts.TooltipOpts(is_show=True)
)

graph.render("hot_words_network.html")  # 保存为HTML文件


import matplotlib.pyplot as plt

# 读取并解析 word_frequency.txt 文件
word_frequencies = {}

with open('word_frequency.txt', 'r', encoding='utf-8') as file:
    for line in file:
        word, frequency = line.strip().split()
        word_frequencies[word] = int(frequency)

# 对频率进行排序，选择前10的热点词汇
top_10_words = sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True)[:10]

# 提取词汇和频率
words = [item[0] for item in top_10_words]
frequencies = [item[1] for item in top_10_words]

# 使用 matplotlib 绘制柱状图
plt.figure(figsize=(10, 6))
plt.bar(words, frequencies, color='blue')
plt.xlabel('Words')
plt.ylabel('Frequencies')
plt.title('Top 10 Hot Words by Frequency')
plt.xticks(rotation=45)  # 旋转x轴标签，以防标签重叠
plt.show()


from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取txt文件内容
with open('word_frequency.txt', 'r', encoding='utf-8') as file:  # 请替换'titles.txt'为你的文件名
    text = file.read()

# 生成词云
wordcloud = WordCloud(
    width=800,            # 设置图片的宽度
    height=400,           # 设置图片的高度
    background_color='white',  # 背景颜色
    max_words=200,        # 显示的最大单词数量
    colormap='viridis',   # 词云的颜色方案
    stopwords=None        # 可以设置停用词（不需要的词）
).generate(text)

# 显示词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 关闭坐标轴
plt.show()

# 保存词云图像到文件
wordcloud.to_file('wordcloud.png')  # 保存为png文件，路径可自定义



