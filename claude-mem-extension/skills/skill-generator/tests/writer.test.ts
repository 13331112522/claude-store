import { writeSkillFile, updateSkillIndex } from '../src/writer';
import { SkillContent, SkillMetadata } from '../src/types';
import * as fs from 'fs';
import * as path from 'path';

jest.mock('fs');
jest.mock('path');

const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

describe('Skill Writer', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should write skill file to experiences directory', () => {
    const metadata: SkillMetadata = {
      name: 'test-skill',
      description: 'Test',
      version: '1.0.0',
      generated: '2026-01-09T00:00:00Z',
      confidence: 0.9,
      tags: ['test'],
      type: 'bugfix',
      source: {
        sessions: ['S1'],
        observations: [1],
        project: 'test'
      },
      usage_count: 0,
      last_used: 'never'
    };

    const content: SkillContent = {
      metadata,
      sections: [{ type: 'problem', content: 'Test' }]
    };

    const markdown = '---\nname: test-skill\n---';

    mockPath.join.mockReturnValue('/skills/experiences/test-skill.md');
    mockFs.writeFileSync.mockReturnValue(undefined as any);
    mockFs.existsSync.mockReturnValue(false);
    mockFs.mkdirSync.mockReturnValue(undefined as any);

    writeSkillFile(content, markdown, '/skills/experiences');

    expect(mockFs.writeFileSync).toHaveBeenCalledWith(
      '/skills/experiences/test-skill.md',
      markdown,
      'utf-8'
    );
  });

  test('should update skill index with new entry', () => {
    const metadata: SkillMetadata = {
      name: 'new-skill',
      description: 'New',
      version: '1.0.0',
      generated: '2026-01-09T00:00:00Z',
      confidence: 0.85,
      tags: ['new'],
      type: 'feature',
      source: {
        sessions: ['S2'],
        observations: [2],
        project: 'test'
      },
      usage_count: 0,
      last_used: 'never'
    };

    const existingIndex = {
      version: '1.0.0',
      last_updated: '2026-01-08T00:00:00Z',
      total_skills: 1,
      skills: []
    };

    mockFs.readFileSync.mockReturnValue(JSON.stringify(existingIndex));
    mockFs.writeFileSync.mockReturnValue(undefined as any);
    mockFs.existsSync.mockReturnValue(true);
    mockFs.appendFileSync.mockReturnValue(undefined as any);

    updateSkillIndex(metadata, '/skills/experiences', existingIndex);

    expect(mockFs.writeFileSync).toHaveBeenCalled();
  });
});
