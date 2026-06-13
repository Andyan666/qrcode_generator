# QR Code Generator

A feature-rich Python tkinter QR code generator application with a clean gray interface design.

## Features

### Basic Features
- Generate QR codes from text or URLs
- Copy text to clipboard / Paste from clipboard
- Error correction level selection (Low/Medium/High)
- Multi-format export (PNG, JPG, SVG, PDF)

### Style Customization
- **Foreground Color**: Customize QR code color with live preview
- **Background Color**: Customize background color with live preview
- **Logo Embedding**: Embed a logo image in the center of the QR code (auto-scaled with white border)
- **Border Width**: Input field to set margin (0-10), auto-clamped to valid range
- **Output Size**: Input field to set resolution (100-800 pixels), suitable for different purposes

### Advanced Features
- **Dynamic QR Code**: Monitor URL content changes, auto-regenerate every 5 seconds
- **Batch Generation**: Generate multiple QR codes from TXT/CSV files with auto-naming
- **Wi-Fi QR Code**: Generate QR codes for direct Wi-Fi connection

## Interface Design

- Clean gray background (#f5f5f5)
- Grouped layout (Input, Style Settings, Preview)
- Gray-themed buttons:
  - Generate QR Code (dark gray)
  - Dynamic Monitor (medium gray)
  - Batch Generate (medium gray)
  - Wi-Fi QR Code (medium gray)
  - Dynamic Monitor Running (red)
- Preview area with white background

## Installation

```bash
pip install qrcode pillow
```

## Running

```bash
python qrcode_generator.py
```

## Usage Guide

### Generate QR Code
1. Enter content in the text box
2. Set style parameters:
   - Click "Select" button to customize colors
   - Select a logo image (optional)
   - Enter border width (0-10)
   - Enter output size (100-800)
   - Select error correction level
3. Click "Generate QR Code"
4. Select save format and click "Save Image"

### Batch Generation
1. Prepare a TXT or CSV file with one item per line
2. Click "Batch Generate" button
3. Select file and save directory
4. Click "Start", auto-named as `qrcode_001.png`, `qrcode_002.png`...

### Wi-Fi QR Code
1. Click "Wi-Fi QR Code" button
2. Enter network name (SSID) and password
3. Select encryption type (WPA/WPA2, WEP, None)
4. Optionally check "Hidden Network" or "Show Password"
5. Click "Generate QR Code" to preview
6. Click "Save Image"

### Dynamic Monitor
1. Enter a URL (must start with http:// or https://)
2. Click "Start Dynamic Monitor"
3. Program checks for URL changes every 5 seconds
4. QR code auto-regenerates when content changes
5. Click "Stop Dynamic Monitor" to end

## Error Correction Levels

| Level | Recovery | Description |
|-------|----------|-------------|
| Low (L) | 7% | Clear environment |
| Medium (M) | 15% | Default recommended |
| High (H) | 30% | Logo embedding or harsh environment |

## Parameter Ranges

| Parameter | Range | Description |
|-----------|-------|-------------|
| Border Width | 0-10 | QR code margin, auto-clamped |
| Output Size | 100-800 | Pixels, small for screen, large for print |

## Notes

- High error correction recommended when embedding logos
- Large output suitable for printing
- SVG format is vector graphics for further editing
- PDF format handles transparency automatically
- Dynamic monitor only supports HTTP/HTTPS URLs
- Parameters outside range are auto-clamped to valid values

## File Structure

```
project/
├── qrcode_generator.py  # Main program
├── README_CN.md            # Chinese documentation
└── README_EN.md         # English documentation
```

## Tech Stack

| Technology | Purpose |
|------------|---------|
| tkinter | GUI framework |
| qrcode | QR code generation |
| PIL/Pillow | Image processing |
| threading | Dynamic monitor background thread |