from openai import OpenAI
from typing import List, Dict, Any
import config
from .mongodb_client import MongoDBClient
from .embedder import Embedder

class RAGRetriever:
    def __init__(self, mongodb_client: MongoDBClient, embedding_model=None, generation_model=None):
        self.mongodb_client = mongodb_client
        self.embedder = Embedder(model=embedding_model)
        self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.generation_model = generation_model or config.GENERATION_MODEL
    
    def retrieve_documents(self, query: str, n: int = 10) -> str:
        """Retrieve relevant documents for query"""
        query_embedding = self.embedder.embed_text(query)
        results = self.mongodb_client.vector_search(query_embedding, limit=n)
        
        return "\n".join([
            f"\n\n===== Document {i+1} =====\n{doc['text']}" 
            for i, doc in enumerate(results)
        ])
    
    def generate_answer(self, query: str, retrieved_docs: str) -> str:
        """Generate answer using retrieved documents"""
        prompt = f"""
---

### Retrieved Documentation:
{retrieved_docs}

Analyse the retrieved docs, and then take the user's question, retrieved documents and suggest an answer based on the context provided. You can use your understanding of the retrieved documents to build on top and answer the user's question.

Respond in clear **Markdown**. Use code blocks where relevant. Make sure the code is syntactically accurate and the content very relevant.

---

### User Question:
{query}
"""
        
        response = self.openai_client.chat.completions.create(
            model=self.generation_model,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def ask(self, question: str) -> tuple[str, str]:
        """Complete RAG pipeline: retrieve and generate"""
        retrieved_docs = self.retrieve_documents(question)
        answer = self.generate_answer(question, retrieved_docs)
        return answer, retrieved_docs