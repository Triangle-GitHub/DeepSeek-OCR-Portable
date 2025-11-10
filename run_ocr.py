# run_ocr.py
# Fully offline DeepSeek-OCR inference script
# Requirement: models/DeepSeek-OCR/ directory must exist and be complete

import os
import sys
import time
import torch
import shutil
from pathlib import Path
from tkinter import filedialog, Tk

# Automatically locate script directory
SCRIPT_DIR = Path(__file__).parent.resolve()

# Set environment variables for portable Python
env_dir = SCRIPT_DIR / "env"
scripts_dir = env_dir / "Scripts"
library_bin_dir = env_dir / "Library" / "bin"

# Add to PATH
path_list = [str(env_dir), str(scripts_dir), str(library_bin_dir)]
if "PATH" in os.environ:
    path_list.append(os.environ["PATH"])
os.environ["PATH"] = ";".join(path_list)

# Set PYTHONHOME and PYTHONPATH
os.environ["PYTHONHOME"] = str(env_dir)
os.environ["PYTHONPATH"] = str(env_dir / "Lib" / "site-packages")

# Check if model exists
MODEL_PATH = SCRIPT_DIR / "models" / "DeepSeek-OCR"
if not MODEL_PATH.exists():
    print(f"Model directory does not exist: {MODEL_PATH}")
    print("Please ensure the Hugging Face model cache has been copied to this location.")
    sys.exit(1)

print(f"Using local model: {MODEL_PATH}")

# Input/Output configuration
root = Tk()
root.withdraw()
print("Using input image:", end="")
IMAGE_FILE = filedialog.askopenfilename(
    title = "Select image file for OCR",
    filetypes = [
        ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
        ("All files", "*")
    ],
    initialdir=str(SCRIPT_DIR)
)
if not IMAGE_FILE:
    print("\nNo file selected, exiting program")
    sys.exit(1)
IMAGE_FILE = Path(IMAGE_FILE)
print(f" {IMAGE_FILE}")
OUTPUT_DIR = IMAGE_FILE.parent

images_dir_exists_before = (OUTPUT_DIR / "images").exists()

# Record start time
start_time = time.time()

# Load model
print("\n" + "="*60)
print("Loading model...")
try:
    from transformers import AutoModel, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        str(MODEL_PATH),
        trust_remote_code=True,
        local_files_only=True
    )
    model = AutoModel.from_pretrained(
        str(MODEL_PATH),
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
        use_safetensors=True,
        local_files_only=True
    ).eval().cuda()
except Exception as e:
    print(f"Model loading failed: {e}")
    print("Please verify that model files are complete and that the correct versions of transformers/torch are installed.")
    sys.exit(1)

# Inference configuration
PROMPT = "<image>\n<|grounding|>Convert the document to markdown with full structure, including tables, formulas, figures, and references."
IMAGE_SIZE = 1280
BASE_SIZE = 1280
CROP_MODE = False
SAVE_RESULTS = True
TEST_COMPRESS = False
print(f"Starting OCR inference (resolution: {IMAGE_SIZE}x{IMAGE_SIZE})")
print(f"Input: {IMAGE_FILE}")
print(f"Output: {OUTPUT_DIR}")

# Perform OCR
try:
    result = model.infer(
        tokenizer=tokenizer,
        prompt=PROMPT,
        image_file=str(IMAGE_FILE),
        output_path=str(OUTPUT_DIR),
        base_size=BASE_SIZE,
        image_size=IMAGE_SIZE,
        crop_mode=CROP_MODE,
        save_results=SAVE_RESULTS,
        test_compress=TEST_COMPRESS
    )
    input_stem = IMAGE_FILE.stem
    images_dir = OUTPUT_DIR / "images"
    if images_dir.exists() and not images_dir_exists_before:
        shutil.rmtree(images_dir)
    mmd_file = OUTPUT_DIR / "result.mmd"
    md_file = OUTPUT_DIR / f"{input_stem}.md"
    if mmd_file.exists():
        if md_file.exists():
            md_file.unlink()
        mmd_file.rename(md_file)
    boxes_file = OUTPUT_DIR / "result_with_boxes.jpg"
    new_boxes_file = OUTPUT_DIR / f"{input_stem}_with_boxes.jpg"
    if boxes_file.exists():
        if new_boxes_file.exists():
            new_boxes_file.unlink()
        boxes_file.rename(new_boxes_file)
    print("\n" + "="*60)
    print("\nOCR completed! Output files:")
    print(f"  - Markdown: {md_file}")
    print(f"  - Annotated Image: {new_boxes_file}")
except RuntimeError as e:
    if "out of memory" in str(e):
        print("\nOut of memory! Suggestions:")
        print("  → Reduce IMAGE_SIZE to 1024 or 640")
        print("  → Close other GPU-intensive programs")
    else:
        print(f"\nInference error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\nUnknown error: {e}")
    sys.exit(1)

# Record end time and calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time

# Format elapsed time as HH:MM:SS.ms
def format_elapsed_time(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    ms = int((seconds - int(s + m*60 + h*3600)) * 100)
    return f"{h:02d}:{m:02d}:{int(s):02d}.{ms:02d}"
formatted_time = format_elapsed_time(elapsed_time)

print(f"\nExecution time: {formatted_time}")
