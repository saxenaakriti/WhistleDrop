import sqlite3
import os
import shutil
from datetime import datetime
from typing import Optional, List, Dict, Any

def get_db_path() -> str:
    custom = os.environ.get("WHISTLEDROP_DB")
    if custom:
        return custom
    if os.environ.get("VERCEL"):
        tmp_db = "/tmp/whistledrop.db"
        if not os.path.exists(tmp_db) and os.path.exists("whistledrop.db"):
            try:
                shutil.copyfile("whistledrop.db", tmp_db)
            except Exception:
                pass
        return tmp_db
    return "whistledrop.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_code TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        evidence_url TEXT,
        status TEXT NOT NULL DEFAULT 'SUBMITTED',
        status_update TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_reports_case_code ON reports(case_code)
    ''')
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status)
    ''')
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_reports_category ON reports(category)
    ''')
    
    # Check if empty, seed initial records
    cursor.execute('SELECT COUNT(*) as count FROM reports')
    if cursor.fetchone()['count'] == 0:
        cursor.execute('''
        INSERT INTO reports (case_code, category, description, evidence_url, status, status_update, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'WD-A7K92M4QX81P',
            'Security',
            'There is a security issue that needs to be reviewed.',
            'https://example.com/evidence',
            'SUBMITTED',
            None,
            '2026-10-01T10:15:00.000Z'
        ))
        cursor.execute('''
        INSERT INTO reports (case_code, category, description, evidence_url, status, status_update, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'WD-H93B7X2LQ490',
            'Harassment',
            'Unwarranted intimidation during department sprint retrospectives.',
            None,
            'UNDER_REVIEW',
            'Ethics and HR committee opened an inquiry on Oct 2nd.',
            '2026-10-02T08:30:00.000Z'
        ))
        cursor.execute('''
        INSERT INTO reports (case_code, category, description, evidence_url, status, status_update, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'WD-C41M88Z99K12',
            'Corruption',
            'Vendor procurement anomalies in Q3 server hardware purchasing.',
            'https://example.org/vendor-audit-notes.pdf',
            'RESOLVED',
            'Independent audit conducted. Vendor contract terminated and controls updated.',
            '2026-09-28T14:20:00.000Z'
        ))
    conn.commit()
    conn.close()

def insert_report(case_code: str, category: str, description: str, evidence_url: Optional[str] = None) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.utcnow().isoformat() + "Z"
    cursor.execute('''
    INSERT INTO reports (case_code, category, description, evidence_url, status, status_update, created_at)
    VALUES (?, ?, ?, ?, 'SUBMITTED', NULL, ?)
    ''', (case_code, category, description, evidence_url, created_at))
    conn.commit()
    report_id = cursor.lastrowid
    conn.close()
    return {
        "id": report_id,
        "case_code": case_code,
        "category": category,
        "description": description,
        "evidence_url": evidence_url,
        "status": "SUBMITTED",
        "status_update": None,
        "created_at": created_at
    }

def get_report(case_code: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports WHERE case_code = ?', (case_code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def list_reports(category: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM reports WHERE 1=1'
    params = []
    if category:
        query += ' AND category = ?'
        params.append(category)
    if status:
        query += ' AND status = ?'
        params.append(status)
    query += ' ORDER BY id DESC'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_status(case_code: str, new_status: str, status_update: Optional[str] = None) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE reports
    SET status = ?, status_update = ?
    WHERE case_code = ?
    ''', (new_status, status_update, case_code))
    conn.commit()
    cursor.execute('SELECT * FROM reports WHERE case_code = ?', (case_code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
