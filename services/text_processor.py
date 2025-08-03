import re
import os
import tiktoken
from typing import List
from nltk.tokenize import sent_tokenize
import nltk

# 确保NLTK数据已下载，并增强异常提示
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
        nltk.data.find('tokenizers/punkt')
    except Exception as e:
        print("[NLTK punkt] 资源下载失败，请检查网络或手动执行: python -m nltk.downloader punkt")
        raise e

class TextProcessor:
    def __init__(self, 
                 chunk_size: int = None, 
                 overlap: int = None, 
                 model_name: str = "gpt-3.5-turbo"):
        # 从环境变量获取配置，如果没有则使用默认值
        self.chunk_size = chunk_size or int(os.getenv("CHUNK_SIZE", 500))
        self.overlap = overlap or int(os.getenv("CHUNK_OVERLAP", 100))
        self.encoding = tiktoken.encoding_for_model(model_name)
    
    def chunk_text(self, text: str, document_id: int) -> List[dict]:
        """将文本分割成多个重叠的片段，修复死循环和推进问题"""
        chunks = []
        tokens = self.encoding.encode(text)

        if len(tokens) <= self.chunk_size:
            chunks.append({
                "document_id": document_id,
                "text": self.encoding.decode(tokens),
                "start_pos": 0,
                "end_pos": len(tokens)
            })
            return chunks

        start = 0
        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            try:
                # 尝试在句子边界处分割
                decoded_text = self.encoding.decode(tokens[start:end])
                sentences = sent_tokenize(decoded_text)
            except LookupError as e:
                raise RuntimeError("NLTK punkt 资源缺失，请手动执行: python -m nltk.downloader punkt") from e

            # 默认用 chunk_size 分割
            new_end = end
            if len(sentences) > 1:
                # 尝试在最后一个完整句子后分割
                last_full_sent_idx = -1
                total_len = 0
                for i, sent in enumerate(sentences):
                    sent_len = len(self.encoding.encode(sent))
                    if total_len + sent_len <= self.chunk_size * 0.9:
                        last_full_sent_idx = i
                        total_len += sent_len
                    else:
                        break
                if last_full_sent_idx >= 0:
                    end_text = ' '.join(sentences[:last_full_sent_idx+1])
                    end_tokens = self.encoding.encode(end_text)
                    new_end = start + len(end_tokens)
            # 防止死循环：如果分句分割无效或推进太少，强制推进
            if new_end <= start:
                new_end = min(start + self.chunk_size, len(tokens))
            chunk_text = self.encoding.decode(tokens[start:new_end])
            chunks.append({
                "document_id": document_id,
                "text": chunk_text,
                "start_pos": start,
                "end_pos": new_end
            })
            # 计算下一个块的起始位置（考虑重叠）
            # 保证 start 一定推进
            next_start = max(start + self.chunk_size - self.overlap, new_end - self.overlap)
            if next_start <= start:
                next_start = start + self.chunk_size  # 兜底推进
            start = next_start
        return chunks
    
    def clean_text(self, text: str) -> str:
        """清理文本，去除多余空格和特殊字符"""
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
        # 去除tab符号
        text = re.sub(r'\t+', ' ', text)
        return text    