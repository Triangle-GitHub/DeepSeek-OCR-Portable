"""
DeepSeek-OCR Model Downloader
Download DeepSeek-OCR model files from ModelScope into ./models
"""

import sys
import requests
from pathlib import Path
from tqdm import tqdm
import json
import time

with open('required_model_files.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    REQUIRED_FILES = config['files']
    MODEL_FILES_URL = config['base_url']

def download_file(url, destination, max_retries=3):
    """Download a single file - skip if exists."""
    
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    if destination.exists():
        print(f"✓ {destination.name} already exists, skipping")
        return True
    
    temp_file = destination.with_name(destination.name + ".tmp")
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")

            total_size = int(response.headers.get('content-length', 0))

            with open(temp_file, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=destination.name) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            if total_size > 0 and temp_file.stat().st_size != total_size:
                raise Exception("File size mismatch")

            temp_file.rename(destination)
            return True

        except Exception as e:
            print(f"\nDownload failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"   Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed to download {destination.name}")
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
    print("Fetching file list...")
    file_list = REQUIRED_FILES
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
        
        print(f"\nDownloading: {filename}")
        if download_file(download_url, destination):
            print(f"✓ Done: {filename}")
            success_count += 1
        else:
            failed_files.append(filename)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Completed: {success_count}/{len(file_list)} files")
    
    if failed_files:
        print(f"\nFailed files:")
        for f in failed_files:
            print(f"   - {f}")
        print("\nTips:")
        print("   1. Re-run this script to continue downloading")
        print(f"   2. Manually download from {MODEL_FILES_URL}")
        return False
    else:
        print("\nAll files downloaded successfully!")
        return True


if __name__ == "__main__":
    try:
        success = download_models()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDownload canceled")
        sys.exit(1)
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
