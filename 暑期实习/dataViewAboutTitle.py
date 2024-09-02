import pandas as pd
from collections import Counter

# 读取CSV文件
df = pd.read_csv("processed_cvpr_2022_papers.csv")

# 提取标题数据
titles = df['processed_title'].tolist()

# 计算标题的字母个数和单词个数
title_lengths = [len(title.replace(" ", "")) for title in titles]  # 字母个数
word_counts = [len(title.split()) for title in titles]  # 单词个数

# 定义字母个数的区间
letter_bins = [0, 20, 40, 60, 80, 100, float('inf')]
letter_labels = ["0-20", "21-40", "41-60", "61-80", "81-100", ">100"]

# 定义单词个数的区间
word_bins = [0, 5, 10, 15, 20, float('inf')]
word_labels = ["0-5", "6-10", "11-15", "16-20", ">20"]

# 将标题长度和单词个数分区
letter_distribution = Counter(pd.cut(title_lengths, bins=letter_bins, labels=letter_labels))
word_distribution = Counter(pd.cut(word_counts, bins=word_bins, labels=word_labels))

from pyecharts import options as opts
from pyecharts.charts import Pie

# 绘制字母个数的玫瑰图
letter_pie = (
    Pie()
    .add(
        "Title Length (Letters)",
        [list(z) for z in zip(letter_labels, letter_distribution.values())],
        radius=["30%", "75%"],
        center=["50%", "50%"],
        rosetype="radius",
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Title Length Distribution (Letters)"),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
)

# 绘制单词个数的玫瑰图
word_pie = (
    Pie()
    .add(
        "Title Length (Words)",
        [list(z) for z in zip(word_labels, word_distribution.values())],
        radius=["30%", "75%"],
        center=["50%", "50%"],
        rosetype="radius",
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Title Length Distribution (Words)"),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
)

# 渲染玫瑰图为 HTML 文件
letter_pie.render("title_length_distribution_letters.html")
word_pie.render("title_length_distribution_words.html")
