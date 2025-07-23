from tortoise import fields
from tortoise.models import Model

class Chunk(Model):
    id = fields.IntField(pk=True)
    document = fields.ForeignKeyField("models.Document", related_name="chunks")
    text = fields.TextField()
    start_pos = fields.IntField()
    end_pos = fields.IntField()
    embedding = fields.JSONField()  # 存储向量为JSON数组
    created_at = fields.DatetimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chunk {self.id} from document {self.document_id}"    