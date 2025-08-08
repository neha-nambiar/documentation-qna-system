# RAG Documentation System

A Retrieval-Augmented Generation documentation assistant for websites. Crawls documentation content, creates vector embeddings, and provides query-based retrieval for accurate answer generation. The system retrieves relevant documentation chunks based on semantic similarity, then uses them as context for LLM answer generation.

## Implementation

- Local document processing with Unstructured library
- OpenAI embeddings (text-embedding-3-small) and generation (gpt-3.5-turbo)
- MongoDB Atlas vector search with cosine similarity
- Firecrawl for web content extraction
- AWS S3 for temporary HTML storage

## Technology Stack

- **Firecrawl**: Professional web crawling with smart content extraction
- **Unstructured**: Local AI-powered document processing
- **MongoDB Atlas**: Vector database with similarity search
- **OpenAI**: Embeddings and natural language generation
- **AWS S3**: Temporary storage for crawled content

## Workflow

```
Website → Firecrawl → S3 → Unstructured → MongoDB → Interactive Q&A
```

1. **Crawl**: Extract documentation from target website
2. **Store**: Upload raw HTML files to S3 for processing
3. **Process**: Parse HTML and create semantic chunks locally
4. **Embed**: Generate vector representations of content
5. **Index**: Store in MongoDB with vector search capabilities
6. **Query**: Interactive CLI for natural language questions

Vector similarity search enables retrieval of relevant documentation chunks, which serve as context for generating accurate, source-grounded responses.

**Output**: Answers are grounded in the actual documentation content and include contextual information from the crawled source material.

## Demo

[https://github.com/user-attachments/assets/demo.mp4](https://github.com/user-attachments/assets/e24b8461-b1b3-48b8-8071-1641ecc86113)

## Usage

Run `python main.py` and provide the documentation URL when prompted. Configure crawling parameters (page limit, max depth) to control the scope of content extraction. The system will crawl the documentation site and create a documentation assistant for that specific library.

**Examples:**
- For LangGraph questions: `https://docs.langchain.com/langgraph-platform`
- For React questions: `https://react.dev/learn`
- For FastAPI questions: `https://fastapi.tiangolo.com`

Once processing is complete, ask questions like:
- "How do I create a state graph in LangGraph?"
- "What are React hooks and how do I use them?"
- "How do I handle authentication in FastAPI?"
