let nextId = 1;
export const reportsStore = new Map();
export function addReport(data) {
    const report = {
        id: nextId++,
        case_code: data.case_code,
        category: data.category,
        description: data.description,
        evidence_url: data.evidence_url ?? null,
        status: data.status ?? 'SUBMITTED',
        status_update: data.status_update ?? null,
        created_at: data.created_at ?? new Date().toISOString()
    };
    reportsStore.set(report.case_code, report);
    return report;
}
// Seed initial reports including the sample from README.md
addReport({
    case_code: 'WD-A7K92M4QX81P',
    category: 'Security',
    description: 'There is a security issue that needs to be reviewed.',
    evidence_url: 'https://example.com/evidence',
    status: 'SUBMITTED',
    status_update: null,
    created_at: '2026-10-01T10:15:00.000Z'
});
addReport({
    case_code: 'WD-H93B7X2LQ490',
    category: 'Harassment',
    description: 'Unwarranted intimidation during department sprint retrospectives.',
    evidence_url: null,
    status: 'UNDER_REVIEW',
    status_update: 'Ethics and HR committee opened an inquiry on Oct 2nd.',
    created_at: '2026-10-02T08:30:00.000Z'
});
addReport({
    case_code: 'WD-C41M88Z99K12',
    category: 'Corruption',
    description: 'Vendor procurement anomalies in Q3 server hardware purchasing.',
    evidence_url: 'https://example.org/vendor-audit-notes.pdf',
    status: 'RESOLVED',
    status_update: 'Independent audit conducted. Vendor contract terminated and controls updated.',
    created_at: '2026-09-28T14:20:00.000Z'
});
