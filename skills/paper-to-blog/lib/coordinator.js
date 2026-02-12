/**
 * Multi-Agent Paper-to-Blog Coordinator
 *
 * Orchestrates 6 specialized agents:
 * 1. Parser → Blog Generator || Figure Extractor || Cover Designer → Integrator → Master
 * 2. Iteration loop (1-3 cycles) with targeted rework
 */

const fs = require('fs').promises;
const path = require('path');

class BlogCoordinator {
  constructor(pdfPath, outputDir = 'pdf/PaperLog') {
    // Input validation
    if (!pdfPath || typeof pdfPath !== 'string') {
      throw new Error('pdfPath is required and must be a string');
    }
    if (typeof outputDir !== 'string') {
      throw new Error('outputDir must be a string');
    }

    this.pdfPath = pdfPath;
    this.outputDir = outputDir;
    this.iteration = 0;
    this.maxIterations = 3;
    this.checkpoints = [];
  }

  /**
   * Main workflow orchestration
   */
  async run() {
    try {
      console.log(`Starting paper-to-blog workflow for: ${this.pdfPath}`);

      // Phase 1: Parse PDF
      const parsedContent = await this.runParser();

      // Phase 2: Parallel execution of Blog Generator, Figure Extractor, Cover Designer
      let [blogDraft, figuresData, coverPath] = await Promise.all([
        this.runBlogGenerator(parsedContent),
        this.runFigureExtractor(),
        this.runCoverDesigner()
      ]);

      // Phase 3: Iteration loop (minimum 1, maximum 3)
      let integratedBlog = await this.runIntegrator(blogDraft, figuresData, coverPath);

      do {
        this.iteration++;
        const review = await this.runMaster(integratedBlog);

        if (review.approved && this.iteration >= 1) {
          console.log(`Blog approved after iteration ${this.iteration}`);
          break;
        }

        if (this.iteration >= this.maxIterations) {
          console.log(`Max iterations reached. Outputting best version.`);
          break;
        }

        // Targeted rework based on feedback - captures updated results
        const reworkResults = await this.runTargetedRework(review.feedback, parsedContent);

        // Update data with rework results (with null/undefined validation)
        if (reworkResults.blogDraft != null) {
          blogDraft = reworkResults.blogDraft;
        }
        if (reworkResults.figuresData != null) {
          figuresData = reworkResults.figuresData;
        }
        if (reworkResults.coverPath != null) {
          coverPath = reworkResults.coverPath;
        }

        // Re-run Integrator and Master with updated data
        integratedBlog = await this.runIntegrator(blogDraft, figuresData, coverPath);

        await this.saveCheckpoint(integratedBlog, review);
      } while (this.iteration < this.maxIterations);

      // Phase 4: Save final output
      return this.saveFinalOutput(integratedBlog);
    } catch (error) {
      console.error(`Error in paper-to-blog workflow: ${error.message}`);
      console.error(error.stack);
      throw error;
    }
  }

  /**
   * Phase 1: Parse PDF
   */
  async runParser() {
    console.log('Phase 1: Running Parser Agent...');
    // Agent execution via Claude Code Task tool
    return { /* parsed content */ };
  }

  /**
   * Phase 2a: Blog Generator
   */
  async runBlogGenerator(parsedContent) {
    console.log('Phase 2a: Running Blog Generator Agent...');
    // Agent execution via Claude Code Task tool
    return { /* blog draft */ };
  }

  /**
   * Phase 2b: Figure Extractor
   */
  async runFigureExtractor() {
    console.log('Phase 2b: Running Figure Extractor Agent...');
    // Agent execution via Claude Code Task tool
    return { /* figures metadata */ };
  }

  /**
   * Phase 2c: Cover Designer
   */
  async runCoverDesigner() {
    console.log('Phase 2c: Running Cover Designer Agent...');
    // Agent execution via Claude Code Task tool
    return { /* cover path */ };
  }

  /**
   * Phase 3: Integrator
   */
  async runIntegrator(blogDraft, figuresData, coverPath) {
    console.log('Phase 3: Running Integrator Agent...');
    // Agent execution via Claude Code Task tool
    return { /* integrated blog */ };
  }

  /**
   * Phase 4: Master Review
   */
  async runMaster(integratedBlog) {
    console.log(`Phase 4: Running Master Agent (iteration ${this.iteration})...`);
    // Agent execution via Claude Code Task tool
    return { approved: false, feedback: [], summary: '' };
  }

  /**
   * Targeted rework based on Master feedback
   */
  async runTargetedRework(feedback, parsedContent) {
    console.log('Running targeted rework...');

    const results = {
      blogDraft: null,
      figuresData: null,
      coverPath: null
    };

    for (const item of feedback) {
      switch (item.to) {
        case 'blog-generator':
          results.blogDraft = await this.runBlogGenerator(parsedContent, item.action);
          break;
        case 'figure-extractor':
          results.figuresData = await this.runFigureExtractor(item.action);
          break;
        case 'cover-designer':
          results.coverPath = await this.runCoverDesigner(item.action);
          break;
      }
    }

    return results;
  }

  /**
   * Save checkpoint for iteration history
   */
  async saveCheckpoint(integratedBlog, review) {
    const checkpointDir = path.join(this.outputDir, 'checkpoints');
    await fs.mkdir(checkpointDir, { recursive: true });

    const blogPath = path.join(checkpointDir, `blog_v${this.iteration}.md`);
    const feedbackPath = path.join(checkpointDir, `feedback/feedback_v${this.iteration}.txt`);

    await fs.writeFile(blogPath, integratedBlog.content);
    await fs.mkdir(path.dirname(feedbackPath), { recursive: true });
    await fs.writeFile(feedbackPath, JSON.stringify(review, null, 2));

    this.checkpoints.push({ iteration: this.iteration, blogPath, feedbackPath });
  }

  /**
   * Save final output
   */
  async saveFinalOutput(integratedBlog) {
    const filename = `${integratedBlog.title.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_')}.md`;
    const outputPath = path.join(this.outputDir, filename);

    await fs.mkdir(this.outputDir, { recursive: true });
    await fs.writeFile(outputPath, integratedBlog.content);

    console.log(`Final blog saved to: ${outputPath}`);
    return outputPath;
  }
}

module.exports = BlogCoordinator;
