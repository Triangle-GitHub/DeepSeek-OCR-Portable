# DeepSeek-OCR Portable

这是一个基于 **DeepSeek-OCR 1280×1280 模式** 构建的**开箱即用的离线 OCR 工具**。无需安装 Python、Miniconda、CUDA 工具包或配置环境变量，只需双击即可享受由深度学习驱动的强大 OCR 体验。

---

## 📋 功能特性

- 支持对图像进行 OCR，包括表格、公式、图表、参考文献等复杂结构
- 输出格式：
  - Markdown 格式的 OCR 结果（`<文件名>.md`）
  - 带有边界框标注的图像（`<文件名>_with_boxes.jpg`）
- **完全离线**运行 — 所有依赖项和模型均已本地打包

---

## 🖥️ 系统要求

- Windows 10 或 Windows 11
- NVIDIA 显卡（显存 ≥ 4GB）
- NVIDIA 驱动版本 ≥ 560.35

---

## 🚀 使用方法

0. 启动 `init.bat` ，进行环境配置及模型下载
1. 双击运行 `run_ocr.bat`
2. 弹出文件选择窗口，选择你想要进行 OCR 的图片
3. 处理完成后，会在原图所在目录生成两个文件：
   - Markdown OCR 结果：`<原文件名>.md`
   - 带边界框的图片：`<原文件名>_with_boxes.jpg`

> 无需安装 Python、Miniconda 或配置环境变量，所有依赖均已包含/自动补全！

---

## 📁 项目结构

```
DeepSeek-OCR Portable/
├── env/                   # 便携式 Python 环境
├── models/                # 模型目录
│   └── DeepSeek-OCR/      # DeepSeek OCR 模型文件（必须存在）
├── run_ocr.bat            # 启动脚本
├── run_ocr.py             # OCR 核心逻辑
└── README.md              # 本文件
```

---

## ⚠️ 注意事项

- 确保 `models/DeepSeek-OCR/` 目录存在且包含完整模型文件，否则程序将无法运行
- 如果遇到显存不足（out of memory）错误，可以尝试：
  - 关闭其他占用显存的程序
  - 在 `run_ocr.py` 中将 `IMAGE_SIZE` 调整为 `1024` 或 `640`
- 当前仅支持 **Windows 系统**，不支持 macOS 或 Linux

---

## 📝 输出示例

假设你选择了一张名为 `document.jpg` 的图片进行 OCR，处理完成后将生成以下两个文件：

- `document.md` — 以 Markdown 格式保存的 OCR 结果
- `document_with_boxes.jpg` — 原图叠加检测框后的图像

---

## 🧠 技术细节

- 使用 HuggingFace 的 `transformers` 库加载本地模型
- 使用 `torch.bfloat16` 降低显存占用
- 使用 `tkinter` 实现文件选择界面
- 所有依赖均已打包在 `env/` 目录中，实现真正的便携性

---

## 📌 开发者说明

你可以在 `run_ocr.py` 中修改以下参数来自定义 OCR 行为：

```python
PROMPT = "<image>\n<|grounding|>Convert the document to markdown with full structure, including "
IMAGE_SIZE = 1280
BASE_SIZE = 1280
CROP_MODE = False
SAVE_RESULTS = True
TEST_COMPRESS = False
```

---

## ❤️ 致谢

本项目基于 [DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR) 构建，感谢 DeepSeek 团队开源此高质量 OCR 模型。

---

欢迎贡献代码、提交问题或改进本项目！
