# Paper-to-Blog Integration Test

## Test Setup

1. Obtain a sample academic paper PDF
2. Place in test directory: `test/fixtures/sample-paper.pdf`

## Test Execution

Run the skill with test PDF:

```
User: "Convert test/fixtures/sample-paper.pdf to a blog post"
```

## Expected Behavior

### Phase 1: Parser
- Output: Parsed markdown (intermediate, not saved)
- Verify: Markdown contains headings, text, figure references

### Phase 2: Parallel Agents
- Blog Generator: Chinese content ~2000 words, bolded subheadings
- Figure Extractor: `pdf/PaperLog/figures_metadata.json` with at least 1 figure
- Cover Designer: `pdf/PaperLog/figures/cover.png` exists, 16:9 aspect ratio

### Phase 3: Integrator
- Output: Integrated markdown with cover at top
- Verify: `![](figures/cover.png)` present (relative path from blog file)
- Verify: Figure placeholders replaced with actual references

### Phase 4: Master + Iteration
- Minimum 1 iteration occurs
- Maximum 3 iterations
- Final output: `pdf/PaperLog/[title].md`

## Agent Execution Verification

- [ ] Parser Agent: Completed
- [ ] Blog Generator Agent: Completed
- [ ] Figure Extractor Agent: Completed
- [ ] Cover Designer Agent: Completed
- [ ] Integrator Agent: Completed
- [ ] Master Agent: Completed

## Success Criteria

- [ ] All 6 agents execute successfully
- [ ] Blog content is Chinese, ~2000 words
- [ ] At least 1 figure extracted
- [ ] Cover image generated
- [ ] At least 1 iteration completed
- [ ] Final output file exists in pdf/PaperLog/

## Manual Verification

1. Open final blog file
2. Check headline is compelling
3. Scan for bolded subheadings
4. Verify figures are contextually placed
5. Check cover image displays correctly
