import { extractPattern } from '../src/extractor';
import { Observation } from '../src/types';

describe('Pattern Extractor', () => {
  test('should extract core pattern from bugfix observations', () => {
    const observations: Observation[] = [
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

    const pattern = extractPattern(observations);

    expect(pattern.core_problem).toBeDefined();
    expect(pattern.solution).toBeDefined();
    expect(pattern.edge_cases).toEqual([]);
    expect(pattern.structure_type).toBe('pattern-focused');
  });
});
