# WhistleDrop — Speak Without Being Seen

WhistleDrop is a backend system for confidential reporting. It allows people to report problems inside an organization without creating an account or sharing their identity.

The system gives each report a unique case code. The reporter can use this case code later to check the status of the report without logging in.

Moderators can securely view reports, filter them, and update their status.

## Project Links

**GitHub Repository:**
[https://github.com/saxenaakriti/WhistleDrop](https://github.com/saxenaakriti/WhistleDrop)

**Live API:**
[https://whistle-drop-jwy7-2598up6yd-akriti14.vercel.app](https://whistle-drop-jwy7-2598up6yd-akriti14.vercel.app)

**Swagger API Documentation:**
[https://whistle-drop-jwy7-2598up6yd-akriti14.vercel.app/docs](https://whistle-drop-jwy7-2598up6yd-akriti14.vercel.app/docs)

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

## Features

* Anonymous report submission
* No account required for reporters
* Unique and difficult-to-guess case codes
* Case status tracking using the case code
* Moderator authentication using an API key
* Moderator report listing
* Filter reports by category
* Filter reports by status
* Status updates by moderators
* Status workflow validation
* Input validation
* Error handling for invalid requests
* SQLite database for storing reports
* Swagger/OpenAPI documentation
* Deployed API using Vercel

---

## Technologies Used

* Node.js & TypeScript
* Express.js
* Swagger UI / OpenAPI 3.0
* CORS

---

## Report Categories

A report can belong to one of the following categories:

* Security
* Harassment
* Corruption
* Technical
* Other

---

## Report Status Workflow

Reports follow this workflow:

```text
SUBMITTED
     ↓
UNDER_REVIEW
     ↓
RESOLVED
     OR
DISMISSED
```

A report cannot move backwards or skip an invalid status transition.

For example:

* `SUBMITTED → UNDER_REVIEW` ✅
* `UNDER_REVIEW → RESOLVED` ✅
* `UNDER_REVIEW → DISMISSED` ✅
* `SUBMITTED → RESOLVED` ❌
* `RESOLVED → UNDER_REVIEW` ❌

---

## How WhistleDrop Works

### 1. Submit a Report

A reporter sends:

* Category
* Description
* Optional evidence/reference URL

No account or personal information is required.

The system creates a unique case code such as:

```text
WD-A7K92M4QX81P
```

The reporter should save this case code because it is used to track the report later.

### 2. Track a Report

The reporter can use the case code to check:

* Category
* Description
* Current status
* Latest status update
* Other relevant report information

No login is required.

### 3. Moderator Access

Moderators use a moderator API key to access the report management endpoints.

They can:

* View reports
* Filter reports
* Change report status
* Add a short status update

The reporter's identity is not stored as part of the report.

---

# API Endpoints

## 1. Home

**GET /**

Used to check whether the API is running.

Example response:

```json
{
  "message": "Welcome to WhistleDrop - Speak Without Being Seen"
}
```

---

## 2. Submit a Report

**POST /reports**

Creates a new anonymous report.

### Example Request

```json
{
  "category": "Security",
  "description": "There is a security issue that needs to be reviewed.",
  "evidence_url": "https://example.com/evidence"
}
```

### Example Response

```json
{
  "message": "Report received successfully",
  "case_code": "WD-A7K92M4QX81P",
  "category": "Security",
  "description": "There is a security issue that needs to be reviewed.",
  "evidence_url": "https://example.com/evidence"
}
```

The case code is generated automatically by the server.

---

## 3. Track a Report

**GET /reports/{case_code}**

Used by reporters to check their report.

Example:

```text
GET /reports/WD-A7K92M4QX81P
```

No moderator key is required.

If the case code does not exist, the API returns:

```text
404 Report not found
```

---

## 4. View Reports

**GET /reports**

This endpoint is for moderators.

A moderator key must be provided in the request header.

Header:

```text
X-Moderator-Key: WD-MOD-2026
```

Example:

```text
GET /reports
```

---

## 5. Filter Reports

Moderators can filter reports using category or status.

### Filter by category

```text
GET /reports?category=Security
```

### Filter by status

```text
GET /reports?status=SUBMITTED
```

### Filter by both

```text
GET /reports?category=Security&status=SUBMITTED
```

The moderator key is required.

---

## 6. Update Report Status

**PUT /reports/{case_code}/status**

Used by moderators to update the status of a report.

Example:

```text
PUT /reports/WD-A7K92M4QX81P/status
```

Header:

```text
X-Moderator-Key: WD-MOD-2026
```

Request body:

```json
{
  "status": "UNDER_REVIEW",
  "status_update": "The report is currently being reviewed."
}
```

Example response:

```json
{
  "message": "Report status updated successfully",
  "case_code": "WD-A7K92M4QX81P",
  "status": "UNDER_REVIEW",
  "status_update": "The report is currently being reviewed."
}
```

---

# Moderator Authentication

Moderator endpoints are protected using a moderator API key.

The current development key is:

```text
WD-MOD-2026
```

The key is sent using the following header:

```text
X-Moderator-Key
```

Requests without the correct key receive:

```text
401 Unauthorized
```

In a production system, the moderator authentication should be replaced with a stronger authentication system and the secret should be stored securely as an environment variable.

---

# Privacy

Privacy is an important part of WhistleDrop.

The system does not require reporters to create an account or provide their name, email address, or other identity information.

Reports are identified using a generated case code instead.

The reporter uses the case code to track the report, while moderators only see the report information needed to review and manage it.

The current implementation does not intentionally store reporter identity information.

---

# Case Code Security

Each report receives a randomly generated case code.

The code uses Python's `secrets` module instead of a simple sequential number.

This makes case codes much harder to guess compared with codes such as:

```text
CASE-001
CASE-002
CASE-003
```

The generated format is:

```text
WD-XXXXXXXXXXXX
```

where the characters are randomly selected uppercase letters and numbers.

---

# Validation and Error Handling

The API validates incoming requests and returns appropriate error responses.

Examples include:

### Invalid category

```text
400 Invalid category
```

### Invalid status

```text
400 Invalid status
```

### Invalid status transition

For example, trying to change:

```text
UNDER_REVIEW → UNDER_REVIEW
```

returns an error because it is not a valid transition.

### Invalid case code

```text
404 Report not found
```

### Incorrect moderator key

```text
401 Unauthorized moderator access
```

---

# Database

WhistleDrop uses SQLite with SQLAlchemy.

The database stores information such as:

* Case code
* Category
* Description
* Evidence URL
* Status
* Status update
* Creation time

The SQLite database file is excluded from Git using `.gitignore`.

---

# Running the Project Locally

No environment variables or `.env` file are required. The server runs directly out of the box.

## 1. Install dependencies

```bash
npm install
```

## 2. Start the development server

```bash
npm run dev
```

The API will be available at:

```text
http://localhost:3000
```

Interactive Swagger documentation is available at:

```text
http://localhost:3000/docs
```

---

# Swagger Documentation

Interactive Swagger API documentation is provided directly at `/docs` using OpenAPI 3.0.0.

After starting the server, open:

```text
http://localhost:3000/docs
```

The Swagger page can be used to test all the API endpoints directly without needing a separate client.

---

# Project Structure

```text
WhistleDrop/
├── src/
│   ├── index.ts      # Express application and route handlers
│   ├── types.ts      # Data types, categories, and workflow transitions
│   ├── db.ts         # In-memory storage and seed data
│   ├── openapi.ts    # OpenAPI 3.0.0 specification
│   └── ui.ts         # Swagger UI HTML renderer
├── package.json      # Dependencies and npm scripts
├── tsconfig.json     # TypeScript configuration
├── .gitignore        # Git ignore rules
└── README.md         # Project documentation
```

The project does not require a frontend because the assignment focuses on building the backend API.

---

# HTTP Methods Used

| Method | Endpoint                      | Purpose              |
| ------ | ----------------------------- | -------------------- |
| GET    | `/`                           | Check API            |
| POST   | `/reports`                    | Create report        |
| GET    | `/reports/{case_code}`        | Track report         |
| GET    | `/reports`                    | View/filter reports  |
| PUT    | `/reports/{case_code}/status` | Update report status |

---

# Design Decisions

### No user accounts

The assignment requires anonymous reporting, so reporters do not create accounts.

### Case code instead of login

A generated case code allows a reporter to track a report without revealing their identity.

### Moderator API key

Moderator functionality is protected so that anyone cannot view or modify reports.

### Status workflow

A fixed status workflow prevents invalid changes to report status.

### SQLite

SQLite was used because it is simple and suitable for this project.

### Swagger

FastAPI's built-in Swagger documentation makes the API easy to demonstrate and test.

---

# Future Improvements

Some features that could be added in a larger production version include:

* Stronger moderator authentication
* Environment variables for secrets
* Moderator/admin dashboard
* File upload for evidence
* Permanent case closure
* Automated tests
* Additional privacy protections
* More advanced report filtering
* Production database such as PostgreSQL
* Audit logging for moderator actions

---

# Project Purpose

WhistleDrop was created as a backend project to demonstrate how an anonymous reporting system can be designed using FastAPI.

The main focus of the project is:

* Anonymous reporting
* Secure case tracking
* Moderator access
* Status management
* Input validation
* Privacy
* API documentation

The backend can be tested using Swagger/OpenAPI, Postman, cURL, or other API testing tools.
