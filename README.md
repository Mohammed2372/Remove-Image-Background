# Background Remover GUI Application 🖼️✂️

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A user-friendly desktop application that removes backgrounds from images with just a few clicks. Built with Python, this tool features an intuitive drag-and-drop interface and allows you to save processed images with transparent backgrounds.

## ✨ Features

- **Easy Image Loading**

  - Drag-and-drop interface (Windows)
  - File browser selection

- **Powerful Processing**

  - Automatic background removal using AI (rembg library)
  - Side-by-side preview of original and processed images

- **Flexible Output**
  - Save results as PNG with transparent background
  - Maintain original image quality

## 📋 Requirements

- Python 3.8 or higher
- pip package manager

## 🚀 Getting Started

### Installation

1. Clone this repository or download the source code:

   ```bash
   git clone https://github.com/Mohammed2372/Remove-Image-Background.git
   cd Remove-Image-Background
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   > **Important:** Always run this command before running the application to ensure all required dependencies are installed.

### Running the Application

```bash
python rembg_program.py
```

> **Note:** The first run may take longer as the AI model downloads necessary files (approximately 100MB).

## 📖 Usage Guide

1. **Load an image:**

   - Drag and drop an image file onto the application window, or
   - Click the drop area to browse for an image

2. **Process the image:**

   - Click the "Remove Background" button
   - Wait for processing to complete (typically a few seconds)

3. **Save the result:**
   - Click "Save Result" to save the image with a transparent background
   - Choose your desired save location and filename

## 🖼️ Supported Image Formats

| Input Formats | Output Format           |
| ------------- | ----------------------- |
| JPG/JPEG      | PNG (with transparency) |
| PNG           | PNG (with transparency) |
| BMP           | PNG (with transparency) |

## ⚠️ Troubleshooting

### Common Issues

| Issue                     | Solution                                   |
| ------------------------- | ------------------------------------------ |
| Drag-and-drop not working | Use the "Click to Browse" option instead   |
| Slow processing           | Larger images require more processing time |
| Installation errors       | Ensure Python 3.8+ is properly installed   |

### Error Resolution

If you encounter errors about missing packages:

```bash
pip install --upgrade rembg pillow onnxruntime
```

## ⚙️ Limitations

- Works best with images that have clear contrast between subject and background
- May not achieve perfect results with complex backgrounds or fuzzy edges
- Processing large images may require additional time

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Uses the [rembg](https://github.com/danielgatis/rembg) library for background removal
- Built with Python's tkinter for the graphical user interface
