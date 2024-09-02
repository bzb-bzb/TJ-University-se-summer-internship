import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from itertools import combinations
import networkx as nx
from pyecharts.charts import Graph
from pyecharts import options as opts

# 1. 读取 institution_frequency.txt 并提取前十个单位
institution_data = []
with open('institution_frequency.txt', 'r', encoding='utf-8') as f:
    for line in f:
         # 去除多余的空格，并确保只从最后一个冒号开始分割
        institution, freq = line.strip().rsplit(': ', 1)
        institution_data.append((institution.strip(), int(freq)))

# 选择前十的单位
top_institutions = sorted(institution_data, key=lambda x: x[1], reverse=True)[:10]

# 2. 可视化前十个单位的频次
institutions, frequencies = zip(*top_institutions)
plt.figure(figsize=(10, 6))
sns.barplot(y=institutions, x=frequencies, palette="viridis")
plt.xlabel('Frequency')
plt.ylabel('Institution')
plt.title('Top 10 Institutions by Frequency')
plt.yticks(fontsize=5)  

plt.show()

# 3. 读取 cvpr_2022_papers.csv 并分析合作关系
df = pd.read_csv('cvpr_2022_papers.csv')
df = df.dropna(subset=["author's research institution"])
cooperation_counts = Counter()

for institutions in df["author's research institution"]:
    # 提取并清理单位名称列表
    institution_list = [inst.strip() for inst in institutions.split(';') if inst]
    for pair in combinations(institution_list, 2):
        cooperation_counts[tuple(sorted(pair))] += 1

# 4. 使用网络图展示合作关系
# 构建图
G = nx.Graph()
for (inst1, inst2), count in cooperation_counts.items():
    G.add_edge(inst1, inst2, weight=count)

# 设置节点大小
nodes = list(G.nodes)
node_sizes = [sum([G[u][v]['weight'] for v in G.neighbors(u)]) for u in nodes]

# 创建 Pyecharts 图
node_list = []
link_list = []

for node, size in zip(nodes, node_sizes):
    # 适当缩放节点大小，避免图形过于庞大
    node_list.append({"name": node, "symbolSize": (size * 100) / max(node_sizes)})

for u, v, data in G.edges(data=True):
    link_list.append({"source": u, "target": v, "value": data['weight']})

# 渲染图形
graph = (
    Graph()
    .add("", nodes=node_list, links=link_list, repulsion=8000)
    .set_global_opts(title_opts=opts.TitleOpts(title="Institution Cooperation Network"))
)
graph.render("institution_cooperation_network.html")