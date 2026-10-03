#!/usr/bin/env python3
"""
WhistleDrop — Standalone Python + SQLite Server (Zero External Dependencies)
Runs with standard Python 3.8+ library alone (sqlite3, http.server, urllib, json).
"""

import http.server
import json
import os
import re
import secrets
import sqlite3
import string
import sys
from datetime import datetime
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get("PORT", 8000))
DB_PATH = os.environ.get("WHISTLEDROP_DB", "whistledrop.db")
MODERATOR_KEY = "WD-MOD-2026"

VALID_TRANSITIONS = {
    "SUBMITTED": ["UNDER_REVIEW"],
    "UNDER_REVIEW": ["RESOLVED", "DISMISSED"],
    "RESOLVED": [],
    "DISMISSED": []
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
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
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_case_code ON reports(case_code)')
    cursor.execute('SELECT COUNT(*) as count FROM reports')
    if cursor.fetchone()['count'] == 0:
        cursor.execute('''
        INSERT INTO reports (case_code, category, description, evidence_url, status, status_update, created_at)
        VALUES ('WD-A7K92M4QX81P', 'Security', 'There is a security issue that needs to be reviewed.', 'https://example.com/evidence', 'SUBMITTED', NULL, '2026-10-01T10:15:00.000Z')
        ''')
    conn.commit()
    conn.close()

def generate_case_code():
    alphabet = string.ascii_uppercase + string.digits
    return f"WD-{''.join(secrets.choice(alphabet) for _ in range(12))}"

class WhistleDropHandler(http.server.BaseHTTPRequestHandler):
    def send_json(self, status_code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Moderator-Key")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Moderator-Key")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # 1. Home
        if path == "/":
            return self.send_json(200, {"message": "Welcome to WhistleDrop - Speak Without Being Seen (Python SQLite)"})

        # 2. Get All Reports
        if path == "/reports":
            mod_key = self.headers.get("X-Moderator-Key")
            if mod_key != MODERATOR_KEY:
                return self.send_json(401, {"detail": "Unauthorized moderator access"})
            
            status_param = query.get("status", [None])[0]
            cat_param = query.get("category", [None])[0]

            if status_param and status_param not in ["SUBMITTED", "UNDER_REVIEW", "RESOLVED", "DISMISSED"]:
                return self.send_json(400, {"detail": "Invalid status"})

            conn = get_db()
            cursor = conn.cursor()
            sql = "SELECT * FROM reports WHERE 1=1"
            params = []
            if cat_param:
                sql += " AND category = ?"
                params.append(cat_param)
            if status_param:
                sql += " AND status = ?"
                params.append(status_param)
            sql += " ORDER BY id DESC"
            cursor.execute(sql, params)
            rows = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return self.send_json(200, rows)

        # 3. Get Single Report by Case Code
        match = re.match(r"^/reports/([A-Za-z0-9_-]+)$", path)
        if match:
            case_code = match.group(1)
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reports WHERE case_code = ?", (case_code,))
            row = cursor.fetchone()
            conn.close()
            if not row:
                return self.send_json(404, {"detail": "Report not found"})
            return self.send_json(200, dict(row))

        return self.send_json(404, {"detail": "Not Found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/reports":
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(raw_body.decode("utf-8"))
            except Exception:
                return self.send_json(400, {"detail": "Invalid JSON body"})

            category = data.get("category")
            description = data.get("description")
            evidence_url = data.get("evidence_url")

            if not category or not isinstance(category, str) or not category.strip():
                return self.send_json(400, {"detail": "Category is required and cannot be empty"})

            if not description or not isinstance(description, str) or not description.strip():
                return self.send_json(422, {"detail": "Description cannot be empty"})

            case_code = generate_case_code()
            created_at = datetime.utcnow().isoformat() + "Z"

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO reports (case_code, category, description, evidence_url, status, status_update, created_at)
            VALUES (?, ?, ?, ?, 'SUBMITTED', NULL, ?)
            ''', (case_code, category.strip(), description.strip(), evidence_url.strip() if evidence_url else None, created_at))
            conn.commit()
            conn.close()

            return self.send_json(201, {
                "message": "Report received successfully",
                "case_code": case_code,
                "category": category.strip(),
                "description": description.strip(),
                "evidence_url": evidence_url.strip() if evidence_url else None
            })

        return self.send_json(404, {"detail": "Not Found"})

    def do_PUT(self):
        parsed = urlparse(self.path)
        match = re.match(r"^/reports/([A-Za-z0-9_-]+)/status$", parsed.path)
        if match:
            case_code = match.group(1)
            mod_key = self.headers.get("X-Moderator-Key")
            if mod_key != MODERATOR_KEY:
                return self.send_json(401, {"detail": "Unauthorized moderator access"})

            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(raw_body.decode("utf-8"))
            except Exception:
                return self.send_json(400, {"detail": "Invalid JSON body"})

            new_status = data.get("status")
            status_update = data.get("status_update")

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reports WHERE case_code = ?", (case_code,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return self.send_json(404, {"detail": "Report not found"})

            current_status = row["status"]
            allowed_next = VALID_TRANSITIONS.get(current_status, [])
            if new_status not in allowed_next:
                conn.close()
                return self.send_json(400, {"detail": f"Invalid transition from {current_status} to {new_status}. Allowed: {allowed_next}"})

            cursor.execute("UPDATE reports SET status = ?, status_update = ? WHERE case_code = ?", (new_status, status_update, case_code))
            conn.commit()
            conn.close()

            return self.send_json(200, {
                "message": "Report status updated successfully",
                "case_code": case_code,
                "status": new_status,
                "status_update": status_update
            })

        return self.send_json(404, {"detail": "Not Found"})

if __name__ == "__main__":
    init_db()
    print(f"🚀 WhistleDrop Python + SQLite server listening on http://0.0.0.0:{PORT}")
    server = http.server.HTTPServer(("0.0.0.0", PORT), WhistleDropHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
