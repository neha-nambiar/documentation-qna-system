import boto3
import os
import tempfile
from typing import List, Dict, Any
from unstructured.partition.html import partition_html
from unstructured.chunking.title import chunk_by_title
from unstructured.staging.base import elements_to_json

# Set language to English to avoid detection warnings
os.environ['UNSTRUCTURED_LANGUAGE'] = 'en'

def process_s3_documents(s3_uri: str, chunk_size: int = 2048, overlap: int = 160) -> List[Dict[str, Any]]:
    """Download HTML files from S3, process with Unstructured locally, and return chunks"""
    bucket, prefix = s3_uri[5:].split('/', 1)
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ['S3_AWS_KEY'],
        aws_secret_access_key=os.environ['S3_AWS_SECRET']
    )
    
    # List all HTML files in S3
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    html_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.html')]
    
    all_chunks = []
    total_files = len(html_files)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, s3_key in enumerate(html_files, 1):
            # Download file
            local_path = os.path.join(tmpdir, os.path.basename(s3_key))
            s3_client.download_file(bucket, s3_key, local_path)
            
            # Process with Unstructured
            chunks = _process_html_file(local_path, s3_key, chunk_size, overlap)
            all_chunks.extend(chunks)
            print(f"Processing {i}/{total_files} files...")
    
    print(f"Processed {total_files} files into {len(all_chunks)} chunks")
    return all_chunks

def _process_html_file(file_path: str, source_key: str, chunk_size: int, overlap: int) -> List[Dict[str, Any]]:
    """Process single HTML file with Unstructured"""
    # Partition HTML with English language
    elements = partition_html(filename=file_path, languages=['en'])
    
    # Chunk by title
    chunks = chunk_by_title(
        elements,
        max_characters=chunk_size,
        new_after_n_chars=chunk_size - 200,
        overlap=overlap,
        combine_text_under_n_chars=0
    )
    
    # Convert to structured format
    processed_chunks = []
    for i, chunk in enumerate(chunks):
        processed_chunks.append({
            "text": str(chunk),
            "source": source_key,
            "chunk_id": f"{source_key}_{i}"
        })
    
    return processed_chunks