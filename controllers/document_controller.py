from fastapi import APIRouter, File, UploadFile, HTTPException
from models.document import Document
from models.chunk import Chunk
from schemas.document import DocumentResponse, DocumentListResponse
from services.document_parser import DocumentParser
from services.text_processor import TextProcessor
from services.simple_vector_db import SimpleVectorDB
from tortoise.transactions import in_transaction

router = APIRouter()

# 初始化服务
document_parser = DocumentParser()
text_processor = TextProcessor()
vector_db = SimpleVectorDB()  # 使用简化版向量数据库

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """上传并处理文档"""
    # 读取文件内容以获取大小
    file_contents = await file.read()
    file_size = len(file_contents)
    
    # 重置文件指针
    await file.seek(0)
    
    # 保存文档信息
    async with in_transaction():
        doc = await Document.create(
            filename=file.filename,
            file_type=file.content_type or "application/octet-stream",
            size=file_size
        )
        
        try:
            # 解析文档内容
            text = document_parser.parse_uploaded_file(file)
            # print(f"解析后的文本长度: {(text)}")
            cleaned_text = text_processor.clean_text(text)
            print(f"清理后的文本: {cleaned_text}")
            
            if not cleaned_text.strip():
                await doc.delete()
                raise HTTPException(status_code=400, detail="文档内容为空或无法解析")
            
            # 文本分段
            chunks = text_processor.chunk_text(cleaned_text, doc.id)
            print(f"分段: {chunks}")
            
            if not chunks:
                await doc.delete()
                raise HTTPException(status_code=400, detail="文档分段失败")
            
            # 生成嵌入
            chunks_with_embeddings = await vector_db.create_embeddings(chunks)
            
            # 保存所有片段
            chunk_objects = []
            for chunk_data in chunks_with_embeddings:
                chunk_objects.append(Chunk(
                    document_id=doc.id,
                    text=chunk_data["text"],
                    start_pos=chunk_data["start_pos"],
                    end_pos=chunk_data["end_pos"],
                    embedding=chunk_data["embedding"]
                ))
            
            # 批量创建
            await Chunk.bulk_create(chunk_objects)
            
            # 更新文档处理状态
            doc.processed = True
            doc.chunk_count = len(chunks)
            doc.total_tokens = sum(len(text_processor.encoding.encode(chunk["text"])) for chunk in chunks)
            await doc.save()
            
            return doc
        except Exception as e:
            # 出错时回滚
            await doc.delete()
            raise HTTPException(status_code=500, detail=f"处理文档时出错: {str(e)}")

@router.get("/", response_model=DocumentListResponse)
async def list_documents(limit: int = 10, offset: int = 0):
    """列出所有文档"""
    documents = await Document.all().limit(limit).offset(offset)
    total = await Document.all().count()
    return {"documents": documents, "total": total}

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int):
    """获取单个文档信息"""
    doc = await Document.get_or_none(id=document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")
    return doc

@router.delete("/{document_id}", response_model=dict)
async def delete_document(document_id: int):
    """删除文档及其所有片段"""
    doc = await Document.get_or_none(id=document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    # 删除相关片段
    await Chunk.filter(document_id=document_id).delete()
    
    # 删除文档
    await doc.delete()
    
    return {"message": "文档已成功删除"}    