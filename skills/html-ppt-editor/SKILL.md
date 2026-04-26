---
name: html-ppt-editor
description: Use when user wants to visually edit a guizang-style HTML PPT file — edit text, add images/text, drag/reposition elements, replace/delete/resize images, delete slides, and save. Triggers on "编辑HTML PPT", "编辑网页PPT", "打开PPT编辑器", "edit HTML presentation", or when user provides a guizang HTML file and wants to modify it visually.
---

# HTML PPT 可视化编辑器

为 guizang 杂志风 HTML PPT 提供浏览器端 WYSIWYG 编辑能力。

## 何时使用

- 用户提供了一个 guizang 格式的 HTML PPT 文件（单文件，包含 `<section class="slide">` 和 `#deck`）
- 用户要求"编辑这个PPT"、"修改文字"、"替换图片"、"添加图片"、"添加文字"、"拖拽调整位置"
- 用户想可视化编辑而非手动改代码

## 工作流

### Step 1 · 创建编辑版文件

将编辑器脚本注入到用户提供的 HTML 文件中：

```python
import os
# 读取原始 HTML
with open('用户文件.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 读取编辑器脚本
editor_js_path = os.path.expanduser('~/.claude/skills/html-ppt-editor/guizang-ppt-editor.js')
with open(editor_js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 在 </body> 前注入
html = html.replace('</body>', f'<script>\n{js}\n</script>\n</body>')

# 保存为 editor.html
output_path = 'editor.html'  # 与原文件同目录
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)
```

### Step 2 · 在浏览器中打开

```bash
open editor.html
```

### Step 3 · 向用户展示使用说明

直接输出以下内容给用户：

---

**PPT 编辑器已启动！** 使用方法：

| 操作 | 方法 |
|------|------|
| **进入/退出编辑** | 点击顶部「编辑」按钮，或按 `E` 键 |
| **选中元素** | 编辑模式下，单击文字块或图片 |
| **编辑文字** | 双击文字块，直接输入修改 |
| **添加图片** | 编辑模式下，点击「🖼 添加图片」→ 选择图片文件 |
| **添加文本** | 编辑模式下，点击「📝 添加文本」→ 自动进入编辑状态 |
| **拖拽移动** | 选中后，按住左上角蓝色抓手图标拖拽 |
| **替换图片** | 选中图片 → 点击「📷 替换」按钮 → 选择新图片 |
| **删除图片** | 选中图片 → 点击「🗑 删除」按钮 |
| **调整大小** | 选中图片 → 拖拽四角小方块 |
| **删除元素** | 选中后按 `Delete` 键 |
| **翻页** | 退出编辑后用 `←→` 键或底部圆点；编辑中用工具栏 ◀▶ |
| **删除整页** | 点击工具栏「🗑 删除页」 |
| **取消选中** | 点击空白区域或 `Esc` |
| **保存** | 点击「💾 保存」或 `Ctrl+S`，下载干净的 HTML |

快捷键：`E` 编辑 | `←→` 翻页 | `DblClick` 编辑文字 | `Delete` 删除 | `Ctrl+S` 保存 | `Esc` 退出

---

### Step 4 · 用户编辑完成后

保存功能会自动下载 `index-edited.html`，这是干净的 HTML 文件（不含编辑器代码）。如需继续编辑，重新注入即可。

## 注意事项

1. **仅支持 guizang 格式** — HTML 中必须有 `#deck` 容器和 `<section class="slide">` 元素
2. **保存是下载方式** — 浏览器安全限制，只能下载新文件，不能覆盖原文件
3. **编辑器不影响原文件** — 注入是在副本上进行
4. **图片替换用 base64** — 替换的图片以内嵌 base64 方式保存到 HTML 中，文件会变大
5. **拖拽用 transform** — 移动后的元素使用 CSS `transform: translate()` 定位，保存时保留

## 文件结构

```
html-ppt-editor/
├── SKILL.md                    ← 本文件
└── guizang-ppt-editor.js       ← 编辑器脚本（注入到 HTML 中）
```
