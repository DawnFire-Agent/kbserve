#!/usr/bin/env python3
"""
测试脚本 - 测试文档问答系统的各个功能
"""

import requests
import io
import json

# API基础URL
BASE_URL = "http://127.0.0.1:8001"

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
        test_query("什么是Python？")
        test_query("什么是FastAPI？")
    
    print("测试完成!")
