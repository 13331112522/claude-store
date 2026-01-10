import { Observation } from './types';

const HIGH_WORK_TOKENS = 1000;

export interface ExtractedPattern {
  core_problem: string;
  solution: string;
  rationale: string;
  edge_cases: EdgeCase[];
  structure_type: 'pattern-focused' | 'standard' | 'tutorial' | 'reference';
}

export interface EdgeCase {
  description: string;
  resolution: string;
}

export function extractPattern(observations: Observation[]): ExtractedPattern {
  if (!observations || observations.length === 0) {
    throw new Error('Cannot extract pattern from empty observations array');
  }

  const mainType = observations[0].type;

  // Group observations by type to identify the main flow
  const bugfixes = observations.filter(o => o.type === 'bugfix');
  const decisions = observations.filter(o => o.type === 'decision');
  const discoveries = observations.filter(o => o.type === 'discovery');

  // Extract core problem from bugfix titles
  const core_problem = summarizeProblem(bugfixes);

  // Extract solution from high-work observations
  const solution = summarizeSolution(observations.filter(o => o.work_tokens > HIGH_WORK_TOKENS));

  // Extract rationale from decisions
  const rationale = summarizeRationale(decisions);

  // Identify edge cases from discoveries
  const edge_cases = identifyEdgeCases(discoveries);

  // Determine structure type
  const structure_type = determineStructureType(mainType);

  return {
    core_problem,
    solution,
    rationale,
    edge_cases,
    structure_type
  };
}

function summarizeProblem(observations: Observation[]): string {
  if (observations.length === 0) return '';
  // Simple heuristic: use the title of the first bugfix
  return observations[0].title.replace(/^Fixed\s+/i, '');
}

function summarizeSolution(observations: Observation[]): string {
  // Extract solution pattern from high-work observations
  const titles = observations.map(o => o.title);
  return `Solution derived from ${observations.length} observations: ${titles.join(', ')}`;
}

function summarizeRationale(decisions: Observation[]): string {
  if (decisions.length === 0) return 'No explicit decisions recorded.';
  return decisions.map(d => d.title).join('; ');
}

function identifyEdgeCases(discoveries: Observation[]): EdgeCase[] {
  if (discoveries.length > 0) {
    return discoveries.map(d => ({
      description: d.title,
      resolution: 'Documented in original session'
    }));
  }

  // Return empty array if no discoveries found
  return [];
}

function determineStructureType(type: string): ExtractedPattern['structure_type'] {
  const typeMap: Record<string, ExtractedPattern['structure_type']> = {
    bugfix: 'pattern-focused',
    feature: 'tutorial',
    decision: 'standard',
    discovery: 'reference',
    change: 'standard'
  };

  return typeMap[type] || 'standard';
}
