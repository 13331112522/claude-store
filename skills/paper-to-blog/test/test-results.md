# Agent Test Results

**Date:** 2026-01-17
**Tested:** Figure Extractor Agent, Cover Designer Agent

## Test Environment

```
Platform: macOS (Darwin 25.1.0)
Python: 3.12
Dependencies: PyMuPDF, Pillow, requests (all installed)
```

## Test Fixtures

- `test/fixtures/attention_paper.pdf` - "Attention Is All You Need" (2.1 MB, 15 pages)
- `test/fixtures/sample_cv_paper.pdf` - Computer Vision with SAS (4.2 MB, has rendering issues)

---

## 1. Figure Extractor Agent Test

### Test Setup
- Script: `scripts/extract_figures.py`
- Test PDF: `test/fixtures/attention_paper.pdf` (Page 3 with Transformer architecture)
- MCP Tool: `mcp__zai-mcp-server__analyze_image`

### Test Results

| Component | Status | Details |
|-----------|--------|---------|
| PDF Rendering | ✅ PASS | PyMuPDF successfully rendered pages at 2x scale (1224x1584) |
| MCP Vision Analysis | ✅ PASS | `mcp__zai-mcp-server__analyze_image` detected Figure 1 (Transformer architecture) |
| Bounding Box Detection | ✅ PASS | Accurate coordinates: top=8%, left=32%, bottom=51%, right=68% |
| Image Cropping | ✅ PASS | Successfully cropped and saved figure (441x681 pixels) |
| Metadata Generation | ✅ PASS | Created `figures_metadata.json` with figure info |

### Output Files
```
test/output/
├── attention_page3.png          # Full page render (1224x1584)
├── fig1_transformer_architecture.png  # Cropped figure (441x681)
└── figures_metadata.json        # Figure metadata
```

### Vision Analysis Result
```json
{
  "type": "diagram",
  "bounding_box": {
    "top": 8, "left": 32, "bottom": 51, "right": 68
  },
  "content_description": "A schematic diagram illustrating the architecture of the Transformer model...",
  "figure_table_number": "Figure 1",
  "key_text": ["Inputs", "Multi-Head Attention", "Feed Forward", ...]
}
```

### Issues Found
1. **`mcp__4_5v_mcp__analyze_image`** - Returns error 1210 "图片输入格式/解析错误" for local files
2. **Solution**: Use `mcp__zai-mcp-server__analyze_image` instead, which supports local files

---

## 2. Cover Designer Agent Test

### Test Setup
- Script: `scripts/generate_cover.py`
- Test Content: Blog summary about Transformer architecture
- API: ZhipuAI CogView (https://open.bigmodel.cn/)

### Test Results

| Component | Status | Details |
|-----------|--------|---------|
| Script Execution | ✅ PASS | Script runs correctly with API key |
| Prompt Construction | ✅ PASS | Generated appropriate prompt from blog content |
| API Call | ✅ PASS | Successfully generated cover image |
| Image Download | ✅ PASS | Downloaded and saved as PNG (1024x1024, 892KB) |

### Output Files
```
test/output/
└── cover_transformer.png  # Generated cover (1024x1024, 892KB)
```

### Issues Found & Fixed
1. **Size Parameter**: Original default `1920x1080` not supported by API
   - **Fix**: Changed to `1024x1024` (square format)
   - Files updated: `scripts/generate_cover.py`

2. **Rate Limiting**: API returns 429 after multiple rapid requests
   - **Mitigation**: Add delays between batch requests

### Configuration Required
```bash
export ZHIPUAI_API_KEY="your_api_key_here"
# Get key from: https://open.bigmodel.cn/
```

---

## Summary

| Agent | Status | Notes |
|-------|--------|-------|
| Figure Extractor | ✅ WORKING | Uses `mcp__zai-mcp-server__analyze_image` for vision analysis |
| Cover Designer | ✅ WORKING | Fixed size parameter to use `1024x1024` |

### Fixes Applied

1. **Figure Extractor** (`agents/figure-extractor.md`):
   - Updated to use `mcp__zai-mcp-server__analyze_image` instead of `mcp__4_5v_mcp__analyze_image`

2. **Cover Designer** (`scripts/generate_cover.py`):
   - Changed default size from `1920x1080` to `1024x1024` (API compatibility)
   - Removed 16:9 aspect ratio from prompt template

### User Setup Required

1. **Cover Designer**: Set ZhipuAI API key
   ```bash
   export ZHIPUAI_API_KEY="your_api_key_here"
   ```

2. **Rate Limiting**: Add delays between multiple cover generation requests

---

## Sources

- [Computer Vision with SAS - Free PDF](https://support.sas.com/content/dam/SAS/support/en/books/free-books/computer-vision-with-sas.pdf)
- [VIS30K: IEEE Visualization Figures Collection](https://inria.hal.science/hal-03123279/file/Chen_2021_VCF.pdf)
- [Multiple View Geometry in Computer Vision](http://www.r-5.org/files/books/computers/algo-list/image-processing/vision/Richard_Hartley_Andrew_Zisserman-Multiple_View_Geometry_in_Computer_Vision-EN.pdf)
- [arXiv Computer Vision and Pattern Recognition](https://arxiv.org/list/cs.CV/recent)
