from tortoise import fields
from tortoise.models import Model

class Document(Model):
    id = fields.IntField(pk=True)
    filename = fields.CharField(max_length=255)
    file_type = fields.CharField(max_length=200)  # 增加长度以支持长MIME类型
    size = fields.IntField()
    upload_date = fields.DatetimeField(auto_now_add=True)
    processed = fields.BooleanField(default=False)
    chunk_count = fields.IntField(default=0)
    total_tokens = fields.IntField(default=0)
    
    def __str__(self):
        return self.filename    