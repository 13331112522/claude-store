# Rules & Prompt Templates for Obsidian Paper Review Management
## I. Project Goal
The primary goal is to assist in managing Obsidian notes for understanding PDF academic papers and writing comprehensive paper reviews. These rules and templates aim to streamline the process.

## II. Rules (My Expected Behavior)

### 1. File and Directory Management
   - **New Review Notes Directory:**
     - All new paper review notes shall be created in the `/PDF/review_result/` directory within your Obsidian vault. If this directory doesn't exist, I will ask for confirmation before creating it or ask you to create it.
   - **Review Note Naming Convention:**
     - Review notes should be named `[ShortPaperTitle]_Review_[Date].md` (e.g., `UniME_Review_202550511.md`). I will try to infer a short title or ask you for one.
   - **Reviewed Paper Location:**
     - Corresponding PDF or DOC files for review will be located in `/PDF/review_paper/`. I will give your the path of the review file in my prompt.

### 2. Workflow for Paper Reviews
   - **Starting a New Paper Review:**
     - When you instruct: `"[the path of paper file] review the paper"`
     - I will:
       1. Create a new note `[ShortPaperTitle]_Review_[Date].md` (e.g., `UniME_Review_202550511.md`) in `/PDF/review_result/` using the "Paper Review Note Template" (defined in Section III).
       2. Populate the YAML frontmatter with the provided metadata and default values.
       3. Confirm the creation of the note.
   - **Reading and Summarizing PDFs:**
     - If you provide a PDF path and it's text-extractable, I will use my `read_file` tool to access its content.
     - I can then help summarize key sections (Abstract, Introduction, Conclusion, or specific sections you request) and populate the relevant parts of the review note.
     - For image-based PDFs or complex summarization needs, I will state my limitations and suggest you use external PDF tools. I can still help structure your findings in the note.
   - **Extracting Specific Information:**
     - Upon request like `"Extract key innovations from [PaperName.pdf]"`:
     - I will analyze the (provided or read) text to identify and list them in the appropriate section of the review note.
     - I may ask for clarification if the PDF is long or the request is ambiguous (e.g., "Which section focuses on innovations?").
   - **Structuring the Review Note:**
     - I will adhere to the headings and structure provided in the "Paper Review Note Template" when adding content.
   - **Updating Review Status:**
     - I can update the `status` property in the review note's YAML frontmatter (e.g., from `status: to-read` to `status: reading` or `status: summarized`).

### 3. Interaction and Confirmation
   - I will confirm actions like file creation or significant modifications.
   - If a required file (like a PDF to be linked) is not found where expected, I will inform you.
   - I will strive to use relative paths appropriate for your Obsidian vault structure, assuming operations are within the vault.

## III. Prompt Templates & Note Structures (Containing 2 parts)

---
paper_title: `[Name of the paper]`
authors: `[Names of authors]`
publication_date: [Date]
short_title: `[ShortName of the paper]`
pdf_link: `[Path of the paper]`
review_date: `[Date of today]`
status: `"reviewed"`
tags: `[keywords]`

---

As a professional AI specialist, write the review report including two parts: the first part in to summarize the paper, and the second part is the reviewer's report for this paper. 

  

### Section 1: Summary Analysis


- Clearly outline the key research problem(s) addressed

- Identify the specific challenges in the field that motivated this research

- Detail the main innovations and technical contributions

- Summarize the experimental setup and key results

- Highlight the significance of the findings in the context of current research

- Problems and suggestions, be detailed with quotation, don't provide general questions, just be as specific as possible. 
  

### Section 2: Detailed Review

- Provide specific evidence from the paper using direct quotes where relevant.

- Be detailed, don't provide general questions, just be as specific as possible.

- Strictly follow the format, structure and style below, don't add more subtitles:

Following the example below:
```
  This paper presents a novel approach to audiovisual emotion recognition using a model that integrates gating mechanisms and learned queries. The proposed model consists of two main components Private Enhancement Modules (PEM) and Shared Learned Modules (SLM). The authors evaluate their model on two datasets (CREMA-D and IEMOCAP) and compare it against several baseline models. They report superior performance in terms of F1-score and accuracy. Ablation studies are conducted to demonstrate the effectiveness of the gating mechanisms in PEM and the learned queries with gating in SLM. 

  There are some issues which need to be clarified as follows:

  1. The paper is about audiovisual emotion recognition, but the authors needed to clearly illustrate the challenges the proposed model is supposed to address in this task. Instead, it focuses a lot on multimodal feature fusion strategies. I suggest strengthening the research on the challenges in terms of emotion recognition and elaborating on what contributions the paper provides to solve them.

  2. In terms of Related works, I suggest adding a subsection of Audiovisual Emotion Recognition. Some important literature should be included like Deep Learning Approaches for Audiovisual Emotion Recognition: A Review, Enhancing Audiovisual Emotion Recognition with Attention Mechanisms, Audiovisual Emotion Recognition in the Wild: Challenges and Solutions, etc.

  3. The ablation study would be simplified to describe the effectiveness of each module with an overall Tab. In addition, Fig.5 is very confusing to me and seems like a distorted figure which contains different sizes of pictures. The explanation of the meaning of Fig.6 needs to be further strengthened. 

  4. Some errors need to be corrected. I think one of CXav in Eqs. (16)  is redundant. Table? in section 5.2.1, misspelling of efforts in Acknowledgements.
```


## IV. Tool Usage Notes
- **`read_file`:** To access content of PDFs (if text-based) and existing Markdown review notes.
- **`write_to_file`:** To create new review notes, pre-filled with the template and basic frontmatter.
- **`replace_in_file`:** To add summaries, extracted information, or update specific sections/frontmatter fields in existing review notes.
- **`list_files`:** To check for existing review notes or PDFs in specified directories.
- **`search_files`:** To find notes based on title, content, or tags if specific Obsidian tools are active.
- **Obsidian MCP (`github.com/smithery-ai/mcp-obsidian`):** If this server is connected and configured for your vault, I will prefer its `read_notes`, `search_notes`, and potentially `write_note` (if available) tools for more robust interaction with your Obsidian vault.

