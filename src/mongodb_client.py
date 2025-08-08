from pymongo import MongoClient
from typing import List, Dict, Any
import os

class MongoDBClient:
    def __init__(self, uri: str, database: str, collection: str):
        self.client = MongoClient(uri)
        self.db = self.client[database]
        self.collection = self.db[collection]
        print(f"Connected to MongoDB: {database}.{collection}")
    
    def insert_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Insert processed documents into MongoDB"""
        if documents:
            result = self.collection.insert_many(documents)
            print(f"Inserted {len(result.inserted_ids)} documents")
    
    def vector_search(self, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """Perform vector search using MongoDB Atlas Vector Search"""
        pipeline = [
            {
                "$vectorSearch": {
                    "queryVector": query_vector,
                    "path": "embeddings",
                    "numCandidates": 50,
                    "limit": limit,
                    "index": "vector_index"
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        return [{"text": doc["text"], "source": doc.get("source", "")} for doc in results]
    
    def clear_collection(self) -> None:
        """Clear all documents from collection"""
        result = self.collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents")
    
    def close(self) -> None:
        """Close MongoDB connection"""
        self.client.close()