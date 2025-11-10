# DeepSeek-OCR Portable

This is an **easy-to-use offline OCR tool** based on the **DeepSeek-OCR 1280×1280 mode**. It allows users to perform OCR without installing Python, Miniconda, CUDA Toolkit, or configuring environment variables. Just double-click and enjoy the powerful OCR experience powered by deep learning.

---

## 📋 Features

- Performs OCR on images, including complex structures like tables, formulas, figures, and references
- Output formats:
  - Markdown OCR result (`<filename>.md`)
  - Annotated image with bounding boxes (`<filename>_with_boxes.jpg`)
- **"Green software" mode** — All dependencies and models require no manual downloads; fully offline after initial setup

---

## 🖥️ System Requirements

- Windows 10 or Windows 11
- NVIDIA GPU (≥ 4GB VRAM)
- NVIDIA Driver ≥ 560.35

---

## 🚀 How to Use

1. Double-click `init.bat` (First run requires downloading models and dependencies - may take significant time)
2. A file selection window will appear — select the image you want to OCR
3. After processing, two files will be generated in the original image's directory:
   - Markdown OCR result: `<original_filename>.md`
   - Image with bounding boxes: `<original_filename>_with_boxes.jpg`

> No need to install Python, Miniconda, or configure environment variables — all dependencies are automatically resolved!

---

## 📁 Project Structure

```
DeepSeek-OCR Portable/
├── env/                      # Portable Python environment
├── models/
│   └── DeepSeek-OCR/         # DeepSeek OCR model files
├── init.bat                  # One-click launch script (double-click to run)
├── run_ocr.bat               # Quick offline launch script (requires pre-downloaded models)
├── requirements.txt          # Python dependencies list
├── required_model_files.json # Model file list
├── check_model_files.py      # Model file existence checker
├── download_model_files.py   # Model download script
├── run_ocr.py                # OCR core logic
├── README.md                 # Documentation
├── README_zh.md              # Chinese documentation
└── LICENSE                   # MIT License
```

---

## ⚠️ Notes

- Initial download may be slow (~10GB) — please be patient
- If encountering "out of memory" errors:
  - Close other GPU-intensive applications
  - Modify `IMAGE_SIZE` in `run_ocr.py` to `1024` or `640`
- Currently **Windows-only** (no macOS/Linux support)
- **NVIDIA GPU required** (CUDA 12.8 based) — AMD GPUs or CPU execution not supported

---

## 📝 Example Output

Suppose you select an image named `document.jpg`. After OCR processing, the following files will be generated in the original image's directory:

- `document.md` — OCR result in Markdown format
- `document_with_boxes.jpg` — Original image with detection boxes overlaid

---

## 🧠 Technical Details

- Uses HuggingFace's `transformers` library to load local models
- Uses `torch.bfloat16` to reduce GPU memory usage
- Uses `tkinter` for file selection UI
- All dependencies are bundled in the `env/` directory for true portability

---

## 📌 Developer Notes

You can customize the OCR behavior by modifying these parameters in `run_ocr.py`:

```python
PROMPT = "<image>\n<|grounding|>Convert the document to markdown with full structure, including "
IMAGE_SIZE = 1280
BASE_SIZE = 1280
CROP_MODE = False
SAVE_RESULTS = True
TEST_COMPRESS = False
```

---

## ❤️ Acknowledgments

This project is built based on [DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR). Special thanks to the DeepSeek team for open-sourcing this high-quality OCR model.

---

Feel free to contribute, report issues, or improve this project!