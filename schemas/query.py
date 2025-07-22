from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, description="用户问题")
    top_k: int = Field(5, ge=1, le=20, description="检索的上下文数量")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="生成的答案")
    sources: list = Field(..., description="参考的文档来源")    