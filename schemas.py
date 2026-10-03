from typing import Optional, Literal
from pydantic import BaseModel, Field

class ReportCreate(BaseModel):
    category: str = Field(..., min_length=1, description="Category of the incident (e.g. Security, Harassment, Corruption, Technical, etc.)", example="Security")
    description: str = Field(..., min_length=1, description="Detailed account of the incident", example="There is a security issue that needs to be reviewed.")
    evidence_url: Optional[str] = Field(None, description="Optional URL to supporting evidence", example="https://example.com/evidence")

class ReportCreateResponse(BaseModel):
    message: str = "Report received successfully"
    case_code: str
    category: str
    description: str
    evidence_url: Optional[str] = None

class StatusUpdate(BaseModel):
    status: Literal['SUBMITTED', 'UNDER_REVIEW', 'RESOLVED', 'DISMISSED'] = Field(..., description="Target status", example="UNDER_REVIEW")
    status_update: Optional[str] = Field(None, description="Moderator notes or progress details", example="The report is currently being reviewed.")

class StatusUpdateResponse(BaseModel):
    message: str = "Report status updated successfully"
    case_code: str
    status: str
    status_update: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    case_code: str
    category: str
    description: str
    evidence_url: Optional[str] = None
    status: str
    status_update: Optional[str] = None
    created_at: str
