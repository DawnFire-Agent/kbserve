import os
import numpy as np
from typing import List, Dict, Any, Tuple
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from models.chunk import Chunk

class VectorDB:
    def __init__(self, embedding_model_name: str = None):
        self.embedding_model_name = embedding_model_name or os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def _initialize_model(self):
        """延迟初始化嵌入模型，节省资源"""
        if self.model is None:
            self.tokenizer = AutoTokenizer.from_pretrained(self.embedding_model_name)
            self.model = AutoModel.from_pretrained(self.embedding_model_name).to(self.device)
            self.model.eval()
    
    def embed_text(self, text: str) -> np.ndarray:
        """将文本转换为向量表示"""
        self._initialize_model()
        
        # 对文本进行分词
        inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors="pt", max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # 获取模型嵌入
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # 使用[CLS]标记的输出作为文本嵌入
        embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        return embeddings.squeeze()
    
    async def create_embeddings(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """为多个文本片段创建嵌入"""
        for chunk in chunks:
            embedding = self.embed_text(chunk["text"])
            chunk["embedding"] = embedding.tolist()
        return chunks
    
    async def search(self, query: str, top_k: int = 5) -> List[Tuple[Chunk, float]]:
        """搜索与查询最相似的文本片段"""
        query_embedding = self.embed_text(query)
        
        # 查询数据库中的所有嵌入
        chunks = await Chunk.all()
        
        # 计算查询与所有文本片段的相似度
        similarities = []
        for chunk in chunks:
            similarity = cosine_similarity([query_embedding], [np.array(chunk.embedding)])[0][0]
            similarities.append((chunk, similarity))
        
        # 按相似度排序并返回前k个结果
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]    