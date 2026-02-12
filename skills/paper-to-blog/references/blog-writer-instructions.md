# Blog Writer Instructions

This reference contains the detailed instructions for transforming academic papers into engaging, comprehensive blog posts.

## Core Prompt

Act as a thoughtful writer and synthesizer of ideas, tasked with creating an engaging, comprehensive blog post that deeply explores academic research. Your goal is to transform the provided research paper into an accessible 2000-word article that balances technical depth with broader implications, written in flowing prose rather than listicle format.

## Writing Style Requirements

### Overall Style
- Engaging, intelligent, and thorough
- Write in **Chinese**
- Target length: approximately **2000 words**
- Prioritize flowing paragraphs over bullet points
- Balance technical accessibility with intellectual depth

### Structure

1. **Compelling Headline**
   - Click-worthy and engaging
   - Should hint at the paper's main contribution or insight

2. **Introduction (200-300 words)**
   - Hook the reader by establishing a relatable problem or curiosity
   - Provide context about the research domain and why it matters
   - Briefly introduce the paper and its significance
   - Set up the main themes that will be explored

3. **Background & Context (250-350 words)**
   - Explain the research domain and relevant prior work
   - Describe the problem the paper addresses in detail
   - Help readers understand the technical landscape
   - Use flowing paragraphs, not bullet points

4. **Core Methodology (400-500 words)**
   - Explain the paper's approach or methodology in detail
   - Describe key innovations or techniques
   - Explain how the approach differs from existing methods
   - Include specific details about algorithms, architectures, or experimental designs
   - Write in integrated prose - explain concepts fully within paragraphs

5. **Key Findings & Results (400-500 words)**
   - Present the main results and their significance
   - Discuss performance metrics and comparisons
   - Explain what the results mean in practical terms
   - Include quantitative details and specific numbers where relevant
   - Analyze why the findings are important or surprising

6. **Implications & Applications (250-350 words)**
   - Discuss real-world applications of the research
   - Explore implications for the field or industry
   - Consider limitations or open questions
   - Connect to broader trends or future directions

7. **Conclusion (150-200 words)**
   - Summarize the key takeaways in a flowing narrative
   - Offer a forward-looking perspective on the research
   - Leave the reader with a thought-provoking insight or question

### Content Guidelines

**For 2000-word target, ensure:**
- Each section contains substantive, specific content
- Avoid vague generalizations - include specific details from the paper
- Explain technical concepts thoroughly for accessibility
- Include concrete examples and numerical data when available
- Elaborate on the "why" and "how," not just the "what"

**Avoid excessive bullet points:**
- Use bullet points sparingly, only for clear itemization when absolutely necessary
- Prefer integrated paragraphs that flow naturally
- If listing items, group them into thematic paragraphs instead
- Maximum 1-2 short bullet lists per article, if any

## Image Handling

**Figure and Table Extraction:**

The Figure Extractor agent uses PDF rendering and AI vision to extract actual figures and tables as individual image files.

**Extraction Process:**

1. **PDF Rendering with PyMuPDF:**
   - Each page is rendered at 2x scale for high quality
   - Temporary full-page images are created for analysis

2. **AI Vision Region Detection:**
   - `mcp__4_5v_mcp__analyze_image` identifies visual elements
   - Returns coordinates and descriptions for each figure/table
   - Filters out text blocks, page numbers, headers/footers

3. **Cropping and Saving:**
   - PIL crops identified regions from rendered pages
   - Saves with descriptive names: `fig1_architecture.png`, `table1_results.png`
   - Creates `figures_metadata.json` with descriptions

4. **Output Location:**
   - All extracted images saved to `pdf/PaperLog/figures/`
   - Temp files cleaned up after extraction

5. **Image References in Blog:**
   - Use format: `![](figures/filename.png)`
   - Only actual figures/diagrams/tables (no full page renders)

6. **Strategic Placement:**
   - Flow diagrams → Introduction/Background sections
   - Architecture diagrams → Core Methodology section
   - Result tables/charts → Key Findings section
   - Add brief context before each image

## Style Reference

- Write as a knowledgeable guide explaining complex ideas clearly
- Use transitional phrases to connect paragraphs and sections
- Vary sentence structure for engagement
- Include specific technical details balanced with plain-language explanations
- Each section should feel like a cohesive exploration, not a collection of facts

## Output Format

- Save as Markdown file (.md)
- Output directory: `pdf/PaperLog/`
- Filename pattern: `[PaperTitle]_博客.md` or `[Topic]博客.md`
