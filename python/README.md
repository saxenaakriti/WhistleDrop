# WhistleDrop — Python + SQLite Backend

This directory contains the complete Python + SQLite implementation of WhistleDrop.

## Features

- **SQLite Database**: Persistent relational storage (`whistledrop.db`) with automatic schema initialization and indexed queries (`case_code`, `status`, `category`).
- **FastAPI Framework**: Automatic interactive Swagger UI at `/docs` and ReDoc at `/redoc`.
- **Zero-Dependency Standalone Mode**: Includes `standalone.py` which runs purely on Python standard library (`sqlite3` and `http.server`) with no `pip install` required.
- **Workflow State Engine**: Enforces valid status transitions:
  - `SUBMITTED` ➔ `UNDER_REVIEW` ➔ `RESOLVED` or `DISMISSED`
- **Moderator Authentication**: Protected endpoints require `X-Moderator-Key: WD-MOD-2026`.
- **Test Suite**: Built-in unit tests verifying database queries and transitions (`python test_api.py`).

---

## Quick Start Options

### Option 1: FastAPI + SQLite (Recommended)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with Uvicorn**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

3. **Open Interactive Swagger UI**:
   - Browser: `http://localhost:8000/docs`
   - Alternative ReDoc: `http://localhost:8000/redoc`

---

### Option 2: Standalone Mode (Zero Dependencies)

No `pip install` needed! Uses standard library `sqlite3` and `http.server`:

```bash
python standalone.py
```
Server starts on `http://localhost:8000`.

---

## Running Automated Tests

Run the built-in SQLite test suite:

```bash
python test_api.py
```

---

## Database Schema (`whistledrop.db`)

```sql
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_code TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    evidence_url TEXT,
    status TEXT NOT NULL DEFAULT 'SUBMITTED',
    status_update TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reports_case_code ON reports(case_code);
CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
CREATE INDEX IF NOT EXISTS idx_reports_category ON reports(category);
```
