import secrets
import string
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Header, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from database import init_db, insert_report, get_report, list_reports, update_status
from schemas import (
    ReportCreate,
    ReportCreateResponse,
    StatusUpdate,
    StatusUpdateResponse,
    ReportResponse
)

MODERATOR_KEY = "WD-MOD-2026"
VALID_TRANSITIONS = {
    "SUBMITTED": ["UNDER_REVIEW"],
    "UNDER_REVIEW": ["RESOLVED", "DISMISSED"],
    "RESOLVED": [],
    "DISMISSED": []
}

app = FastAPI(
    title="WhistleDrop",
    description="WhistleDrop — Speak Without Being Seen. A confidential reporting backend system allowing individuals to submit anonymous reports, track case status via secure case codes, and enabling moderators to manage workflow securely with SQLite persistence.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

def generate_case_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    rand_chars = "".join(secrets.choice(alphabet) for _ in range(12))
    return f"WD-{rand_chars}"

@app.get("/", summary="Home")
def home():
    return {"message": "Welcome to WhistleDrop - Speak Without Being Seen"}

@app.post(
    "/reports",
    response_model=ReportCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Report",
    description="Submit an anonymous incident report. Returns a unique case code for tracking."
)
def create_report(payload: ReportCreate):
    if not payload.category or not payload.category.strip():
        raise HTTPException(status_code=400, detail="Category is required and cannot be empty")
    
    if not payload.description or not payload.description.strip():
        raise HTTPException(status_code=422, detail="Description cannot be empty")

    case_code = generate_case_code()
    # Retry if code collisions (negligible probability)
    while get_report(case_code) is not None:
        case_code = generate_case_code()

    saved = insert_report(
        case_code=case_code,
        category=payload.category.strip(),
        description=payload.description.strip(),
        evidence_url=payload.evidence_url.strip() if payload.evidence_url else None
    )

    return {
        "message": "Report received successfully",
        "case_code": saved["case_code"],
        "category": saved["category"],
        "description": saved["description"],
        "evidence_url": saved["evidence_url"]
    }

@app.get(
    "/reports",
    response_model=List[ReportResponse],
    summary="Get All Reports",
    description="Moderator endpoint to view and filter reports. Requires X-Moderator-Key header."
)
def get_all_reports(
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    x_moderator_key: str = Header(..., alias="X-Moderator-Key", description="Moderator secret key")
):
    if x_moderator_key != MODERATOR_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized moderator access")
    
    if status and status not in ["SUBMITTED", "UNDER_REVIEW", "RESOLVED", "DISMISSED"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    return list_reports(category=category, status=status)

@app.get(
    "/reports/{case_code}",
    response_model=ReportResponse,
    summary="Get Report",
    description="Retrieve report details and status by case code for reporters."
)
def get_report_by_code(case_code: str):
    report = get_report(case_code)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.put(
    "/reports/{case_code}/status",
    response_model=StatusUpdateResponse,
    summary="Update Status",
    description="Update report status following valid transition workflow (SUBMITTED -> UNDER_REVIEW -> RESOLVED/DISMISSED). Requires X-Moderator-Key header."
)
def update_report_status(
    case_code: str,
    payload: StatusUpdate,
    x_moderator_key: str = Header(..., alias="X-Moderator-Key", description="Moderator secret key")
):
    if x_moderator_key != MODERATOR_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized moderator access")

    report = get_report(case_code)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    current_status = report["status"]
    allowed_next = VALID_TRANSITIONS.get(current_status, [])

    if payload.status not in allowed_next:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition from {current_status} to {payload.status}. Allowed: {allowed_next}"
        )

    updated = update_status(
        case_code=case_code,
        new_status=payload.status,
        status_update=payload.status_update
    )

    return {
        "message": "Report status updated successfully",
        "case_code": updated["case_code"],
        "status": updated["status"],
        "status_update": updated["status_update"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
