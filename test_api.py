#!/usr/bin/env python3
"""
测试脚本 - 测试文档问答系统的各个功能
"""

import requests
import io
import json

# API基础URL
BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """测试健康检查"""
    print("=== 测试健康检查 ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_root():
    """测试根路径"""
    print("=== 测试根路径 ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_document_list():
    """测试文档列表"""
    print("=== 测试文档列表 ===")
    response = requests.get(f"{BASE_URL}/api/documents/")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_upload_document():
    """测试上传文档"""
    print("=== 测试文档上传 ===")
    
    # 创建一个简单的文本文件
    text_content = """
    这是一个测试文档。
    
    文档包含了一些基本信息：
    1. Python是一种编程语言
    2. FastAPI是一个Web框架
    3. 机器学习是人工智能的一个分支
    
    这个文档用于测试文档问答系统的功能。
    文档上传成功后，系统应该能够解析并存储这些信息。
    请各位处长包括各位分管领导，前期办公室全面梳理了一下，从去年开始一直到今年当下。
    我们通过各种形式出台的行动方案，有的是市委市政府主要领导圈过的，有的是市政府常务会议通过的，有的是刘市长专门研究的。
    请大家今年务必行动起来，否则就是一个方案。
    二，也再梳理一下吉宁书记就有关领域布局做出的圈阅或者指示，请办公室和规划处列个清单，请各位专业处室、分管领导就这些重要领域的布局今年一定要有所动作。
    按照吉宁书记现在的要求，一个月之后就开始督查，如果我们做了行动方案没行动，到年底是很难交账的。
    前期做行动方案的时候大家发了很多心思，真正到我们该行动的时候不行动，或者行动得不全面、不细。
    就像今天上午我们在研究养老科技的时候，有的行动是用指南的方式，有的行动可能是要和区里面联动的方式，但是整体呈现要呈现体系化、系统的布局，不能单单呈现面向招标的那几个项目，那几个项目不支撑整个行动.
    """
    
    # 准备文件上传
    files = {
        'file': ('test_document.txt', io.StringIO(text_content), 'text/plain')
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/documents/upload", files=files)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"上传失败: {e}")
        return None
    print()

def test_query(question="什么是Python？"):
    """测试问答功能"""
    print(f"=== 测试问答功能 ===")
    print(f"问题: {question}")
    
    data = {
        "question": question,
        "top_k": 3
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/query/",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"查询失败: {e}")
    print()

if __name__ == "__main__":
    print("开始测试文档问答系统API...")
    print("=" * 50)
    
    # 基础测试
    test_health()
    test_root()
    test_document_list()
    
    # 文档上传测试
    uploaded_doc = test_upload_document()
    
    # 如果上传成功，再次检查文档列表
    if uploaded_doc:
        print("上传成功后的文档列表:")
        test_document_list()
        
        # 测试问答功能
        # test_query("什么是Python？")
        # test_query("什么是FastAPI？")
    
    print("测试完成!")
