# PaperDog Podcast Skill

## 功能
从 paperdog.org 获取**当天**评分最高的 AI 论文，写成播客式中文介绍，生成 md 文件、封面图片和 mp3 播客，通过飞书发送。

**核心要求：必须基于 paperdog.org 当天评分最高的论文，确保是最新鲜的内容。**

## 步骤

### 1. 获取当天论文列表（关键步骤）
访问 paperdog.org/archive 或 paperdog.org 获取**当天**最新的论文列表，**必须确认是当天发布的论文**。

**验证方法：**
- 检查论文的发布日期/评分时间
- 确保选择的是当天评分最高的论文
- 排除往期论文

### 2. 选择 Top 5 论文（按评分排序）
**必须选择评分最高的5篇论文**，按评分从高到低排序，记录：
- 论文标题（英文）
- 作者
- 机构/学校
- arXiv 链接

### 3. 获取论文摘要
访问每篇论文的 arXiv 页面提取摘要。

### 4. 撰写播客文稿
每篇论文约 400 字，内容要求：
- 标题用英文
- 作者和机构用英文
- 内容为中文
- 通俗易懂，适合播客朗读
- 包含背景介绍、研究意义、核心贡献

### 5. 生成 MD 文件
保存为 `/workspace/paper-podcast-YYYYMMDD.md`

### 6. 分析论文内容生成提示词
读取 MD 文件内容，提取关键主题和研究方向，生成适合提示的图片词：
- 提取 5 篇论文的核心主题（如：LLM、Agent、视觉、机器人等）
- 生成描绘这些主题的 AI 图像提示词
- 提示词格式：科技感、学术风格、深蓝紫色调、现代简约设计

### 7. 生成播客封面
使用海螺 AI 图片生成：
```python
image_synthesize(prompt="[基于论文内容的提示词]")
```
示例提示词：
```
A futuristic podcast cover for AI research papers about [TOPIC]. 
Abstract [TECHNOLOGY] patterns, [VISUAL_ELEMENTS], 
deep blue and purple color scheme, professional tech style, 
modern and clean design, 3D render
```
保存为 `/workspace/paper-podcast-YYYYMMDD-cover.png`

### 8. 生成 MP3 播客
使用火山引擎 TTS 生成播客音频：
```bash
/workspace/.venv/bin/python /workspace/volc_podcast.py -f /workspace/paper-podcast-YYYYMMDD.md -o /workspace/paper-podcast-YYYYMMDD.mp3
```

### 9. 上传并发送
1. 上传 MD、封面、MP3 到 CDN
2. 使用 `message` 的 `media` 参数依次发送：
   - 封面图片
   - MP3 音频
   - MD 文件
（飞书用户ID: ou_972a18ccdc1d6f0d265093adf3a5a1c3）

### 10. 生成播客介绍
从 MD 文件中提取 5 篇论文的标题、机构和研究亮点，生成简洁的播客介绍：
- 每篇论文用 emoji 序号排列
- 包含论文标题（英文）、机构、1句话研究亮点
- 格式示例：

```
📰 PaperDog论文日报 - YYYY年M月D日

本期5篇论文：

1️⃣ **论文标题**
   - 机构 | 研究亮点

2️⃣ ...
```

发送顺序：封面 → MP3 → MD → 播客介绍（文字消息）

## 火山引擎 TTS 配置
- APP_ID: 4243287022
- ACCESS_TOKEN: i2MarDfvjlf0Piv7Zwudu3dt2htyVJr4
- WS_URL: wss://openspeech.bytedance.com/api/v3/sami/podcasttts
- 发音人：大一先生 + 咪仔同学

## 格式模板

```markdown
# Paper Podcast - March 4, 2026

> Selected from PaperDog Daily AI Papers

---

## Paper 1: [论文标题英文]

**Authors:** [作者]  
**Institution:** [机构]

[中文播客内容，约400字]

---

## Paper 2: [论文标题英文]

...

---
```

## 定时任务
- **论文播客：每天 7:30** 自动运行
- **重要：必须获取当天最新论文，不能使用往期内容**
- 输出文件：
  - `/workspace/paper-podcast-YYYYMMDD.md`
  - `/workspace/paper-podcast-YYYYMMDD.mp3`
  - `/workspace/paper-podcast-YYYYMMDD-cover.png`
- 发送顺序：封面 → MP3 → MD → 播客介绍（文字消息）
- **重要：封面图片必须基于当日论文内容生成**
