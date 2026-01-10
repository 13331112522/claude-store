import { SkillContent, SkillSection } from './types';

export function buildSkillMarkdown(content: SkillContent): string {
  const { metadata, sections } = content;

  // Build frontmatter
  const frontmatter = buildFrontmatter(metadata);

  // Build title from metadata name
  const title = toTitleCase(metadata.name);

  // Build sections
  let body = `# ${title}\n\n`;

  for (const section of sections) {
    body += buildSection(section);
  }

  return `${frontmatter}\n\n${body}`;
}

function buildFrontmatter(metadata: any): string {
  return `---
name: ${metadata.name}
description: ${metadata.description}
version: ${metadata.version}
generated: ${metadata.generated}
confidence: ${metadata.confidence}
tags: [${metadata.tags.map((t: string) => `"${t}"`).join(', ')}]
type: ${metadata.type}
source:
  sessions: [${metadata.source.sessions.map((s: string) => `"${s}"`).join(', ')}]
  observations: [${metadata.source.observations.join(', ')}]
  project: "${metadata.source.project}"
usage_count: ${metadata.usage_count}
last_used: ${metadata.last_used}
---`;
}

function buildSection(section: SkillSection): string {
  const headings = {
    'problem': '## Problem',
    'solution': '## Solution',
    'rationale': '## Rationale',
    'edge-cases': '## Edge Cases',
    'examples': '## Examples',
    'overview': '## Overview'
  };

  const heading = headings[section.type] || `## ${section.type}`;

  return `${heading}\n\n${section.content}\n\n`;
}

function toTitleCase(str: string): string {
  return str.split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}
