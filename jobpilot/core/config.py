import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


class Config:
    """Typed wrapper around profile.yaml + .env values."""

    def __init__(self, data: dict, base_dir: Path):
        self._data = data
        self._base_dir = base_dir

        # Identity
        self.name: str = data["name"]
        self.email: str = data.get("email", "")
        self.positioning: str = data.get("positioning", "")

        # Roles
        self.target_roles: list[str] = data.get("target_roles", [])
        self.fallback_roles: list[str] = data.get("fallback_roles", [])

        # Salary
        salary = data.get("salary", {})
        self.uk_gbp_min: int = salary.get("uk_gbp_min", 90000)
        self.serbia_eur_monthly_min: int = salary.get("serbia_eur_monthly_min", 5500)

        # Locations
        self.preferred_locations: list[str] = data.get("preferred_locations", [])

        # CV variants — resolve paths relative to base_dir
        self.cv_variants: dict[str, dict] = {}
        for slug, variant in data.get("cv_variants", {}).items():
            self.cv_variants[slug] = {
                **variant,
                "path": str((base_dir / variant["path"]).resolve()),
            }
        self.cv_threshold: int = data.get("cv_threshold", 2)

        # Context files
        context = data.get("context", {})
        self.projects_md_path: str = str(
            (base_dir / context.get("projects_md", "../context/projects.md")).resolve()
        )
        self.coverletter_snippets_md_path: str = str(
            (base_dir / context.get("coverletter_snippets_md", "../context/coverletter_snippets.md")).resolve()
        )

        # Scoring
        scoring = data.get("scoring", {})
        self.base_score: float = scoring.get("base_score", 5.0)
        self.positive_signals: list[dict] = scoring.get("positive_signals", [])
        self.title_red_flags: list[str] = scoring.get("title_red_flags", [])
        self.jd_red_flags: list[dict] = scoring.get("jd_red_flags", [])
        self.llm_scoring_enabled: bool = scoring.get("llm_enabled", False)
        self.llm_scoring_threshold: float = scoring.get("llm_threshold", 6.0)
        self.llm_scoring_model: str = scoring.get("llm_model", "moonshotai/kimi-k2.5")
        self.generation_model: str = scoring.get("generation_model", "moonshotai/kimi-k2.5")
        self.pipeline_scoring_enabled: bool = scoring.get("pipeline_enabled", False)
        self.pipeline_scoring_model: str = scoring.get("pipeline_model", "google/gemma-4-26b-a4b-it")
        self.critic_model: str = scoring.get("critic_model", self.generation_model)
        self.rewrite_model: str = scoring.get("rewrite_model", self.generation_model)

        # Discovery
        discovery = data.get("discovery", {})
        self.keyword_searches: list[str] = discovery.get("keyword_searches", ["AI engineer"])
        self.title_positive_filter: list[str] = discovery.get("title_positive_filter", [])
        self.default_days_old: int = discovery.get("default_days_old", 7)
        self.target_countries: list[dict] = discovery.get("target_countries", [])
        # Normalise search_locations — accept both plain strings and dicts
        raw_locations = discovery.get("search_locations", [])
        self.search_locations: list[dict] = [
            loc if isinstance(loc, dict) else {"location": loc}
            for loc in raw_locations
        ]
        self.sources: list[dict] = discovery.get("sources", [])

        # Watched companies (Greenhouse/Lever/Ashby)
        self.watched_companies: list[dict] = data.get("watched_companies", [])

        # Workday job boards — companies using Workday ATS with public CXS API
        self.workday_companies: list[dict] = data.get("workday_companies", [])

        # Pinpoint HQ job boards — companies using Pinpoint ATS
        self.pinpoint_companies: list[dict] = data.get("pinpoint_companies", [])

        # Playwright-scraped career pages (JS-rendered / bot-protected)
        self.playwright_companies: list[dict] = data.get("playwright_companies", [])

        # Company watchlist — consulting/services firms to track via LinkedIn
        self.company_watchlist: list[dict] = data.get("company_watchlist", [])

        # DB path — .env overrides profile.yaml
        self.db_path: str = os.environ.get(
            "DB_PATH",
            str((base_dir / data.get("db_path", "jobpilot.db")).resolve()),
        )

        # API keys from environment
        self.anthropic_api_key: str = os.environ.get("ANTHROPIC_API_KEY", "")
        self.openrouter_api_key: str = os.environ.get("OPENROUTER_API_KEY", "")
        self.serper_api_key: str = os.environ.get("SERPER_API_KEY", "")
        self.adzuna_app_id: str = os.environ.get("ADZUNA_APP_ID", "")
        self.adzuna_api_key: str = os.environ.get("ADZUNA_API_KEY", "")
        self.reed_api_key: str = os.environ.get("REED_API_KEY", "")
        self.foorilla_api_key: str = os.environ.get("FOORILLA_API_KEY", "")
        self.foorilla_session: str = os.environ.get("FOORILLA_SESSION", "")

    def get_enabled_sources(self) -> list[dict]:
        return [s for s in self.sources if s.get("enabled", False)]

    def get_cv_path(self, slug: str) -> str:
        return self.cv_variants.get(slug, self.cv_variants.get("cv_cx", {})).get(
            "path", ""
        )

    def get_cv_display_name(self, slug: str) -> str:
        return self.cv_variants.get(slug, {}).get("display_name", slug)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)


_config_cache: Config | None = None


def load_config(profile_path: str | None = None) -> Config:
    """Load and cache config. Subsequent calls return the cached instance."""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    # Resolve profile.yaml path
    if profile_path is None:
        here = Path(__file__).parent.parent  # jobpilot/
        profile_path = here / "profile.yaml"
    else:
        profile_path = Path(profile_path)

    load_dotenv(profile_path.parent / ".env")

    with open(profile_path) as f:
        data = yaml.safe_load(f)

    _config_cache = Config(data, profile_path.parent)
    return _config_cache


def reload_config(profile_path: str | None = None) -> Config:
    """Force reload — use when profile.yaml has been edited."""
    global _config_cache
    _config_cache = None
    return load_config(profile_path)
