<div align="center">

# 📚 DocsChat

[![OpenAI](https://img.shields.io/badge/OpenAI-4A4A55?style=for-the-badge&logo=openai)](https://openai.com)
[![MongoDB](https://img.shields.io/badge/-MongoDB-13aa52?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Firecrawl](https://img.shields.io/badge/Firecrawl-orange?style=for-the-badge)](https://firecrawl.dev)
[![Unstructured](https://img.shields.io/badge/Unstructured-purple?style=for-the-badge)](https://unstructured.io)
[![AWS S3](https://img.shields.io/badge/AWS%20S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3)

*Crawl → Process → Embed → Query*

</div>

Transforms any website's documentation into an intelligent, conversational assistant. Simply provide a documentation URL, get answers to questions about a specific library or framework.

**🎯 For developers who want to:**
- Quickly understand new frameworks and libraries
- Get instant answers from complex documentation
- Save time searching through lengthy docs
- Have contextual conversation about code

## Technology Stack

- **[Firecrawl](https://firecrawl.dev)** -  LLM-Ready web crawling
- **[Unstructured](https://unstructured.io)** - Document processing and intelligent chunking
- **[MongoDB Atlas](https://mongodb.com/atlas)** - Vector database with similarity search
- **[OpenAI](https://openai.com)** - Embeddings (text-embedding-3-large) and generation (gpt-4o-mini)
- **[AWS S3](https://aws.amazon.com/s3)** - Temporary storage for crawled content

## Demo

[https://github.com/user-attachments/assets/demo.mp4](https://github.com/user-attachments/assets/e24b8461-b1b3-48b8-8071-1641ecc86113)

## Setup

### 1. Clone & Install
```bash
git clone <repository-url>
cd rag_documentation
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Add your API keys to .env file
```

### 3. Run DocsChat
```bash
python main.py
```

### 4. Choose Your Documentation
**Popular examples:**
- 🔗 **React**: `https://react.dev/learn`
- 🔗 **FastAPI**: `https://fastapi.tiangolo.com`
- 🔗 **LangGraph**: `https://docs.langchain.com/langgraph-platform`
- 🔗 **Next.js**: `https://nextjs.org/docs`

### 5. Start Asking Questions!
```
💭 "How do I create a state graph in LangGraph?"
💭 "What are React hooks and how do I use them?"
💭 "How do I handle authentication in FastAPI?"
💭 "What's the difference between SSR and SSG in Next.js?"
```

## 🔧 Configuration

| Parameter | Description | Default |
|-----------|-------------|----------|
| `limit` | Number of pages to crawl | 20 |
| `max_depth` | Maximum crawl depth | 5 |
| `embedding_model` | OpenAI embedding model | text-embedding-3-large |
| `generation_model` | OpenAI chat model | gpt-4o-mini |

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- MongoDB Atlas cluster
- AWS S3 bucket
- Firecrawl API key
