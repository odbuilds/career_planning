from core.config import Config


def score_job(jd_text: str, config: Config) -> float:
    """
    Score a job description 0.0–10.0 against the user profile.
    Higher = better match. Weights configured in profile.yaml.
    """
    text = jd_text.lower()
    score = config.base_score

    for signal in config.positive_signals:
        if signal["text"].lower() in text:
            score += signal["weight"]

    for flag in config.jd_red_flags:
        if flag["text"].lower() in text:
            score -= flag["weight"]

    return round(max(0.0, min(10.0, score)), 1)


def recommend_cv(jd_text: str, config: Config) -> str:
    """
    Return the slug of the best-matching CV variant for this JD.
    Scores each non-fallback variant by keyword hits; returns the highest
    scorer that meets its threshold. Falls back to 'cv_cx' if none qualify.
    """
    slug, _ = explain_cv_recommendation(jd_text, config)
    return slug


def explain_cv_recommendation(jd_text: str, config: Config) -> tuple[str, list[str]]:
    """
    Returns (recommended_cv_slug, list_of_matched_keywords).
    Iterates all non-fallback CV variants, scores by keyword hits,
    returns the best match above threshold.
    """
    text = jd_text.lower()
    best_slug = "cv_cx"
    best_hits = 0
    best_matched: list[str] = []

    for slug, variant in config.cv_variants.items():
        if slug == "cv_cx":
            continue  # fallback — only used if nothing else matches

        keywords = [kw.lower() for kw in variant.get("keywords", [])]
        strong = {kw.lower() for kw in variant.get("strong_keywords", [])}
        threshold = variant.get("threshold", config.cv_threshold)

        matched = []
        hits = 0
        for kw in keywords:
            if kw in text:
                matched.append(kw)
                hits += 2 if kw in strong else 1

        if hits >= threshold and hits > best_hits:
            best_hits = hits
            best_slug = slug
            best_matched = matched

    return best_slug, best_matched
