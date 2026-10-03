export interface Report {
  id: number;
  case_code: string;
  category: string;
  description: string;
  evidence_url: string | null;
  status: 'SUBMITTED' | 'UNDER_REVIEW' | 'RESOLVED' | 'DISMISSED';
  status_update: string | null;
  created_at: string;
}

export const ALLOWED_STATUSES = [
  'SUBMITTED',
  'UNDER_REVIEW',
  'RESOLVED',
  'DISMISSED'
] as const;

export const DEFAULT_CATEGORIES = [
  'Security',
  'Harassment',
  'Corruption',
  'Technical',
  'Financial Fraud',
  'Safety Violation',
  'Other'
];

export const VALID_TRANSITIONS: Record<string, string[]> = {
  SUBMITTED: ['UNDER_REVIEW'],
  UNDER_REVIEW: ['RESOLVED', 'DISMISSED'],
  RESOLVED: [],
  DISMISSED: []
};
