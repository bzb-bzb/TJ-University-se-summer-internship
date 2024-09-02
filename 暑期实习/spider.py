#本文件实现的功能是将CVPR2022和CVPR2023的论文的URL爬取下来并存储
import requests
from bs4 import BeautifulSoup

# 定义一个函数来爬取指定年份的CVPR会议论文信息
def scrape_cvpr_papers(year):
    # 1. 构建请求URL
    url = f"https://openaccess.thecvf.com/CVPR{year}?day=all"

    # 2. 发送HTTP请求以获取页面内容
    response = requests.get(url)
    
    # 检查请求是否成功
    if response.status_code != 200:
        print(f"Failed to retrieve data for {year}")
        return []
    
    # 3. 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')
    papers = []

    dts = soup.find_all('dt', class_='ptitle')
    print('爬取的数据数量', len(dts))

    base_url = "https://openaccess.thecvf.com"

    # 4. 查找并遍历页面中的所有论文条目
    for paper in soup.find_all('dt', class_='ptitle'):
        # 5. 提取论文标题
        title = paper.text.strip()

        # 6. 提取作者信息，通常在下一个相邻标签 <dd> 内
        authors_dd = paper.find_next_sibling('dd')
        authors = authors_dd.text.strip()

         # 7. 提取PDF的URL，该URL在作者信息的下一个相邻标签 <dd> 内，并且是其中的第一个 <a href> 标签
        pdf_url_dd = authors_dd.find_next_sibling('dd')
        pdf_url_tag = pdf_url_dd.find('a', href=True)
        pdf_url = pdf_url_tag['href'] if pdf_url_tag else None

        # 如果找到了pdf_url，就在它前面加上base_url
        if pdf_url:
            full_pdf_url = base_url + pdf_url
        else:
            full_pdf_url = None

        # 8. 将信息存储在字典中，并添加到列表中
        papers.append({'title': title, 'authors': authors, 'pdf_url': full_pdf_url})

        # print(f"Paper Title: {title}")
        # print(f"PDF URL: {full_pdf_url}\n")

    # 8. 返回收集的论文信息
    return papers

# # 爬取CVPR 2022 和 CVPR 2023 的论文信息
# papers_2022 = scrape_cvpr_papers(2022)
# papers_2023 = scrape_cvpr_papers(2023)




