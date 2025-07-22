from fastapi import APIRouter, HTTPException
from schemas.query import QueryRequest, QueryResponse
from services.simple_vector_db import SimpleVectorDB
from services.retrieval_generator import RetrievalAugmentedGenerator

router = APIRouter()

# 初始化服务
vector_db = SimpleVectorDB()  # 使用简化版向量数据库
rag = RetrievalAugmentedGenerator(vector_db)

@router.post("/", response_model=QueryResponse)
async def query_knowledge_base(query: QueryRequest):
    """向知识库提问"""
    try:
        answer, sources = await rag.generate_answer(
            query.question, 
            top_k=query.top_k
        )
        
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询时出错: {str(e)}")    