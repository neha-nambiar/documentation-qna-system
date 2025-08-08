import os
from dotenv import load_dotenv

load_dotenv()

# Firecrawl
FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')

# AWS S3
S3_AWS_KEY = os.getenv('S3_AWS_KEY')
S3_AWS_SECRET = os.getenv('S3_AWS_SECRET')
S3_BUCKET_URI = os.getenv('S3_BUCKET_URI')

# MongoDB
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODEL = "text-embedding-3-large"  
GENERATION_MODEL = "gpt-4o-mini"  