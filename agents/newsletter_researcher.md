**Newsletter Researcher:**

Create a newsletter research system that analyzes competitor
newsletters and writes drafts.

Build:

1. A /newsletter-research slash command that:
    - Reads newsletter URLs from my files (or asks me to provide
    them)
    - Fetches recent posts from those newsletters
    - Launches a content-researcher subagent to find trends
    - Then launches a newsletter-writer subagent to create a draft
    - Saves research and draft to organized folders
2. A content-researcher subagent that:
    - Analyzes competitor newsletters for trending topics
    - Identifies content gaps and opportunities
    - Finds time-sensitive angles
    - Passes insights to the newsletter-writer
3. A newsletter-writer subagent that:
    - Gets insights from the content-researcher
    - Writes 3 compelling subject line options
    - Creates a complete 500-800 word draft
    - Matches my writing voice based on my existing content
    - Includes practical takeaways
    - Adds a natural, soft CTA if relevant
4. Folder structure:
    - /newsletter/drafts/ for completed newsletters
    - /metrics/ for research reports

The system should:

- Analyze what's trending across multiple newsletters
- Analyze my newsletter from the link in my files
- Analyze the newsletters from my competitors in the links in my files
- Write in MY voice (learn from my files)
- Create ready-to-send drafts, not just outlines
- Make subject lines that create curiosity

Focus on value-first content that sounds authentic, not
AI-generated.
