import * as fs from 'fs';
import * as path from 'path';
import { SkillContent, SkillMetadata, SkillIndex } from './types';

export function writeSkillFile(
  content: SkillContent,
  markdown: string,
  experiencesDir: string
): void {
  const filename = `${content.metadata.name}.md`;
  const filepath = path.join(experiencesDir, filename);

  // Ensure directory exists
  if (!fs.existsSync(experiencesDir)) {
    fs.mkdirSync(experiencesDir, { recursive: true });
  }

  // Write skill file
  fs.writeFileSync(filepath, markdown, 'utf-8');

  // Create metadata tracking file
  const metadataPath = path.join(experiencesDir, '.metadata', `${content.metadata.name}.json`);
  const metadataDir = path.dirname(metadataPath);

  if (!fs.existsSync(metadataDir)) {
    fs.mkdirSync(metadataDir, { recursive: true });
  }

  const trackingData = {
    name: content.metadata.name,
    usage_count: 0,
    invocations: [],
    feedback: []
  };

  fs.writeFileSync(metadataPath, JSON.stringify(trackingData, null, 2), 'utf-8');
}

export function updateSkillIndex(
  metadata: SkillMetadata,
  experiencesDir: string,
  existingIndex?: SkillIndex
): void {
  const indexPath = path.join(experiencesDir, '.index.json');

  let index: SkillIndex = existingIndex || {
    version: '1.0.0',
    last_updated: new Date().toISOString(),
    total_skills: 0,
    skills: []
  };

  // Check if skill already exists
  const existingIdx = index.skills.findIndex(s => s.name === metadata.name);

  if (existingIdx >= 0) {
    // Update existing
    index.skills[existingIdx] = metadata;
  } else {
    // Add new
    index.skills.push(metadata);
    index.total_skills++;
  }

  index.last_updated = new Date().toISOString();

  // Write index
  fs.writeFileSync(indexPath, JSON.stringify(index, null, 2), 'utf-8');

  // Update changelog
  appendToChangelog(metadata, experiencesDir);
}

function appendToChangelog(metadata: SkillMetadata, experiencesDir: string): void {
  const changelogPath = path.join(experiencesDir, '.changelog.md');
  const date = new Date().toISOString().split('T')[0];
  const entry = `\n### ${date}\n\n- **${metadata.name}** - ${metadata.description} (confidence: ${metadata.confidence})\n`;

  if (fs.existsSync(changelogPath)) {
    fs.appendFileSync(changelogPath, entry, 'utf-8');
  } else {
    const header = `# Skills Learning Log\n\n## ${date}\n\n`;
    fs.writeFileSync(changelogPath, header + entry, 'utf-8');
  }
}
