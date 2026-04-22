"""
PDF generation for cover letters and CVs.

Requires: pip install weasyprint markdown
On Ubuntu/WSL2, also: apt install libpango-1.0-0 libharfbuzz0b libfontconfig1
"""
import html as _html
from datetime import date


def _paragraphs_to_html(text: str) -> str:
    """Convert plain-text paragraphs to HTML <p> blocks."""
    paragraphs = text.strip().split("\n\n")
    parts = []
    for p in paragraphs:
        escaped = _html.escape(p.replace("\n", " "))
        parts.append(f"<p>{escaped}</p>")
    return "\n".join(parts)


def cover_letter_to_pdf(
    text: str,
    candidate_name: str,
    company: str,
    role: str,
) -> bytes:
    """
    Convert a plain-text cover letter to a PDF.
    Returns PDF bytes.
    Raises ImportError if weasyprint is not installed.
    """
    from weasyprint import HTML  # deferred — optional dep

    date_str = date.today().strftime("%d %B %Y")
    body_html = _paragraphs_to_html(text)
    safe_name = _html.escape(candidate_name)
    safe_company = _html.escape(company)
    safe_role = _html.escape(role)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: A4;
    margin: 2.5cm 2.8cm;
  }}
  body {{
    font-family: Georgia, "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.65;
    color: #111111;
  }}
  .letterhead {{
    margin-bottom: 2em;
    border-bottom: 1px solid #cccccc;
    padding-bottom: 0.8em;
  }}
  .candidate-name {{
    font-size: 14pt;
    font-weight: bold;
    letter-spacing: 0.02em;
    margin-bottom: 0.25em;
  }}
  .letter-meta {{
    color: #555555;
    font-size: 9.5pt;
  }}
  p {{
    margin: 0 0 0.85em 0;
    text-align: justify;
  }}
</style>
</head>
<body>
<div class="letterhead">
  <div class="candidate-name">{safe_name}</div>
  <div class="letter-meta">{date_str} &nbsp;&middot;&nbsp; {safe_role} at {safe_company}</div>
</div>
{body_html}
</body>
</html>"""

    return HTML(string=html).write_pdf()


def cv_to_pdf(cv_markdown: str, candidate_name: str) -> bytes:
    """
    Convert CV markdown to a PDF.
    Returns PDF bytes.
    Raises ImportError if weasyprint or markdown are not installed.
    """
    import markdown as md  # deferred — optional dep
    from weasyprint import HTML  # deferred — optional dep

    html_body = md.markdown(
        cv_markdown,
        extensions=["extra", "nl2br"],
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: A4;
    margin: 1.8cm 2.2cm;
  }}
  body {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #111111;
  }}
  h1 {{
    font-size: 18pt;
    margin: 0 0 0.15em 0;
    color: #1a1a2e;
    letter-spacing: -0.01em;
  }}
  h2 {{
    font-size: 10.5pt;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #333333;
    border-bottom: 1px solid #cccccc;
    padding-bottom: 0.2em;
    margin: 1.1em 0 0.45em 0;
  }}
  h3 {{
    font-size: 10pt;
    margin: 0.7em 0 0.1em 0;
    color: #1a1a2e;
  }}
  ul {{
    margin: 0.15em 0 0.5em 0;
    padding-left: 1.2em;
  }}
  li {{
    margin-bottom: 0.15em;
  }}
  p {{
    margin: 0.15em 0 0.4em 0;
  }}
  a {{
    color: #1a1a2e;
    text-decoration: none;
  }}
  strong {{
    color: #1a1a2e;
  }}
  hr {{
    border: none;
    border-top: 1px solid #dddddd;
    margin: 0.8em 0;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    return HTML(string=html).write_pdf()
