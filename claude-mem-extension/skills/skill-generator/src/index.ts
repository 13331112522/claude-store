import { Observation, SkillContent, CandidateScore } from './types';
import { scoreCandidates } from './scorer';
import { extractPattern } from './extractor';
import { buildSkillMarkdown } from './builder';

export interface GenerationResult {
  skillsGenerated: number;
  skills: SkillContent[];
  candidates: CandidateScore[];
}

export async function generateSkills(
  observations: Observation[],
  project: string
): Promise<GenerationResult> {
  // Handle empty observations
  if (!observations || observations.length === 0) {
    return {
      skillsGenerated: 0,
      skills: [],
      candidates: []
    };
  }

  // Step 1: Score candidates
  const patternCounts = new Map<number, number>();
  for (const obs of observations) {
    patternCounts.set(obs.id, (patternCounts.get(obs.id) || 0) + 1);
  }

  const candidates = scoreCandidates(observations, patternCounts);

  // Take top candidates (in production, user selects)
  const topCandidates = candidates.slice(0, 5);

  const skills: SkillContent[] = [];

  // Step 2: Generate skills for each candidate
  for (const candidate of topCandidates) {
    const pattern = extractPattern([candidate.observation]);

    const skillContent: SkillContent = {
      metadata: {
        name: generateSkillName(pattern),
        description: generateDescription(pattern),
        version: '1.0.0',
        generated: new Date().toISOString(),
        confidence: Math.min(candidate.score / 10, 1.0),
        tags: generateTags(pattern),
        type: candidate.observation.type,
        source: {
          sessions: [candidate.observation.session_id],
          observations: [candidate.observation.id],
          project
        },
        usage_count: 0,
        last_used: 'never'
      },
      sections: buildSections(pattern)
    };

    skills.push(skillContent);
  }

  return {
    skillsGenerated: skills.length,
    skills,
    candidates
  };
}

function generateSkillName(pattern: any): string {
  return 'skill-' + Date.now();
}

function generateDescription(pattern: any): string {
  return `Auto-generated skill from conversation history`;
}

function generateTags(pattern: any): string[] {
  return ['auto-generated'];
}

function buildSections(pattern: any): any[] {
  return [
    {
      type: 'problem',
      content: pattern.core_problem || 'Problem description'
    },
    {
      type: 'solution',
      content: pattern.solution || 'Solution description'
    }
  ];
}

// Export all modules
export * from './types';
export * from './scorer';
export * from './extractor';
export * from './builder';
export * from './writer';
export * from './mcp-tools';
