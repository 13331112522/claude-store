import { Observation, CandidateScore } from './types';

// Maximum work tokens for normalization (represents ~3000 words of work)
const MAX_WORK_TOKENS = 4000;

export function scoreCandidates(
  observations: Observation[],
  patternCounts: Map<number, number>
): CandidateScore[] {
  const scores: CandidateScore[] = [];

  for (const obs of observations) {
    const repetition = patternCounts.get(obs.id) || 1;
    const success = calculateSuccessWeight(obs);
    const work_investment = obs.work_tokens / MAX_WORK_TOKENS; // Normalize

    const score = (repetition * 1.0) + (success * 2.0) + work_investment;

    scores.push({
      observation: obs,
      score,
      repetition,
      success,
      work_investment,
      pattern: extractPattern(obs)
    });
  }

  return scores.sort((a, b) => b.score - a.score);
}

function calculateSuccessWeight(obs: Observation): number {
  const typeWeights = {
    bugfix: 1.0,
    decision: 0.9,
    feature: 0.8,
    change: 0.7,
    discovery: 0.5
  };

  return typeWeights[obs.type as keyof typeof typeWeights];
}

function extractPattern(obs: Observation): string {
  // Simple pattern extraction from title
  // In production, this would use semantic analysis
  return obs.title.toLowerCase()
    .replace(/^(fix|add|remove|update)\s+/i, '')
    .replace(/\s+/g, '-');
}
