import express, { Request, Response } from 'express';
import cors from 'cors';
import crypto from 'node:crypto';
import { ALLOWED_CATEGORIES, ALLOWED_STATUSES, VALID_TRANSITIONS, Report } from './types.js';
import { reportsStore, addReport } from './db.js';
import { openApiSpec } from './openapi.js';
import { getDocsHtml } from './ui.js';

const app = express();
const PORT = parseInt(process.env.PORT || '3000', 10);
const MODERATOR_KEY = process.env.MODERATOR_KEY || 'WD-MOD-2026';

app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['*']
}));

app.use(express.json());

function generateCaseCode(): string {
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let result = '';
  const randomBytes = crypto.randomBytes(12);
  for (let i = 0; i < 12; i++) {
    result += alphabet[randomBytes[i] % alphabet.length];
  }
  return `WD-${result}`;
}

function checkModeratorKey(req: Request, res: Response): boolean {
  const headerKey = req.header('x-moderator-key');
  if (headerKey !== MODERATOR_KEY) {
    res.status(401).json({ detail: 'Unauthorized moderator access' });
    return false;
  }
  return true;
}

// 1. Home endpoint
app.get('/', (req: Request, res: Response) => {
  const acceptHeader = req.header('accept') || '';
  if (acceptHeader.includes('text/html') && req.query.format !== 'json') {
    return res.redirect('/docs');
  }
  return res.json({
    message: 'Welcome to WhistleDrop - Speak Without Being Seen'
  });
});

// Swagger UI & OpenAPI Specification
app.get(['/docs', '/swagger'], (_req: Request, res: Response) => {
  return res.type('html').send(getDocsHtml());
});

app.get('/openapi.json', (_req: Request, res: Response) => {
  return res.json(openApiSpec);
});

// 2. Submit a Report
app.post('/reports', (req: Request, res: Response) => {
  const { category, description, evidence_url } = req.body || {};

  if (!category || typeof category !== 'string' || !ALLOWED_CATEGORIES.includes(category as any)) {
    return res.status(400).json({ detail: 'Invalid category' });
  }

  if (!description || typeof description !== 'string' || description.trim().length === 0) {
    return res.status(422).json({ detail: 'Description cannot be empty' });
  }

  const case_code = generateCaseCode();
  const dbReport = addReport({
    case_code,
    category: category as Report['category'],
    description: description.trim(),
    evidence_url: evidence_url ? String(evidence_url).trim() : null
  });

  return res.status(201).json({
    message: 'Report received successfully',
    case_code: dbReport.case_code,
    category: dbReport.category,
    description: dbReport.description,
    evidence_url: dbReport.evidence_url
  });
});

// 3. Track a Report by Case Code (Public)
app.get('/reports/:case_code', (req: Request, res: Response) => {
  const case_code = String(req.params.case_code);
  const report = reportsStore.get(case_code);

  if (!report) {
    return res.status(404).json({ detail: 'Report not found' });
  }

  return res.json(report);
});

// 4. View and Filter Reports (Moderator)
app.get('/reports', (req: Request, res: Response) => {
  if (!checkModeratorKey(req, res)) return;

  const { category, status } = req.query;

  if (status && !ALLOWED_STATUSES.includes(status as any)) {
    return res.status(400).json({ detail: 'Invalid status' });
  }

  let reports = Array.from(reportsStore.values());

  if (category) {
    reports = reports.filter(r => r.category === category);
  }

  if (status) {
    reports = reports.filter(r => r.status === status);
  }

  return res.json(reports);
});

// 5. Update Report Status (Moderator)
app.put('/reports/:case_code/status', (req: Request, res: Response) => {
  if (!checkModeratorKey(req, res)) return;

  const case_code = String(req.params.case_code);
  const report = reportsStore.get(case_code);

  if (!report) {
    return res.status(404).json({ detail: 'Report not found' });
  }

  const { status, status_update } = req.body || {};

  if (!status || !ALLOWED_STATUSES.includes(status as any)) {
    return res.status(400).json({ detail: 'Invalid status' });
  }

  const validTransitions = VALID_TRANSITIONS[report.status] || [];

  if (!validTransitions.includes(status)) {
    return res.status(400).json({
      detail: `Invalid status transition from ${report.status} to ${status}`
    });
  }

  report.status = status;
  report.status_update = typeof status_update === 'string' ? status_update.trim() : null;

  return res.json({
    message: 'Report status updated successfully',
    case_code: report.case_code,
    status: report.status,
    status_update: report.status_update
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`WhistleDrop server running at http://0.0.0.0:${PORT}`);
  console.log(`Swagger documentation available at http://0.0.0.0:${PORT}/docs`);
});
