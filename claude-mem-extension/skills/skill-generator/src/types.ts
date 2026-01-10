// src/types.ts

export interface Observation {
  id: number;
  type: 'bugfix' | 'feature' | 'decision' | 'discovery' | 'change';
  title: string;
  read_tokens: number;
  work_tokens: number;
  timestamp: string;
  session_id: string;
}

export interface CandidateScore {
  observation: Observation;
  score: number;
  repetition: number;
  success: number;
  work_investment: number;
  pattern: string;
}

export interface SkillMetadata {
  name: string;
  description: string;
  version: string;
  generated: string;
  confidence: number;
  tags: string[];
  type: 'bugfix' | 'feature' | 'decision' | 'discovery' | 'change';
  source: {
    sessions: string[];
    observations: number[];
    project: string;
  };
  usage_count?: number;
  last_used?: string;
}

export interface SkillContent {
  metadata: SkillMetadata;
  sections: SkillSection[];
}

export interface SkillSection {
  type: 'problem' | 'solution' | 'rationale' | 'edge-cases' | 'examples' | 'overview';
  content: string;
}

export interface SkillIndex {
  version: string;
  last_updated: string;
  total_skills: number;
  skills: SkillMetadata[];
}
