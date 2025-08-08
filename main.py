#!/usr/bin/env python3

import config
from src.firecrawl_client import crawl_and_upload
from src.document_processor import process_s3_documents
from src.mongodb_client import MongoDBClient
from src.embedder import Embedder
from src.retriever import RAGRetriever

def main():
    print("Starting RAG Documentation Pipeline")
    
    # Get crawling parameters from user
    url = input("\nEnter URL to crawl: ").strip()
    limit = int(input("Number of pages to crawl (default 20): ") or "20")
    max_depth = int(input("Max crawl depth (default 5): ") or "5")
    
    # Step 1: Crawl documentation
    print("\nStep 1: Crawling documentation...")
    crawl_result = crawl_and_upload(
        url=url,
        s3_uri=config.S3_BUCKET_URI,
        limit=limit,
        max_crawl_depth=max_depth,
        api_key=config.FIRECRAWL_API_KEY
    )
    print(f"✓ Crawled {crawl_result['file_count']} files to {crawl_result['s3_uri']}")
    
    # Step 2: Process documents
    print("\nStep 2: Processing documents with Unstructured...")
    chunks = process_s3_documents(crawl_result['s3_uri'])
    print(f"✓ Created {len(chunks)} document chunks")
    
    # Step 3: Generate embeddings
    print("\nStep 3: Generating embeddings...")
    embedder = Embedder()
    embedded_chunks = embedder.embed_documents(chunks)
    print(f"✓ Generated embeddings for {len(embedded_chunks)} chunks")
    
    # Step 4: Store in MongoDB
    print("\nStep 4: Storing in MongoDB...")
    mongodb_client = MongoDBClient(
        uri=config.MONGO_URI,
        database=config.MONGO_DATABASE,
        collection=config.MONGO_COLLECTION
    )
    mongodb_client.insert_documents(embedded_chunks)
    print("✓ Documents stored in MongoDB")
    
    # Step 5: RAG Query Interface
    print("\nRAG System Ready!")
    retriever = RAGRetriever(mongodb_client)
    
    # Interactive CLI
    print(f"\nYou can now ask questions about: {url}")
    try:
        while True:
            query = input("\nAsk a question (or 'quit' to exit): ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break
            if not query:
                continue
                
            print("\nSearching...")
            answer, docs = retriever.ask(query)
            print(f"\n**Answer:**\n{answer}\n")
            print("=" * 80)
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    
    mongodb_client.close()
    print("\nSession ended successfully!")

if __name__ == "__main__":
    main()