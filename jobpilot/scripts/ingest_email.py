#!/usr/bin/env python3
"""
Email ingest CLI — called by Claude during a "check job emails" session.

Usage:
    python scripts/ingest_email.py \
        --gmail-id "abc123" \
        --received-at "2026-04-05T10:30:00" \
        --subject "Interview Invitation" \
        --sender "hr@acme.com" \
        --classification "interview_invite" \
        --body "We'd like to invite you..." \
        [--job-id 4] \
        [--status-update "interview"] \
        [--update-last-check]

    python scripts/ingest_email.py --update-last-check
        (updates last_email_check_at to now without inserting an email)

Prints JSON result to stdout.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path so core imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load_config
from core import database as db


def main():
    parser = argparse.ArgumentParser(description="Ingest a classified job email into JobPilot DB")

    parser.add_argument("--gmail-id",        default="", help="Gmail message ID (for dedup)")
    parser.add_argument("--received-at",     default="", help="ISO timestamp")
    parser.add_argument("--subject",         default="", help="Email subject")
    parser.add_argument("--sender",          default="", help="Sender email address")
    parser.add_argument("--classification",  default="general_info", help="Email classification")
    parser.add_argument("--body",            default="", help="Email body (plain text)")
    parser.add_argument("--job-id",          type=int, default=None, help="Job ID to link to")
    parser.add_argument("--company",         default="", help="Company name (used to auto-match job if --job-id not given)")
    parser.add_argument("--status-update",   default="", help="New status to set on the linked job")
    parser.add_argument("--update-last-check", action="store_true", help="Update last_email_check_at to now")

    args = parser.parse_args()

    load_config()
    db.init_db()

    # Auto-match job by company name if job_id not provided
    job_id = args.job_id
    if job_id is None and args.company:
        job = db.search_jobs_by_company(args.company)
        if job:
            job_id = job["id"]

    result = {"ok": True}

    # Insert email (skip if --update-last-check only)
    if not args.update_last_check or args.gmail_id:
        email_id = db.add_email(
            job_id=job_id,
            received_at=args.received_at,
            subject=args.subject,
            sender=args.sender,
            classification=args.classification,
            body=args.body,
            gmail_message_id=args.gmail_id,
        )
        if email_id is None:
            result = {"ok": False, "reason": "duplicate", "gmail_id": args.gmail_id}
            print(json.dumps(result))
            return
        result["email_id"] = email_id
        result["job_id"] = job_id

    # Update job status if requested
    if args.status_update and job_id:
        db.update_job(job_id, {"status": args.status_update})
        result["status_updated"] = args.status_update

    # Update last check timestamp
    if args.update_last_check:
        db.set_last_email_check()
        result["last_check_updated"] = True

    print(json.dumps(result))


if __name__ == "__main__":
    main()
