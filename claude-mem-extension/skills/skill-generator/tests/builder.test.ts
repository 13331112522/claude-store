import { buildSkillMarkdown } from '../src/builder';
import { SkillContent, SkillMetadata } from '../src/types';

describe('Skill Builder', () => {
  test('should generate valid skill markdown with frontmatter', () => {
    const metadata: SkillMetadata = {
      name: 'test-skill',
      description: 'A test skill',
      version: '1.0.0',
      generated: '2026-01-09T00:00:00Z',
      confidence: 0.95,
      tags: ['test', 'example'],
      type: 'bugfix',
      source: {
        sessions: ['S1'],
        observations: [1, 2, 3],
        project: 'test-project'
      },
      usage_count: 0,
      last_used: 'never'
    };

    const content: SkillContent = {
      metadata,
      sections: [
        {
          type: 'problem',
          content: 'Test problem description'
        },
        {
          type: 'solution',
          content: 'Test solution steps'
        }
      ]
    };

    const markdown = buildSkillMarkdown(content);

    expect(markdown).toContain('---');
    expect(markdown).toContain('name: test-skill');
    expect(markdown).toContain('# Test Skill');
    expect(markdown).toContain('## Problem');
    expect(markdown).toContain('Test problem description');
  });

  test('should include all metadata fields', () => {
    const metadata: SkillMetadata = {
      name: 'complete-test',
      description: 'Complete metadata test',
      version: '1.0.0',
      generated: '2026-01-09T00:00:00Z',
      confidence: 0.88,
      tags: ['tag1', 'tag2'],
      type: 'feature',
      source: {
        sessions: ['S1', 'S2'],
        observations: [1, 2],
        project: 'myproject'
      },
      usage_count: 5,
      last_used: '2026-01-08T15:30:00Z'
    };

    const content: SkillContent = { metadata, sections: [] };
    const markdown = buildSkillMarkdown(content);

    expect(markdown).toContain('confidence: 0.88');
    expect(markdown).toContain('sessions: ["S1", "S2"]');
    expect(markdown).toContain('usage_count: 5');
  });
});
