import { generateSkills } from '../src/index';
import { Observation } from '../src/types';

describe('Skill Generator Integration', () => {
  test('should generate skill from sample observations', async () => {
    const sampleObservations: Observation[] = [
      {
        id: 671,
        type: 'bugfix',
        title: 'Fixed Ralph Loop Command Documentation',
        read_tokens: 186,
        work_tokens: 1038,
        timestamp: '2026-01-06T12:55:00Z',
        session_id: '#S58'
      },
      {
        id: 673,
        type: 'bugfix',
        title: 'Ralph Loop Command Structure',
        read_tokens: 307,
        work_tokens: 885,
        timestamp: '2026-01-06T12:56:00Z',
        session_id: '#S58'
      }
    ];

    const result = await generateSkills(sampleObservations, 'test-project');

    expect(result.skillsGenerated).toBe(2);
    expect(result.skills[0].metadata.name).toBeDefined();
    expect(result.skills[0].metadata.confidence).toBeGreaterThan(0);
  });

  test('should handle empty observations array', async () => {
    const result = await generateSkills([], 'test-project');

    expect(result.skillsGenerated).toBe(0);
    expect(result.skills).toHaveLength(0);
  });

  test('should include candidates in result', async () => {
    const sampleObservations: Observation[] = [
      {
        id: 671,
        type: 'bugfix',
        title: 'Fixed Ralph Loop Command Documentation',
        read_tokens: 186,
        work_tokens: 1038,
        timestamp: '2026-01-06T12:55:00Z',
        session_id: '#S58'
      }
    ];

    const result = await generateSkills(sampleObservations, 'test-project');

    expect(result.candidates).toBeDefined();
    expect(result.candidates.length).toBeGreaterThan(0);
    expect(result.candidates[0].score).toBeGreaterThan(0);
  });
});
