# DeepSeek-OCR Portable

This is an **easy-to-use offline OCR tool** based on the **DeepSeek-OCR 1280×1280 mode**. It allows users to perform OCR without installing Python, Miniconda, CUDA Toolkit, or configuring environment variables. Just double-click and enjoy the powerful OCR experience powered by deep learning.

---

## 📋 Features

- Performs OCR on images, including complex structures like tables, formulas, figures, and references
- Output formats:
  - Markdown OCR result (`<filename>.md`)
  - Annotated image with bounding boxes (`<filename>_with_boxes.jpg`)
- **Fully offline** — all dependencies and models are bundled locally

---

## 🖥️ System Requirements

- Windows 10 or Windows 11
- NVIDIA GPU (≥ 4GB VRAM)
- NVIDIA Driver ≥ 560.35

---

## 🚀 How to Use

0. Double-click  `init.bat`,it will initialize the environments and download the model 
1. Double-click `run_ocr.bat`
2. A file dialog will appear — select the image you want to OCR
3. After processing, two files will be saved in the same directory as the original image:
   - Markdown OCR result: `<original_filename>.md`
   - Image with bounding boxes: `<original_filename>_with_boxes.jpg`

> No need to install Python, Miniconda, or configure environment variables — everything is self-contained!

---

## 📁 Project Structure

```
DeepSeek-OCR Portable/
├── env/                   # Portable Python environment
├── models/                # Model directory
│   └── DeepSeek-OCR/      # DeepSeek OCR model files (must exist)
├── run_ocr.bat            # Launch script
├── run_ocr.py             # Core OCR logic
└── README.md              # This file
```

---

## ⚠️ Notes

- Make sure the `models/DeepSeek-OCR/` directory exists and contains complete model files; otherwise, the program will fail
- If you encounter an "out of memory" error, try:
  - Closing other GPU-intensive programs
  - Reducing the `IMAGE_SIZE` in `run_ocr.py` to `1024` or `640`
- This tool currently only supports **Windows**, not macOS or Linux

---

## 📝 Example Output

Suppose you select an image named `document.jpg`. After OCR processing, the following files will be generated:

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

You can customize the OCR behavior by modifying the following settings in `run_ocr.py`:

```python
PROMPT = "<image>\n<|grounding|>Convert the document to markdown with full structure, including tables, formulas, figures, and references."
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
