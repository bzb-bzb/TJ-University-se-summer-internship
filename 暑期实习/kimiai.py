# 本文件的内容是提供一个可以调用kimiai api-key的函数，
# 输入参数为pdf文件名称，输出为json格式的数据，从pdf文件中提取出文章标题，文章作者，作者单位信息。

from pathlib import Path
from openai import OpenAI
import json

api_key = ""
base_url = "https://api.moonshot.cn/v1"

# 初始化OpenAI客户端
client = OpenAI(api_key=api_key, base_url=base_url)

def extract_paper_info(pdf_file_path):    
    # 创建文件并上传
    file_object = client.files.create(file=Path(pdf_file_path), purpose="file-extract")
    
    # 获取文件内容
    file_content = client.files.content(file_id=file_object.id).text
    
    # 准备发送给模型的消息
    messages = [
        {
            "role": "system",
            "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手..."
        },
        {
            "role": "system",
            "content": file_content
        },
        {
            "role": "user",
            "content": "请简单介绍本pdf文件中论文的标题，作者，以及作者单位信息，返回的信息为json格式，即title: authors: author's research institution:"
        }
    ]
    
    # 调用chat-completion获取回答
    completion = client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=messages,
        temperature=0.3,
    )
    
    # 解析回答并返回JSON格式的信息
    response_content = completion.choices[0].message.content
    try:
        paper_info = json.loads(response_content)
        return paper_info
    except json.JSONDecodeError:
        print("返回的内容不是有效的JSON格式")
        return None

# # 使用示例
# pdf_path = "Example_Paper_First_Page.pdf"
# paper_info_json = extract_paper_info(pdf_path)

#该部分代码用于删除已经上传的文件（文件只允许上传不超过1000个）
file_list = client.files.list()
 
for file in file_list.data:
	client.files.delete(file_id=file.id)
