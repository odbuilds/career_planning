"""
TrueUp source (trueup.io/ai) — AI/tech hiring tracker.
Currently disabled in profile.yaml (returns 403 on direct fetch).
TODO: investigate whether a different endpoint or auth is needed.
"""


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    raise NotImplementedError(
        "TrueUp returns 403 on direct fetch. "
        "Enable this source once a working endpoint is identified."
    )
