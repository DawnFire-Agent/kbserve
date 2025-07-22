import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.chunk import Chunk

class SimpleVectorDB:
    """简化的向量数据库实现，不依赖外部模型下载"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.is_fitted = False
        
    def embed_text(self, text: str) -> np.ndarray:
        """将文本转换为向量表示"""
        if not self.is_fitted:
            # 如果还没有拟合，先用当前文本拟合
            self.vectorizer.fit([text])
            self.is_fitted = True
        
        return self.vectorizer.transform([text]).toarray()[0]
    
    async def create_embeddings(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """为多个文本片段创建嵌入"""
        # 收集所有文本用于拟合vectorizer
        texts = [chunk["text"] for chunk in chunks]
        
        # 拟合vectorizer
        self.vectorizer.fit(texts)
        self.is_fitted = True
        
        # 为每个块生成向量
        for chunk in chunks:
            embedding = self.embed_text(chunk["text"])
            chunk["embedding"] = embedding.tolist()
        
        return chunks
    
    async def search(self, query: str, top_k: int = 5) -> List[Tuple[Chunk, float]]:
        """搜索与查询最相似的文本片段"""
        if not self.is_fitted:
            # 如果没有数据，返回空结果
            return []
            
        query_embedding = self.embed_text(query)
        
        # 查询数据库中的所有嵌入
        chunks = await Chunk.all()
        
        if not chunks:
            return []
        
        # 计算查询与所有文本片段的相似度
        similarities = []
        for chunk in chunks:
            chunk_embedding = np.array(chunk.embedding)
            similarity = cosine_similarity([query_embedding], [chunk_embedding])[0][0]
            similarities.append((chunk, similarity))
        
        # 按相似度排序并返回前k个结果
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
