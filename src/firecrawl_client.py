import time
import tempfile
import boto3
import hashlib
import os
from typing import Dict, Any
from firecrawl import FirecrawlApp
from firecrawl.firecrawl import ScrapeOptions

def crawl_and_upload(url: str, s3_uri: str, limit: int = 20, max_crawl_depth: int = 5, 
                    api_key: str = None, timeout: int = 3600) -> Dict[str, Any]:
    """Crawl website and upload results to S3"""
    if not api_key:
        raise ValueError("Firecrawl API key is required")
    
    if not s3_uri.startswith("s3://"):
        raise ValueError("S3 URI must start with 's3://'")
    
    s3_uri = s3_uri if s3_uri.endswith("/") else s3_uri + "/"
    
    firecrawl = FirecrawlApp(api_key=api_key)
    job = firecrawl.async_crawl_url(
        url, 
        limit=limit, 
        max_discovery_depth=max_crawl_depth, 
        scrape_options=ScrapeOptions(formats=["html"])
    )
    
    job_id = job.id
    start = time.time()
    
    while True:
        status = firecrawl.check_crawl_status(job_id)
        if status.status == "completed":
            break
        if time.time() - start > timeout:
            return {"id": job_id, "status": "timeout", "error": "Job timed out."}
        print(f"Job status: {status.status}. Waiting 30s...")
        time.sleep(30)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        job_dir = os.path.join(tmpdir, job_id)
        os.makedirs(job_dir, exist_ok=True)
        file_count = _save_html_files(status, job_dir)
        upload_stats = _upload_to_s3(job_dir, s3_uri + job_id + "/")
    
    return {
        "id": job_id,
        "status": "completed",
        "s3_uri": s3_uri + job_id + "/",
        "file_count": file_count,
        **upload_stats
    }

def _save_html_files(status_response, output_dir: str) -> int:
    """Save crawled HTML files to directory"""
    count = 0
    crawled_urls = []
    
    for i, page in enumerate(status_response.data or []):
        html = getattr(page, 'html', None)
        if not html:
            continue
        metadata = getattr(page, 'metadata', {})
        url = metadata.get('url', f"page-{i}")
        crawled_urls.append(url)
        filename = _clean_url_to_filename(url)
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
    
    print("Crawled pages:")
    for url in crawled_urls:
        print(f"  - {url}")
    
    return count

def _upload_to_s3(local_dir: str, s3_uri: str) -> Dict[str, Any]:
    """Upload directory to S3"""
    bucket, prefix = s3_uri[5:].split('/', 1)
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ['S3_AWS_KEY'],
        aws_secret_access_key=os.environ['S3_AWS_SECRET']
    )
    
    stats = {"uploaded_files": 0, "failed_files": 0, "total_bytes": 0}
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_dir)
            s3_key = os.path.join(prefix, relative_path).replace("\\", "/")
            try:
                s3_client.upload_file(local_path, bucket, s3_key)
                stats["uploaded_files"] += 1
                stats["total_bytes"] += os.path.getsize(local_path)
            except Exception as e:
                print(f"Error uploading {local_path}: {str(e)}")
                stats["failed_files"] += 1
    
    print(f"Successfully uploaded {stats['uploaded_files']} files to S3")
    return stats

def _clean_url_to_filename(url: str) -> str:
    """Convert URL to valid filename"""
    filename = url.replace("https://", "").replace("http://", "")
    filename = filename.replace("/", "_").replace("?", "_").replace("&", "_").replace(":", "_")
    if len(filename) > 200:
        domain = filename.split('_')[0]
        filename_hash = hashlib.md5(url.encode()).hexdigest()
        return f"{domain}_{filename_hash}.html"
    return f"{filename}.html"