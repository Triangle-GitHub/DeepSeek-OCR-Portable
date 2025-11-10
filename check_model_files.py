# check_models.py
import json
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(script_dir, "models", "DeepSeek-OCR")
json_file = os.path.join(script_dir, "required_model_files.json")

if not os.path.exists(json_file):
    print("ERROR: required_model_files.json not found.")
    sys.exit(2)

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

missing = []
for fname in data.get("files", []):
    fp = os.path.join(models_dir, fname)
    if not os.path.exists(fp):
        missing.append(fname)

print(f"Found {len(missing)} missing file(s).")

sys.exit(0 if len(missing) == 0 else 1)
