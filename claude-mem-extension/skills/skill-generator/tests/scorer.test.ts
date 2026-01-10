import { scoreCandidates } from '../src/scorer';
import { Observation } from '../src/types';

describe('Candidate Scorer', () => {
  test('should score observations with repetition boost', () => {
    const observations: Observation[] = [
      {
        id: 1,
        type: 'bugfix',
        title: 'Fix timeout error',
        read_tokens: 100,
        work_tokens: 3000,
        timestamp: '2026-01-09T10:00:00Z',
        session_id: 'S1'
      }
    ];

    const scores = scoreCandidates(observations, new Map([[1, 3]])); // Observation 1 seen 3 times (pattern ID -> count mapping)

    expect(scores[0].repetition).toBe(3);
    expect(scores[0].work_investment).toBeGreaterThan(0);
    expect(scores[0].score).toBeGreaterThan(0);
  });

  test('should weight success higher for bugfixes', () => {
    const bugfix: Observation = {
      id: 1,
      type: 'bugfix',
      title: 'Fix crash',
      read_tokens: 100,
      work_tokens: 2000,
      timestamp: '2026-01-09T10:00:00Z',
      session_id: 'S1'
    };

    const discovery: Observation = {
      id: 2,
      type: 'discovery',
      title: 'Found file',
      read_tokens: 100,
      work_tokens: 2000,
      timestamp: '2026-01-09T10:00:00Z',
      session_id: 'S1'
    };

    const scores = scoreCandidates([bugfix, discovery], new Map([[1, 1], [2, 1]])); // Both observations seen once (pattern ID -> count mapping)

    const bugfixScore = scores.find(s => s.observation.id === 1);
    const discoveryScore = scores.find(s => s.observation.id === 2);

    expect(bugfixScore!.success).toBeGreaterThan(discoveryScore!.success);
  });
});
