# WhistleDrop — Speak Without Being Seen 🛡️

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite 3](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tests Passing](https://img.shields.io/badge/Tests-Passing-success?style=for-the-badge&logo=pytest&logoColor=white)](test_api.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

> **WhistleDrop** is a confidential, anonymous incident reporting backend system built with **Python 3 & SQLite**. It allows individuals to securely submit reports without accounts or identities, track their investigation via cryptographic case codes, and enables authorized moderators to manage investigation workflows through a validated state machine.

---

## 📸 Application Screenshots & Verification

The backend includes interactive **Swagger UI / OpenAPI documentation** at `/docs`. Below is the visual proof of functionality across all core endpoints:

<details open>
<summary><b>1. Swagger UI & API Endpoints Overview</b></summary>
<br>
Interactive documentation displaying all endpoints: <code>GET /</code>, <code>POST /reports</code>, <code>GET /reports</code>, <code>GET /reports/{case_code}</code>, and <code>PUT /reports/{case_code}/status</code>.<br><br>
<img src="screenshots/Screenshot%20(247).png" alt="WhistleDrop Swagger UI Overview" width="100%" />
</details>

<br>

<details>
<summary><b>2. Anonymous Report Submission (POST /reports — 201 Created)</b></summary>
<br>
Submitting an incident with category, description, and optional evidence URL. The server creates the report in SQLite and returns a unique case code (e.g. <code>WD-ZEYIW5GKQD3P</code>).<br><br>
<img src="screenshots/Screenshot%20(248).png" alt="POST /reports 201 Created" width="100%" />
</details>

<br>

<details>
<summary><b>3. Moderator Reports Listing (GET /reports — 200 OK)</b></summary>
<br>
Moderator retrieves submitted reports filtered by criteria, complete with case codes, timestamps, and investigation status.<br><br>
<img src="screenshots/Screenshot%20(249).png" alt="GET /reports 200 OK" width="100%" />
</details>

<br>

<details>
<summary><b>4. Moderator Filtering & Authentication Header</b></summary>
<br>
Demonstration of query parameter filtering (<code>category=Security</code>, <code>status=SUBMITTED</code>) and secret header authentication (<code>X-Moderator-Key: WD-MOD-2026</code>).<br><br>
<img src="screenshots/Screenshot%20(250).png" alt="Moderator Query Filters" width="100%" />
</details>

<br>

<details>
<summary><b>5. Public Case Code Tracking (GET /reports/{case_code})</b></summary>
<br>
Reporters can query report status anytime using their case code (e.g. <code>WD-A7K92M4QX81P</code>) without logging in.<br><br>
<img src="screenshots/Screenshot%20(251).png" alt="Case Tracking by Code" width="100%" />
</details>

<br>

<details>
<summary><b>6. Status Transition Parameters (PUT /reports/{case_code}/status)</b></summary>
<br>
Moderator initiates workflow transition from <code>SUBMITTED</code> to <code>UNDER_REVIEW</code> with internal notes.<br><br>
<img src="screenshots/Screenshot%20(252).png" alt="Status Update Request" width="100%" />
</details>

<br>

<details>
<summary><b>7. Status Updated Successfully (200 OK)</b></summary>
<br>
Verification of successful state update persisted into SQLite database.<br><br>
<img src="screenshots/Screenshot%20(253).png" alt="Status Update Success" width="100%" />
</details>

---

## 🛠️ Architecture & Tech Stack

```
                   ┌──────────────────────────────┐
                   │        HTTP / REST API       │
                   └──────────────┬───────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         │                                                 │
         ▼                                                 ▼
┌──────────────────┐                              ┌──────────────────┐
│   FastAPI App    │                              │  Standalone App  │
│    (main.py)     │                              │ (standalone.py)  │
└────────┬─────────┘                              └────────┬─────────┘
         │                                                 │
         ▼                                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                    SQLite 3 (whistledrop.db)                       │
│  Indexed by: case_code (UNIQUE) | status | category                │
└────────────────────────────────────────────────────────────────────┘
```

* **Backend Framework:** FastAPI (High performance, auto-generated OpenAPI schemas)
* **Language:** Python 3.8+
* **Database:** SQLite 3 with indexing and connection pooling
* **Validation:** Pydantic (Type enforcement & schema serialization)
* **Zero-Dependency Runner:** `standalone.py` (Runs with Python standard library alone)
* **Testing:** Built-in Python `unittest` (`test_api.py`)

---

## ✨ Key Features

1. **100% Anonymous Reporting**: No sign-up, email, IP logging, or account creation required.
2. **Cryptographic Case Codes**: High-entropy identifiers (`WD-` prefix + 12 alphanumeric characters) generated via Python's CSPRNG `secrets` module.
3. **Relational SQLite Persistence**: Automatic schema migrations, transactions, and index optimizations on `case_code`, `status`, and `category`.
4. **Moderator Authentication**: Protected administrative operations guarded by secret header token (`X-Moderator-Key: WD-MOD-2026`).
5. **Enforced Status Workflow**: State machine prevents invalid transitions:
   ```
   [ SUBMITTED ] ──> [ UNDER_REVIEW ] ──┬──> [ RESOLVED ]
                                        └──> [ DISMISSED ]
   ```
6. **Zero-Dependency Mode**: Run on any computer with Python 3 without running `pip install`.

---

## 📂 Repository File Tree

```
WhistleDrop/
├── database.py       # SQLite connection, schema setup & indexed queries
├── main.py           # FastAPI application & API endpoints
├── schemas.py        # Pydantic request/response validation schemas
├── standalone.py     # Standalone Python runner (zero external dependencies)
├── test_api.py       # Automated SQLite unit test suite
├── requirements.txt  # Python package dependencies
├── whistledrop.db    # Seeded SQLite database
├── LICENSE           # MIT Open Source License
├── .gitignore        # Python gitignore
├── README.md         # Comprehensive documentation & API guide
└── screenshots/      # Application screenshots (247-253)
    ├── Screenshot (247).png
    ├── Screenshot (248).png
    ├── Screenshot (249).png
    ├── Screenshot (250).png
    ├── Screenshot (251).png
    ├── Screenshot (252).png
    └── Screenshot (253).png
```

---

## 🚀 Quick Start Guide

### Option 1: FastAPI with Uvicorn (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saxenaakriti/WhistleDrop.git
   cd WhistleDrop
   ```

2. **Create virtual environment & install requirements:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the development server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Open Interactive Docs:**
   * **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
   * **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Option 2: Zero-Dependency Standalone Mode

Run directly using Python's standard library (no `pip install` required):

```bash
python3 standalone.py
```
Server starts immediately on [http://localhost:8000](http://localhost:8000).

---

## 🧪 Running Automated Tests

Run the built-in SQLite test suite to verify database integrity, constraints, queries, and transitions:

```bash
python3 test_api.py
```

Expected output:
```text
....
----------------------------------------------------------------------
Ran 4 tests in 0.005s

OK
```

---

## 🗄️ Database Schema (`whistledrop.db`)

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

### Supported Categories:
* `Security`
* `Harassment`
* `Corruption`
* `Technical`
* `Other`

---

## 📡 API Reference & cURL Examples

### 1. Welcome / Home
```bash
curl -X GET "http://localhost:8000/"
```

### 2. Submit Anonymous Report
```bash
curl -X POST "http://localhost:8000/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Security",
    "description": "Unauthorized access attempt observed in server room.",
    "evidence_url": "https://example.com/logs.txt"
  }'
```

### 3. Track Report Status (Public)
```bash
curl -X GET "http://localhost:8000/reports/WD-A7K92M4QX81P"
```

### 4. Moderator: List & Filter Reports
```bash
curl -X GET "http://localhost:8000/reports?category=Security&status=SUBMITTED" \
  -H "X-Moderator-Key: WD-MOD-2026"
```

### 5. Moderator: Update Case Status
```bash
curl -X PUT "http://localhost:8000/reports/WD-A7K92M4QX81P/status" \
  -H "X-Moderator-Key: WD-MOD-2026" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "UNDER_REVIEW",
    "status_update": "Internal investigation team assigned to verify incident."
  }'
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
