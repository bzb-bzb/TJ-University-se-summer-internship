#实现数据提取的功能，调用kimiai.py spider.py UrlToPdf.py来生成.csv文件，记录所提取到的数据
import csv
from kimiai import *
from spider import *
from spider import *
from UrlToPdf import *

# 爬取CVPR 2022 和 CVPR 2023 的论文信息
papers_2022 = scrape_cvpr_papers(2022)
papers_2023 = scrape_cvpr_papers(2023)

#生成pdf
def download_and_save_papers(papers, year):
    count =0
    papers_data=[]
    for i, paper in enumerate(papers, start=1):  # enumerate 默认从 0 开始，加上 start=1 从 1 开始计数
        count+=1
        # if count>=455:
        #     break
        pdf_url = paper['pdf_url']
        if pdf_url:
            try:
                # 1. 下载PDF的第一页
                pdf = download_first_page_pdf(pdf_url)
                
                # 2. 生成输出文件名，例如 2022_1.pdf，2023_2.pdf
                output_filename = f"{year}_{i}.pdf"
                 
                # 3. 保存第一页PDF
                save_first_page_as_pdf(pdf, output_filename)
                
                print(f"Downloaded and saved: {output_filename}")

                paper_info_json=extract_paper_info(output_filename)

                papers_data.append({
                    "title": paper_info_json["title"],
                    "authors": paper_info_json["authors"],
                    'author\'s research institution': paper_info_json["author's research institution"]  # 使用双引号和反斜杠来避免错误
                })

            except Exception as e:
                print(f"Error processing {pdf_url}: {e}")
        else:
            print(f"No URL found for paper {i}")
    return papers_data

def save_to_csv(data, filename):
    # 定义 CSV 文件的列名
    fieldnames = ['title', 'authors', 'author\'s research institution']
    
    # 打开CSV文件以写入数据
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # 写入列名
        writer.writeheader()
        
        # 写入数据
        for row in data:
            writer.writerow(row)

output_filenames = []
import time
for i in range(1, 98):
    filename = f"2022_{i}.pdf"
    output_filenames.append(filename)
for i in range(99, 450):
    filename = f"2022_{i}.pdf"
    output_filenames.append(filename)
papers_data=[]

# 输出生成的文件名列表
for output_filename in output_filenames:
    # time.sleep(1)
    print(output_filename)
    paper_info_json=extract_paper_info(output_filename)
    papers_data.append({
                    "title": paper_info_json["title"],
                    "authors": paper_info_json["authors"],
                    'author\'s research institution': paper_info_json["author's research institution"]  # 使用双引号和反斜杠来避免错误
                })

save_to_csv(papers_data, 'cvpr_2022_papers.csv')


#处理 CVPR 2022 的论文
paper_data_2022=download_and_save_papers(papers_2022, 2022)

#处理 CVPR 2023 的论文
paper_data_2023=download_and_save_papers(papers_2023, 2023)


# 保存数据到CSV文件
save_to_csv(paper_data_2022, 'cvpr_2022_papers.csv')
save_to_csv(paper_data_2023, 'cvpr_2023_papers.csv')

print("Data saved to cvpr_2022_papers.csv and cvpr_2023_papers.csv")

