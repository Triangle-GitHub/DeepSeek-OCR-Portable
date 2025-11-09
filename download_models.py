"""
DeepSeek-OCR Model Downloader
Download DeepSeek-OCR model files from ModelScope into ./models
"""

import os
import sys
import requests
from pathlib import Path
from tqdm import tqdm
import json
import time

# ModelScope API base URL
MODELSCOPE_API = "https://www.modelscope.cn/models/deepseek-ai/DeepSeek-OCR/files"
MODEL_FILES_URL = "https://www.modelscope.cn/models/deepseek-ai/DeepSeek-OCR/files"

# Files to download (explicit list from provided repository snapshot)
REQUIRED_FILES = [
    ".gitattributes",
    "config.json",
    "configuration.json",
    "configuration_deepseek_v2.py",
    "conversation.py",
    "deepencoder.py",
    "LICENSE",
    "model-00001-of-000001.safetensors",
    "model.safetensors.index.json",
    "modeling_deepseekocr.py",
    "modeling_deepseekv2.py",
    "processor_config.json",
    "README.md",
    "special_tokens_map.json",
    "tokenizer.json",
    "tokenizer_config.json"
]

def get_file_list():
    """Fetch file list from ModelScope API."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    # Try to fetch the file list via API
        response = requests.get(MODELSCOPE_API, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'Data' in data and isinstance(data['Data'], list):
                return [item['Path'] for item in data['Data'] if 'Path' in item]
        
        print(f"⚠️  Unable to fetch file list via API (status code: {response.status_code})")
        print("   Falling back to predefined file list...")
        return REQUIRED_FILES
        
    except Exception as e:
        print(f"⚠️  Error while fetching file list: {e}")
        print("   Falling back to predefined file list...")
        return REQUIRED_FILES


def download_file(url, destination, max_retries=3):
    """Download a single file with resume support and retries."""
    
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Check local partial file for resuming
    resume_header = {}
    initial_pos = 0
    if destination.exists():
        initial_pos = destination.stat().st_size
        resume_header = {'Range': f'bytes={initial_pos}-'}
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers={**headers, **resume_header}, 
                                   stream=True, timeout=30)
            
            # Restart from scratch if server doesn't support range requests
            if response.status_code == 416 or (response.status_code == 200 and initial_pos > 0):
                initial_pos = 0
                response = requests.get(url, headers=headers, stream=True, timeout=30)
            
            if response.status_code not in [200, 206]:
                raise Exception(f"HTTP {response.status_code}")
            
            total_size = int(response.headers.get('content-length', 0)) + initial_pos
            
            mode = 'ab' if initial_pos > 0 and response.status_code == 206 else 'wb'
            
            with open(destination, mode) as f:
                with tqdm(total=total_size, initial=initial_pos, 
                         unit='B', unit_scale=True, 
                         desc=destination.name) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            
            # Validate file size
            if total_size > 0 and destination.stat().st_size != total_size:
                raise Exception("File size mismatch")
            
            return True
            
        except Exception as e:
            print(f"\n⚠️  Download failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"   Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"❌ Failed to download {destination.name}")
                return False
    
    return False


def download_models():
    """Download all required model files."""
    
    models_dir = Path("./models/DeepSeek-OCR")
    models_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("DeepSeek-OCR Model Downloader")
    print("=" * 60)
    print(f"Target directory: {models_dir.absolute()}\n")
    
    # Get file list
    print("📋 Fetching file list...")
    file_list = get_file_list()
    print(f"✓ Found {len(file_list)} files\n")
    
    # Download files
    success_count = 0
    failed_files = []
    
    for filename in file_list:
    # Build download URL (ModelScope API)
        download_url = f"https://www.modelscope.cn/api/v1/models/deepseek-ai/DeepSeek-OCR/repo?Revision=master&FilePath={filename}"
        
        destination = models_dir / filename
        
        # Skip if exists
        if destination.exists():
            print(f"✓ {filename} already exists, skipping")
            success_count += 1
            continue
        
        print(f"\n📥 Downloading: {filename}")
        if download_file(download_url, destination):
            print(f"✓ Done: {filename}")
            success_count += 1
        else:
            failed_files.append(filename)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Completed: {success_count}/{len(file_list)} files")
    
    if failed_files:
        print(f"\n❌ Failed files:")
        for f in failed_files:
            print(f"   - {f}")
        print("\n💡 Tips:")
        print("   1. Re-run this script to continue downloading")
        print(f"   2. Manually download from {MODEL_FILES_URL}")
        return False
    else:
        print("\n✅ All files downloaded successfully!")
        return True


if __name__ == "__main__":
    try:
        success = download_models()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Download canceled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
