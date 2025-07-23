# 文档问答系统API

基于FastAPI、Tortoise ORM和OpenAI的文档问答系统，支持多种文档格式的解析和智能问答。

## 功能特性

- 📄 **多格式支持**: 支持PDF、DOCX、TXT、XLSX、图片等多种文档格式
- 🧠 **智能问答**: 基于RAG（检索增强生成）技术，结合向量搜索和大语言模型
- 🔍 **向量检索**: 使用Sentence Transformers进行文本嵌入和相似度搜索
- 💾 **数据库存储**: 使用Tortoise ORM和SQLite进行数据持久化
- 🚀 **高性能**: 异步处理，支持批量操作
- 🌐 **REST API**: 完整的RESTful API设计
- 📚 **自动文档**: 内置Swagger UI和ReDoc文档

## 技术栈

- **Web框架**: FastAPI
- **数据库**: SQLite + Tortoise ORM
- **AI模型**: OpenAI GPT-3.5/4 + Sentence Transformers
- **文档解析**: pdfplumber、python-docx、openpyxl、pytesseract
- **向量计算**: scikit-learn、numpy

## 快速开始

### 1. 环境准备

```bash
# Python 3.8+
python --version

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制环境变量模板并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置必要的配置：

```env
# OpenAI API密钥（必需）
OPENAI_API_KEY=your_openai_api_key_here

# 数据库URL（可选，默认使用SQLite）
DATABASE_URL=sqlite://db.sqlite3

# 其他配置...
```

### 3. 初始化数据库

```bash
python init_db.py
```

### 4. 启动服务

方式一：使用启动脚本
```bash
./start.sh
```

方式二：直接启动
```bash
uvicorn main:app --reload
```

服务启动后，访问：
- API文档: http://127.0.0.1:8000/docs
- ReDoc文档: http://127.0.0.1:8000/redoc
- 健康检查: http://127.0.0.1:8000/health

## API文档

### 文档管理

#### 上传文档
```http
POST /api/documents/upload
Content-Type: multipart/form-data

file: [文档文件]
```

#### 获取文档列表
```http
GET /api/documents/?limit=10&offset=0
```

#### 获取文档详情
```http
GET /api/documents/{document_id}
```

#### 删除文档
```http
DELETE /api/documents/{document_id}
```

### 问答功能

#### 提问
```http
POST /api/query/
Content-Type: application/json

{
    "question": "你的问题",
    "top_k": 5
}
```

## 项目结构

```
app/
├── main.py                 # 应用主文件
├── requirements.txt        # 依赖列表
├── init_db.py             # 数据库初始化脚本
├── start.sh               # 启动脚本
├── .env.example           # 环境变量模板
├── .env                   # 环境变量配置（需要创建）
├── controllers/           # 控制器层
│   ├── document_controller.py
│   └── query_controller.py
├── models/                # 数据模型
│   ├── document.py
│   └── chunk.py
├── schemas/               # Pydantic schemas
│   ├── document.py
│   └── query.py
└── services/              # 业务逻辑层
    ├── document_parser.py    # 文档解析
    ├── text_processor.py     # 文本处理
    ├── vector_db.py          # 向量数据库
    └── retrieval_generator.py # RAG生成器
```

## 开发指南

### 添加新的文档格式支持

在 `services/document_parser.py` 中：

1. 在 `parse_file` 方法中添加新的文件扩展名判断
2. 实现对应的解析方法 `_parse_new_format`

### 自定义嵌入模型

在 `.env` 文件中设置：

```env
EMBEDDING_MODEL=your_preferred_model_name
```

### 调整文本分段参数

```env
CHUNK_SIZE=500        # 每个文本块的最大token数
CHUNK_OVERLAP=100     # 文本块之间的重叠token数
```

## 部署

### Docker部署（推荐）

```bash
# 构建镜像
docker build -t doc-qa-api .

# 运行容器
docker run -p 8000:8000 -v $(pwd)/.env:/app/.env doc-qa-api
```

### 生产环境部署

1. 使用PostgreSQL替代SQLite
2. 配置Nginx反向代理
3. 使用Gunicorn作为WSGI服务器
4. 配置日志和监控

```bash
# 生产环境启动
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 常见问题

### Q: 如何处理大文件？
A: 系统会自动将大文件分割成小块处理，可以通过环境变量调整块大小。

### Q: 支持哪些图片格式的OCR？
A: 支持JPG、PNG、BMP等常见格式，需要安装Tesseract OCR。

### Q: 如何提高问答准确性？
A: 1. 使用更高质量的文档；2. 调整top_k参数；3. 优化chunk_size参数。

### Q: 数据库迁移怎么处理？
A: 使用Aerich进行数据库迁移管理。

## 贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 更新日志

### v1.0.0 (2025-07-23)
- 初始版本发布
- 支持基本的文档上传和问答功能
- 支持PDF、DOCX、TXT、XLSX、图片格式
- 实现RAG检索增强生成

---

如有问题或建议，请提交 Issue 或联系维护者。
