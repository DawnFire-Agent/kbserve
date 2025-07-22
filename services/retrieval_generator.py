import os
import tiktoken
from typing import List, Tuple
from openai import OpenAI
from models.chunk import Chunk
from models.document import Document

class RetrievalAugmentedGenerator:
    def __init__(self, vectordb, model_name: str = "gpt-3.5-turbo"):
        self.vectordb = vectordb
        self.model_name = model_name
        self.encoding = tiktoken.encoding_for_model(model_name)
        
        # 初始化OpenAI客户端
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not set in environment variables")
        self.client = OpenAI(api_key=api_key) if api_key else None
    
    async def generate_answer(self, question: str, top_k: int = 5, max_context_tokens: int = 3000) -> Tuple[str, List[dict]]:
        """结合检索结果和大模型生成答案"""
        # 检索相关上下文
        results = await self.vectordb.search(question, top_k=top_k)
        
        # 构建上下文
        context = ""
        context_tokens = 0
        sources = []
        for chunk, score in results:
            document = await Document.get(id=chunk.document_id)
            chunk_text = f"来源: {document.filename} (位置: {chunk.start_pos}-{chunk.end_pos})\n内容: {chunk.text}\n\n"
            chunk_tokens = len(self.encoding.encode(chunk_text))
            
            if context_tokens + chunk_tokens <= max_context_tokens:
                context += chunk_text
                context_tokens += chunk_tokens
                
                # 记录来源
                sources.append({
                    "document_id": document.id,
                    "filename": document.filename,
                    "chunk_id": chunk.id,
                    "start_pos": chunk.start_pos,
                    "end_pos": chunk.end_pos,
                    "similarity_score": score
                })
            else:
                break
        
        # 构建提示词
        prompt = f"""基于以下知识库内容回答问题：
        {context}
        
        问题: {question}
        回答: """
        
        # 调用大模型生成答案
        try:
            if not self.client:
                return "错误：未配置OpenAI API密钥。请设置OPENAI_API_KEY环境变量。", []
                
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一个知识渊博的助手，能够基于提供的知识库准确回答问题。如果知识库中没有相关信息，请如实说明。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip(), sources
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "抱歉，生成答案时出错。请重试或检查您的API密钥。", []    