from openai import OpenAI
from typing import List, Dict, Any
import config

class Embedder:
    def __init__(self, model=None):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = model or config.EMBEDDING_MODEL
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for single text"""
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return response.data[0].embedding
    
    def embed_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add embeddings to document chunks"""
        embedded_docs = []
        
        for doc in documents:
            try:
                embedding = self.embed_text(doc["text"])
                doc["embeddings"] = embedding
                embedded_docs.append(doc)
            except Exception as e:
                print(f"Error embedding {doc.get('chunk_id', 'unknown')}: {e}")
        
        print(f"Successfully embedded {len(embedded_docs)} documents")
        return embedded_docs
    
