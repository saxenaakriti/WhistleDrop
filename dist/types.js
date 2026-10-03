export const ALLOWED_STATUSES = [
    'SUBMITTED',
    'UNDER_REVIEW',
    'RESOLVED',
    'DISMISSED'
];
export const ALLOWED_CATEGORIES = [
    'Security',
    'Harassment',
    'Corruption',
    'Technical',
    'Other'
];
export const VALID_TRANSITIONS = {
    SUBMITTED: ['UNDER_REVIEW'],
    UNDER_REVIEW: ['RESOLVED', 'DISMISSED'],
    RESOLVED: [],
    DISMISSED: []
};
