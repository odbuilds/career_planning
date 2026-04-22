import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ── Connection ────────────────────────────────────────────────────────────────

def get_db_path() -> str:
    """Returns DB path from config (avoids circular import — call after config loaded)."""
    from core.config import load_config
    return load_config().db_path


@contextmanager
def get_conn(db_path: str | None = None):
    """Context manager yielding a WAL-mode SQLite connection with row_factory set."""
    path = db_path or get_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Schema ────────────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    company         TEXT    NOT NULL,
    role            TEXT    NOT NULL,
    url             TEXT    DEFAULT '',
    jd_text         TEXT    DEFAULT '',
    source          TEXT    DEFAULT 'manual',
    score           REAL    DEFAULT 0,
    recommended_cv  TEXT    DEFAULT 'cv_draft',
    status          TEXT    DEFAULT 'discovered',
    created_at      TEXT    DEFAULT (datetime('now')),
    applied_at      TEXT    DEFAULT '',
    notes           TEXT    DEFAULT '',
    location        TEXT    DEFAULT ''
);

CREATE TABLE IF NOT EXISTS materials (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id          INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    type            TEXT    NOT NULL,
    content         TEXT    DEFAULT '',
    file_path       TEXT    DEFAULT '',
    generated_at    TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS interviews (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id          INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    date            TEXT    DEFAULT '',
    type            TEXT    DEFAULT '',
    interviewer     TEXT    DEFAULT '',
    notes           TEXT    DEFAULT '',
    created_at      TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS emails (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id              INTEGER REFERENCES jobs(id) ON DELETE SET NULL,
    received_at         TEXT    DEFAULT '',
    subject             TEXT    DEFAULT '',
    sender              TEXT    DEFAULT '',
    classification      TEXT    DEFAULT '',
    body                TEXT    DEFAULT '',
    gmail_message_id    TEXT    UNIQUE DEFAULT ''
);

CREATE TABLE IF NOT EXISTS meta (
    key     TEXT PRIMARY KEY,
    value   TEXT DEFAULT ''
);
"""


def init_db(db_path: str | None = None) -> None:
    """Create all tables if they don't exist. Safe to call on every startup."""
    path = db_path or get_db_path()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with get_conn(path) as conn:
        conn.executescript(SCHEMA)
        # Migrations — safe to run on every startup
        existing = {row[1] for row in conn.execute("PRAGMA table_info(jobs)")}
        if "location" not in existing:
            conn.execute("ALTER TABLE jobs ADD COLUMN location TEXT DEFAULT ''")


# ── Jobs ──────────────────────────────────────────────────────────────────────

def upsert_job(job: dict, db_path: str | None = None) -> int:
    """
    Insert a new job or skip if (company, role, url) already exists.
    Returns the job id (existing or new).
    """
    with get_conn(db_path) as conn:
        # Check for existing by URL first, then by (company, role) tuple
        if job.get("url"):
            row = conn.execute(
                "SELECT id FROM jobs WHERE url = ?", (job["url"],)
            ).fetchone()
            if row:
                return row["id"]

        company = (job.get("company") or "").strip().lower()
        role = (job.get("role") or "").strip().lower()
        if company and role:
            row = conn.execute(
                "SELECT id FROM jobs WHERE lower(company) = ? AND lower(role) = ?",
                (company, role),
            ).fetchone()
            if row:
                return row["id"]

        source = job.get("source", "manual")
        status = job.get("status", "discovered")
        if source == "linkedin" and not job.get("location"):
            status = "rejected"

        cursor = conn.execute(
            """
            INSERT INTO jobs (company, role, url, jd_text, source, score,
                              recommended_cv, status, notes, location)
            VALUES (:company, :role, :url, :jd_text, :source, :score,
                    :recommended_cv, :status, :notes, :location)
            """,
            {
                "company":        job.get("company", ""),
                "role":           job.get("role", ""),
                "url":            job.get("url", ""),
                "jd_text":        job.get("jd_text", ""),
                "source":         source,
                "score":          job.get("score", 0.0),
                "recommended_cv": job.get("recommended_cv", "cv_draft"),
                "status":         status,
                "location":       job.get("location", ""),
                "notes":          job.get("notes", ""),
            },
        )
        return cursor.lastrowid


def get_jobs(
    status: list[str] | None = None,
    source: list[str] | None = None,
    min_score: float = 0.0,
    search: str = "",
    db_path: str | None = None,
) -> list[dict]:
    """Flexible job listing with optional filters. Returns list of dicts."""
    clauses = ["score >= :min_score"]
    params: dict[str, Any] = {"min_score": min_score}

    if status:
        placeholders = ",".join(f":s{i}" for i in range(len(status)))
        clauses.append(f"status IN ({placeholders})")
        for i, s in enumerate(status):
            params[f"s{i}"] = s

    if source:
        placeholders = ",".join(f":src{i}" for i in range(len(source)))
        clauses.append(f"source IN ({placeholders})")
        for i, s in enumerate(source):
            params[f"src{i}"] = s

    if search:
        clauses.append(
            "(lower(company) LIKE :search OR lower(role) LIKE :search)"
        )
        params["search"] = f"%{search.lower()}%"

    where = " AND ".join(clauses)
    sql = f"SELECT * FROM jobs WHERE {where} ORDER BY score DESC, created_at DESC"

    with get_conn(db_path) as conn:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]


def get_job(job_id: int, db_path: str | None = None) -> dict | None:
    with get_conn(db_path) as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        return dict(row) if row else None


def update_job(job_id: int, updates: dict, db_path: str | None = None) -> None:
    """Partial update — only keys present in updates are written."""
    allowed = {
        "company", "role", "url", "jd_text", "source", "score",
        "recommended_cv", "status", "applied_at", "notes",
    }
    filtered = {k: v for k, v in updates.items() if k in allowed}
    if not filtered:
        return
    set_clause = ", ".join(f"{k} = :{k}" for k in filtered)
    filtered["_id"] = job_id
    with get_conn(db_path) as conn:
        conn.execute(f"UPDATE jobs SET {set_clause} WHERE id = :_id", filtered)


def get_pipeline_counts(db_path: str | None = None) -> dict[str, int]:
    """Returns {status: count} for all stages that have at least one job."""
    with get_conn(db_path) as conn:
        rows = conn.execute(
            "SELECT status, COUNT(*) as cnt FROM jobs GROUP BY status"
        ).fetchall()
        return {r["status"]: r["cnt"] for r in rows}


def search_jobs_by_company(company: str, db_path: str | None = None) -> dict | None:
    """Fuzzy match on company name — used by email ingest to link emails to jobs."""
    with get_conn(db_path) as conn:
        row = conn.execute(
            """
            SELECT * FROM jobs
            WHERE lower(company) LIKE :company
              AND status NOT IN ('rejected', 'withdrawn',
                                'passed-application', 'passed-screening',
                                'passed-interview', 'passed-final')
            ORDER BY created_at DESC
            LIMIT 1
            """,
            {"company": f"%{company.lower()}%"},
        ).fetchone()
        return dict(row) if row else None


# ── Materials ─────────────────────────────────────────────────────────────────

def save_material(
    job_id: int,
    type_: str,
    content: str,
    file_path: str = "",
    db_path: str | None = None,
) -> int:
    with get_conn(db_path) as conn:
        # Replace existing material of the same type for this job
        conn.execute(
            "DELETE FROM materials WHERE job_id = ? AND type = ?", (job_id, type_)
        )
        cursor = conn.execute(
            """
            INSERT INTO materials (job_id, type, content, file_path)
            VALUES (?, ?, ?, ?)
            """,
            (job_id, type_, content, file_path),
        )
        return cursor.lastrowid


def get_material(job_id: int, type_: str, db_path: str | None = None) -> dict | None:
    with get_conn(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM materials WHERE job_id = ? AND type = ?",
            (job_id, type_),
        ).fetchone()
        return dict(row) if row else None


def get_materials(job_id: int, db_path: str | None = None) -> list[dict]:
    with get_conn(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM materials WHERE job_id = ? ORDER BY generated_at DESC",
            (job_id,),
        ).fetchall()
        return [dict(r) for r in rows]


# ── Interviews ────────────────────────────────────────────────────────────────

def add_interview(
    job_id: int,
    date: str,
    type_: str,
    interviewer: str = "",
    notes: str = "",
    db_path: str | None = None,
) -> int:
    with get_conn(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO interviews (job_id, date, type, interviewer, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (job_id, date, type_, interviewer, notes),
        )
        return cursor.lastrowid


def get_interviews(job_id: int, db_path: str | None = None) -> list[dict]:
    with get_conn(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM interviews WHERE job_id = ? ORDER BY date DESC",
            (job_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def update_interview(
    interview_id: int, updates: dict, db_path: str | None = None
) -> None:
    allowed = {"date", "type", "interviewer", "notes"}
    filtered = {k: v for k, v in updates.items() if k in allowed}
    if not filtered:
        return
    set_clause = ", ".join(f"{k} = :{k}" for k in filtered)
    filtered["_id"] = interview_id
    with get_conn(db_path) as conn:
        conn.execute(
            f"UPDATE interviews SET {set_clause} WHERE id = :_id", filtered
        )


def delete_interview(interview_id: int, db_path: str | None = None) -> None:
    with get_conn(db_path) as conn:
        conn.execute("DELETE FROM interviews WHERE id = ?", (interview_id,))


# ── Emails ────────────────────────────────────────────────────────────────────

def add_email(
    job_id: int | None,
    received_at: str,
    subject: str,
    sender: str,
    classification: str,
    body: str,
    gmail_message_id: str = "",
    db_path: str | None = None,
) -> int | None:
    """
    Insert email. Returns new id, or None if gmail_message_id already exists.
    """
    with get_conn(db_path) as conn:
        if gmail_message_id:
            exists = conn.execute(
                "SELECT id FROM emails WHERE gmail_message_id = ?",
                (gmail_message_id,),
            ).fetchone()
            if exists:
                return None

        cursor = conn.execute(
            """
            INSERT INTO emails
                (job_id, received_at, subject, sender, classification, body, gmail_message_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (job_id, received_at, subject, sender, classification, body, gmail_message_id),
        )
        return cursor.lastrowid


def get_emails(job_id: int, db_path: str | None = None) -> list[dict]:
    with get_conn(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM emails WHERE job_id = ? ORDER BY received_at DESC",
            (job_id,),
        ).fetchall()
        return [dict(r) for r in rows]


# ── Meta (key/value store) ────────────────────────────────────────────────────

def get_meta(key: str, db_path: str | None = None) -> str | None:
    with get_conn(db_path) as conn:
        row = conn.execute(
            "SELECT value FROM meta WHERE key = ?", (key,)
        ).fetchone()
        return row["value"] if row else None


def set_meta(key: str, value: str, db_path: str | None = None) -> None:
    with get_conn(db_path) as conn:
        conn.execute(
            "INSERT INTO meta (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )


def get_last_email_check() -> str | None:
    return get_meta("last_email_check_at")


def set_last_email_check(ts: str | None = None) -> None:
    if ts is None:
        ts = datetime.now(timezone.utc).isoformat()
    set_meta("last_email_check_at", ts)
