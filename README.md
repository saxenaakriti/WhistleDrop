# WhistleDrop — Speak Without Being Seen 

A confidential, anonymous incident reporting backend system allowing individuals to submit reports, track case status securely using difficult-to-guess case codes, and enabling moderators to manage review workflows with **Python & SQLite**.

---

## Application Screenshots & Verification

| Screen | Description | Preview |
|---|---|---|
| **API Endpoints Overview** | Swagger UI listing all WhistleDrop endpoints (`GET /`, `POST /reports`, `GET /reports`, `GET /reports/{case_code}`, `PUT /reports/{case_code}/status`) | `screenshots/Screenshot (247).png` |
| **Submit Report (201 Created)** | Submitting a report with `category`, `description`, returning unique case code | `screenshots/Screenshot (248).png` |
| **List Reports (200 OK)** | Fetching list of all submitted reports via moderator access | `screenshots/Screenshot (249).png` |
| **Moderator Filter** | Filtering reports by category (`Security`) and status (`SUBMITTED`) using `X-Moderator-Key` | `screenshots/Screenshot (250).png` |
| **Track Report by Case Code** | Public case status tracking by unique case code | `screenshots/Screenshot (251).png` |
| **Update Report Status Form** | Moderator status transition form (`SUBMITTED` -> `UNDER_REVIEW`) | `screenshots/Screenshot (252).png` |
| **Status Updated Successfully** | Successful status transition response with moderator notes | `screenshots/Screenshot (253).png` |

---

## Tech Stack

* **Language:** Python 3.8+
* **Framework:** FastAPI
* **Database:** SQLite 3 (`whistledrop.db`)
* **Validation:** Pydantic
* **Documentation:** Swagger UI / OpenAPI 3.0 (`/docs`) & ReDoc (`/redoc`)
* **Testing:** Python `unittest`

---

## Key Features

* **Anonymous Submission**: No user account, email, or identity required.
* **Cryptographic Case Codes**: High-entropy unique identifiers (e.g. `WD-A7K92M4QX81P`) generated using `secrets`.
* **Category & Description Enforcement**: Strict validation for incident category and description.
* **SQLite Relational Persistence**: Auto-initialized table with optimized indexes on `case_code`, `status`, and `category`.
* **Public Tracking**: Anyone with a valid case code can query status updates without authentication.
* **Protected Moderator Access**: Role authorization enforced via secret `X-Moderator-Key: WD-MOD-2026`.
* **Workflow State Machine**: Enforces valid status transitions:
  `SUBMITTED` ➔ `UNDER_REVIEW` ➔ `RESOLVED` or `DISMISSED`
* **Zero-Dependency Mode**: Includes `standalone.py` to run directly on standard Python library.

---

## Project Structure

```
├── database.py       # SQLite connection, schema creation, indexed queries
├── main.py           # FastAPI application & API route handlers
├── schemas.py        # Pydantic request/response validation models
├── standalone.py     # Standalone Python runner (zero pip dependencies)
├── test_api.py       # Automated unit test suite
├── requirements.txt  # Python package dependencies
├── whistledrop.db    # SQLite database file (pre-seeded)
├── screenshots/      # Application screenshots (247-253)
└── README.md         # Documentation
```

---

## Quick Start

### Option 1: FastAPI + SQLite (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saxenaakriti/WhistleDrop.git
   cd WhistleDrop
   ```

2. **Create virtual environment & install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start the API server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Access the Interactive Docs:**
   * Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   * ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Option 2: Standalone Mode (Zero Dependencies)

If you don't have `pip` installed, run directly with standard Python 3:

```bash
python3 standalone.py
```
* Server starts on [http://localhost:8000](http://localhost:8000).

---

## Running Unit Tests

Run the built-in SQLite test suite:

```bash
python3 test_api.py
```

Expected output:
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.005s

OK
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

---

## API Reference

### 1. Root / Welcome
* **Endpoint:** `GET /`
* **Response:**
  ```json
  {
    "message": "Welcome to WhistleDrop - Speak Without Being Seen"
  }
  ```

---

### 2. Submit Anonymous Report
* **Endpoint:** `POST /reports`
* **Request Body:**
  ```json
  {
    "category": "Security",
    "description": "Unauthorized access attempt observed in staging environment.",
    "evidence_url": "https://example.com/log.txt"
  }
  ```
* **Response (201 Created):**
  ```json
  {
    "message": "Report received successfully",
    "case_code": "WD-ZEYIW5GKQD3P",
    "category": "Security",
    "description": "Unauthorized access attempt observed in staging environment.",
    "evidence_url": "https://example.com/log.txt"
  }
  ```

---

### 3. Track Report Status (Public)
* **Endpoint:** `GET /reports/{case_code}`
* **Response (200 OK):**
  ```json
  {
    "id": 1,
    "case_code": "WD-A7K92M4QX81P",
    "category": "Security",
    "description": "There is a security issue that needs to be reviewed.",
    "evidence_url": "https://example.com/evidence",
    "status": "SUBMITTED",
    "status_update": null,
    "created_at": "2026-10-01T10:15:00.000Z"
  }
  ```

---

### 4. Moderator: List & Filter Reports
* **Endpoint:** `GET /reports?category=Security&status=SUBMITTED`
* **Headers:** `X-Moderator-Key: WD-MOD-2026`
* **Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "case_code": "WD-A7K92M4QX81P",
      "category": "Security",
      "description": "There is a security issue that needs to be reviewed.",
      "evidence_url": "https://example.com/evidence",
      "status": "SUBMITTED",
      "status_update": null,
      "created_at": "2026-10-01T10:15:00.000Z"
    }
  ]
  ```

---

### 5. Moderator: Update Report Status
* **Endpoint:** `PUT /reports/{case_code}/status`
* **Headers:** `X-Moderator-Key: WD-MOD-2026`
* **Request Body:**
  ```json
  {
    "status": "UNDER_REVIEW",
    "status_update": "Ethics committee inquiry opened."
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "message": "Report status updated successfully",
    "case_code": "WD-A7K92M4QX81P",
    "status": "UNDER_REVIEW",
    "status_update": "Ethics committee inquiry opened."
  }
  ```

---

## Status Transition Rules

```
[ SUBMITTED ]
      │
      ▼
[ UNDER_REVIEW ]
   │         │
   ▼         ▼
[RESOLVED] [DISMISSED]
```

Any attempt to jump illegally (e.g. `SUBMITTED` ➔ `RESOLVED` directly) returns HTTP `400 Bad Request`.
