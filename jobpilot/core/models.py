from dataclasses import dataclass, field


@dataclass
class Job:
    company: str
    role: str
    url: str = ""
    jd_text: str = ""
    source: str = "manual"
    score: float = 0.0
    recommended_cv: str = "cv_draft"
    status: str = "discovered"
    created_at: str = ""
    applied_at: str = ""
    notes: str = ""
    id: int = None


@dataclass
class Material:
    job_id: int
    type: str          # 'cv' | 'cover_letter'
    content: str
    file_path: str = ""
    generated_at: str = ""
    id: int = None


@dataclass
class Interview:
    job_id: int
    date: str
    type: str          # 'phone' | 'technical' | 'hm' | 'final' | 'other'
    interviewer: str = ""
    notes: str = ""
    created_at: str = ""
    id: int = None


@dataclass
class Email:
    job_id: int        # nullable — pass None if company not matched
    received_at: str
    subject: str
    sender: str
    classification: str
    body: str
    gmail_message_id: str = ""
    id: int = None


PIPELINE_STAGES = [
    "discovered",
    "applied",
    "screening",
    "interview",
    "final",
    "offer",
    "rejected",
    "passed-application",
    "passed-screening",
    "passed-interview",
    "passed-final",
    "withdrawn",
]

ACTIVE_STAGES = ["applied", "screening", "interview", "final"]
CLOSED_STAGES = [
    "offer", "rejected",
    "passed-application", "passed-screening", "passed-interview", "passed-final",
    "withdrawn",
]

INTERVIEW_TYPES = ["Phone Screen", "Technical", "Hiring Manager", "Final", "Other"]

EMAIL_CLASSIFICATIONS = [
    "application_acknowledgement",
    "recruiter_screen_request",
    "interview_invite",
    "rejection",
    "offer",
    "general_info",
    "action_needed",
]
