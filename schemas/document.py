from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

class DocumentBase(BaseModel):
    filename: str
    file_type: str
    size: int
    
    class Config:
        from_attributes = True

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    upload_date: datetime.datetime
    processed: bool
    chunk_count: int
    total_tokens: int

class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int    