from pathlib import Path

from core.config import Config
from core.scoring import explain_cv_recommendation


def get_recommended_cv_content(jd_text: str, config: Config) -> tuple[str, str, list[str]]:
    """
    Returns (cv_slug, cv_content, matched_keywords).
    Reads the CV file from disk.
    """
    slug, matched = explain_cv_recommendation(jd_text, config)
    path = config.get_cv_path(slug)

    try:
        content = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        content = f"[CV file not found: {path}]"

    return slug, content, matched


def get_cv_content(slug: str, config: Config) -> str:
    """Read a specific CV variant by slug."""
    path = config.get_cv_path(slug)
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"[CV file not found: {path}]"
