#本文件实现的功能是将爬取到的Url转换为Pdf文件
import fitz  # PyMuPDF
import requests
from io import BytesIO

def download_first_page_pdf(pdf_url):
    response = requests.get(pdf_url)
    pdf_stream = BytesIO(response.content)
    doc = fitz.open("pdf", pdf_stream)  # 打开PDF文件流
    
    # 保存第一页为单独的PDF文件
    first_page_pdf = fitz.open()
    first_page_pdf.insert_pdf(doc, from_page=0, to_page=0)
    
    return first_page_pdf

def save_first_page_as_pdf(pdf, output_filename):
    pdf.save(output_filename)
    print(f"Saved first page to {output_filename}")

# # 示例：下载并保存PDF的第一页
# pdf_url = "https://openaccess.thecvf.com/content/CVPR2022/papers/Gu_Stochastic_Trajectory_Prediction_via_Motion_Indeterminacy_Diffusion_CVPR_2022_paper.pdf"
# first_page_pdf = download_first_page_pdf(pdf_url)
# save_first_page_as_pdf(first_page_pdf, "Example_Paper_First_Page.pdf")


