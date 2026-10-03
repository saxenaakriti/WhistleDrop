# WhistleDrop — Speak Without Being Seen 🛡️

**Live Deployment & Interactive API Docs:**  
👉 [https://whistle-drop-jwy7.vercel.app/docs#/default/create_report_reports_post](https://whistle-drop-jwy7.vercel.app/docs#/default/create_report_reports_post)

WhistleDrop is a confidential, anonymous incident reporting system built with **Python & SQLite**. It allows individuals to submit reports safely without creating accounts or revealing their identity, track investigation progress using cryptographic case codes, and enables moderators to review and update case statuses through a validated workflow.

---

## 1. Setup Instructions

Follow these step-by-step instructions to run the project locally on your machine:

### Prerequisites
- **Python 3.8+** installed on your system. You can check by running:
  ```bash
  python3 --version
  ```
- **Git** installed on your system.

---

### Option A: Running with FastAPI & Uvicorn (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saxenaakriti/WhistleDrop.git
   cd WhistleDrop
   ```

2. **Create and activate a virtual environment:**
   - On macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Explore the API:**
   - Interactive Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Alternative ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Option B: Zero-Dependency Standalone Mode

If you do not want to install any external packages, WhistleDrop can run directly using Python's built-in standard library (`sqlite3`, `http.server`, `json`):

```bash
python3 standalone.py
```
The server will start on [http://localhost:8000](http://localhost:8000).

---

### Running Automated Unit Tests

To test the database operations, constraints, and queries:

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

## 2. API Endpoints and Their Purpose

| Method | Endpoint | Access | Purpose |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Public | Welcome message and health confirmation. |
| `POST` | `/reports` | Public | Submit a new anonymous incident report. Returns a generated 12-character cryptographic case code. |
| `GET` | `/reports/{case_code}` | Public | Look up the current status and moderator notes of a report using its case code. |
| `GET` | `/reports` | Moderator Only | View and filter all submitted incident reports. Requires `X-Moderator-Key` header. |
| `PUT` | `/reports/{case_code}/status` | Moderator Only | Update the investigation status and add notes for a case following the state machine. Requires `X-Moderator-Key` header. |

---

## 3. How Anonymity is Maintained

WhistleDrop is built from the ground up to protect the reporter's privacy:

1. **No User Accounts or Sign-ups**:
   - The application does not collect names, email addresses, phone numbers, or passwords.
   - Anyone can submit a report immediately without creating an account or logging in.

2. **No IP Logging or Digital Fingerprinting**:
   - The database schema only records the incident data (`case_code`, `category`, `description`, `evidence_url`, `status`, `status_update`, and `created_at`).
   - Client IP addresses, browser fingerprints, and network headers are intentionally never saved to the database.

3. **High-Entropy Cryptographic Case Codes**:
   - Case codes are generated using Python’s `secrets` module (a Cryptographically Secure Pseudo-Random Number Generator, CSPRNG).
   - Format: `WD-` followed by 12 random alphanumeric characters (e.g. `WD-A7K92M4QX81P`).
   - With 36 possible characters and 12 positions (36¹² ≈ 4.73 × 10¹⁸ combinations), it is virtually impossible for anyone to guess or brute-force another person's case code.

4. **Isolated Access Control**:
   - Reporters can only access their specific report by providing their exact case code.
   - The list of all submissions is protected by a moderator key (`X-Moderator-Key`), preventing unauthorized users from browsing other reports.

---

## 4. Example Requests and Responses

You can test these commands in your terminal using `curl` or by using the Swagger UI at [https://whistle-drop-jwy7.vercel.app/docs](https://whistle-drop-jwy7.vercel.app/docs).

### 1. Submit an Anonymous Report
* **Endpoint:** `POST /reports`
* **cURL Request:**
  ```bash
  curl -X POST "https://whistle-drop-jwy7.vercel.app/reports" \
    -H "Content-Type: application/json" \
    -d '{
      "category": "Security",
      "description": "Unauthorized individual seen accessing server room after business hours.",
      "evidence_url": "https://example.com/evidence-photo.jpg"
    }'
  ```
* **Response (`201 Created`):**
  ```json
  {
    "message": "Report received successfully",
    "case_code": "WD-A7K92M4QX81P",
    "category": "Security",
    "description": "Unauthorized individual seen accessing server room after business hours.",
    "evidence_url": "https://example.com/evidence-photo.jpg"
  }
  ```

---

### 2. Track Report Status (Public)
* **Endpoint:** `GET /reports/{case_code}`
* **cURL Request:**
  ```bash
  curl -X GET "https://whistle-drop-jwy7.vercel.app/reports/WD-A7K92M4QX81P"
  ```
* **Response (`200 OK`):**
  ```json
  {
    "id": 1,
    "case_code": "WD-A7K92M4QX81P",
    "category": "Security",
    "description": "Unauthorized individual seen accessing server room after business hours.",
    "evidence_url": "https://example.com/evidence-photo.jpg",
    "status": "SUBMITTED",
    "status_update": null,
    "created_at": "2026-10-01T10:15:00.000Z"
  }
  ```

---

### 3. View All Reports (Moderator)
* **Endpoint:** `GET /reports?category=Security&status=SUBMITTED`
* **cURL Request:**
  ```bash
  curl -X GET "https://whistle-drop-jwy7.vercel.app/reports?category=Security&status=SUBMITTED" \
    -H "X-Moderator-Key: WD-MOD-2026"
  ```
* **Response (`200 OK`):**
  ```json
  [
    {
      "id": 1,
      "case_code": "WD-A7K92M4QX81P",
      "category": "Security",
      "description": "Unauthorized individual seen accessing server room after business hours.",
      "evidence_url": "https://example.com/evidence-photo.jpg",
      "status": "SUBMITTED",
      "status_update": null,
      "created_at": "2026-10-01T10:15:00.000Z"
    }
  ]
  ```

---

### 4. Update Report Status (Moderator)
* **Endpoint:** `PUT /reports/{case_code}/status`
* **cURL Request:**
  ```bash
  curl -X PUT "https://whistle-drop-jwy7.vercel.app/reports/WD-A7K92M4QX81P/status" \
    -H "X-Moderator-Key: WD-MOD-2026" \
    -H "Content-Type: application/json" \
    -d '{
      "status": "UNDER_REVIEW",
      "status_update": "Ethics and Security team assigned to investigate entry badge logs."
    }'
  ```
* **Response (`200 OK`):**
  ```json
  {
    "message": "Report status updated successfully",
    "case_code": "WD-A7K92M4QX81P",
    "status": "UNDER_REVIEW",
    "status_update": "Ethics and Security team assigned to investigate entry badge logs."
  }
  ```

---

## 5. Important Assumptions and Design Decisions

1. **State Machine for Case Statuses**:
   - Rather than allowing any status to change randomly, transitions must strictly follow this workflow:
     ```text
     [ SUBMITTED ] ──> [ UNDER_REVIEW ] ──┬──> [ RESOLVED ]
                                          └──> [ DISMISSED ]
     ```
   - *Why:* A report cannot be marked `RESOLVED` directly from `SUBMITTED` without an active review phase. Once marked `RESOLVED` or `DISMISSED`, it reaches a terminal state to preserve investigation records.

2. **Cryptographic Case Code in Place of Accounts**:
   - *Why:* Asking a whistleblower to create an account requires personal identifiers (such as an email). A single random case code allows the user to check updates anytime while keeping their identity 100% disconnected from the submission.

3. **SQLite Database Choice**:
   - *Why:* SQLite is lightweight, serverless, and file-based. It requires zero configuration, making it fast to deploy and ideal for small to mid-sized applications.
   - *Optimization:* Database indexes are added to `case_code` (unique index), `status`, and `category` so searching and filtering remain fast as data grows.

4. **Shared Secret Key for Moderator Authentication**:
   - *Why:* To keep the backend code simple, readable, and lightweight for a student project, moderator protection is implemented via an `X-Moderator-Key` header (`WD-MOD-2026`) instead of a complex multi-table user/password management system.

5. **Self-Documenting REST API with FastAPI**:
   - *Why:* FastAPI automatically generates interactive OpenAPI documentation (`/docs`), making it easy for reviewers, teammates, and evaluators to test API endpoints directly in the browser without third-party software like Postman.
