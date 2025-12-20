#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Save a Wikipedia page (default: fr) as Markdown containing "Headings + Body".
Images, tables, and footnotes are removed.
"""

import argparse
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


API_ENDPOINT = "https://{lang}.wikipedia.org/w/api.php"
DEFAULT_UA = "https://github.com/sekika/langreader/blob/main/docs/scripts/wiki_to_md.py"

# Mappings for language codes to full names for the description
LANG_MAP = {
    "fr": "French",
    "en": "English",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "ja": "Japanese",
    "zh": "Chinese",
    "ru": "Russian",
    "nl": "Dutch",
    "pl": "Polish",
}

# Headings to skip (footer sections like References, External links, etc.)
# Covers French, English, and German common terms.
SKIP_HEADINGS = {
    # French
    "notes et references",
    "notes",
    "references",
    "annexes",
    "bibliographie",
    "articles connexes",
    "liens externes",
    "voir aussi",
    # English
    "external links",
    "further reading",
    "works cited",
    "sources",
    "see also",
    # German
    "literatur",
    "weblinks",
    "einzelnachweise",
    "siehe auch",
    "anmerkungen",
    "quellen",
}

# Common UI fragments like [ edit ]
UI_JUNK_RE = re.compile(r"\[\s*modifier\s*\]|\[\s*edit\s*\]|\[\s*bearbeiten\s*\]", re.IGNORECASE)

# Regex to handle spacing around punctuation (mainly for French typography cleanup)
PUNCT_NO_SPACE_BEFORE_RE = re.compile(r"\s+([,.;:!?])")
CLOSE_PAREN_NO_SPACE_BEFORE_RE = re.compile(r"\s+([\)\]\}])")
OPEN_PAREN_NO_SPACE_AFTER_RE = re.compile(r"([\(\[\{])\s+")
APOSTROPHE_NO_SPACE_AFTER_RE = re.compile(r"([dDlLjJcCmMnNsStTqQuU]')\s+")  # elision


def fix_french_spacing(text: str) -> str:
    """
    Clean up spacing for punctuation.
    """
    if not text:
        return ""

    # Convert NBSP to normal space
    text = text.replace("\xa0", " ").replace("\u202f", " ")

    # Remove extra spaces (order matters)
    text = APOSTROPHE_NO_SPACE_AFTER_RE.sub(r"\1", text)          # d' élan -> d'élan
    text = OPEN_PAREN_NO_SPACE_AFTER_RE.sub(r"\1", text)         # ( vinaigre -> (vinaigre
    text = CLOSE_PAREN_NO_SPACE_BEFORE_RE.sub(r"\1", text)       # lactique ) -> lactique)
    text = PUNCT_NO_SPACE_BEFORE_RE.sub(r"\1", text)             # renne , -> renne,

    # Collapse multiple spaces (keep newlines for paragraph separation)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()


def norm_heading(s: str) -> str:
    """
    Normalize heading text for comparison (lowercase, remove accents/punctuation).
    """
    if not isinstance(s, str):
        s = ""
    s = (s or "").strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace("’", "'")
    s = re.sub(r"\s+", " ", s)
    return s


def api_get(params, lang="fr", user_agent=DEFAULT_UA):
    """
    General wrapper for Wikipedia API requests.
    """
    url = API_ENDPOINT.format(lang=lang)
    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json; charset=utf-8",
        "Accept-Language": f"{lang},en;q=0.8",
    }
    r = requests.get(url, params=params, headers=headers, timeout=45)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(f"Wikipedia API error: {data['error']}")
    return data


def get_page_metadata(title: str, lang: str, user_agent: str):
    """
    Retrieve page metadata: canonical title, URL, and last revision timestamp.
    """
    data = api_get(
        {
            "action": "query",
            "titles": title,
            "prop": "info|revisions",
            "inprop": "url",
            "rvprop": "timestamp",
            "redirects": 1,
            "format": "json",
            "formatversion": 2,
        },
        lang=lang,
        user_agent=user_agent,
    )
    
    if not data.get("query") or not data["query"].get("pages"):
        raise ValueError(f"Page not found: {title}")

    page = data["query"]["pages"][0]
    if "missing" in page:
        raise ValueError(f"Page does not exist: {title}")

    canonical_title = page.get("title", title)
    full_url = page.get("fullurl", "")
    
    # Get timestamp from the last revision
    last_modified = ""
    if "revisions" in page and len(page["revisions"]) > 0:
        ts = page["revisions"][0].get("timestamp", "")
        # Convert ISO 8601 string to a cleaner format if possible
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                last_modified = dt.strftime("%Y-%m-%d")
            except ValueError:
                last_modified = ts

    return canonical_title, full_url, last_modified


def get_sections(title: str, lang: str, user_agent: str):
    """
    Get the list of sections (TOC) to handle nesting.
    """
    data = api_get(
        {
            "action": "parse",
            "page": title,
            "prop": "sections",
            "redirects": 1,
            "format": "json",
            "formatversion": 2,
        },
        lang=lang,
        user_agent=user_agent,
    )
    return data["parse"].get("sections", [])


def get_section_html(title: str, section: int, lang: str, user_agent: str) -> str:
    """
    Fetch HTML for a specific section.
    section: 0 is the lead paragraph (intro).
    """
    data = api_get(
        {
            "action": "parse",
            "page": title,
            "prop": "text",
            "section": section,
            "redirects": 1,
            "format": "json",
            "formatversion": 2,
        },
        lang=lang,
        user_agent=user_agent,
    )
    return data["parse"].get("text") or ""


def _soup(html: str) -> BeautifulSoup:
    """
    Create a BeautifulSoup object using lxml if available, else html.parser.
    """
    try:
        return BeautifulSoup(html, "lxml")
    except Exception:
        return BeautifulSoup(html, "html.parser")


def html_to_plain_text(html: str) -> str:
    """
    Convert HTML to plain text, stripping out non-content elements.
    """
    if not html:
        return ""

    soup = _soup(html)

    # Remove unwanted elements
    for sel in [
        "table",
        ".infobox",
        ".infobox_v2",
        ".navbox",
        ".vertical-navbox",
        ".metadata",
        ".mbox",
        ".bandeau-portail",
        ".portal",
        ".sistersitebox",
        ".toc",
        ".mw-editsection",
        ".mw-editsection-bracket",

        # References and footnotes
        ".mw-references-wrap",
        ".reflist",
        ".references",
        "ol.references",
        "sup.reference",
        "span.reference",

        # Cite errors, ref tags
        "ref",
        ".mw-ext-cite-error",
        ".error",

        ".noprint",
        ".shortdescription",
        ".hatnote",
        ".dablink",
        ".thumb",
        ".thumbinner",
        "figure",
        "audio",
        "video",
        "noscript",
        ".gallery",
    ]:
        for node in soup.select(sel):
            node.decompose()

    for node in soup(["script", "style"]):
        node.decompose()

    root = soup.select_one(".mw-parser-output") or soup

    blocks = []

    # Extract text primarily from p, ul, ol, dl, blockquote
    for el in root.find_all(["p", "ul", "ol", "dl", "blockquote"], recursive=True):
        if el.name in ("ul", "ol"):
            items = []
            for li in el.find_all("li", recursive=False):
                t = li.get_text(" ", strip=True)
                t = UI_JUNK_RE.sub("", t).strip()
                t = fix_french_spacing(t)
                if t:
                    items.append(f"- {t}")
            if items:
                # Treat list block as a paragraph
                blocks.append("\n".join(items))
            continue

        text = el.get_text(" ", strip=True)
        text = UI_JUNK_RE.sub("", text).strip()
        text = fix_french_spacing(text)
        if text:
            blocks.append(text)

    # Separate blocks with double newlines
    out = "\n\n".join(blocks)

    # Clean up excessive newlines
    out = re.sub(r"\n{3,}", "\n\n", out).strip()
    return out


def sanitize_filename(s: str) -> str:
    s = (s or "").strip().replace(" ", "_")
    s = re.sub(r"[^\w\-.()]+", "_", s, flags=re.UNICODE)
    return s or "wikipedia_page"


def build_markdown(input_title: str, lang: str, user_agent: str, intro_only: bool = False) -> str:
    """
    Orchestrates the metadata fetching and content generation.
    Returns the full Markdown string with frontmatter.
    """
    
    # 1. Fetch Metadata (Canonical Title, URL, Date)
    title, url, last_modified = get_page_metadata(input_title, lang, user_agent)
    
    # 2. Prepare Frontmatter
    lang_name = LANG_MAP.get(lang, lang.upper())
    desc = (
        f"{lang_name} reading practice. "
        f"Based on the {lang_name} Wikipedia article [{title}]({url}) "
        f"(as of {last_modified}). "
        f"Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)."
    )
    
    out = []
    out.append("---")
    out.append(f"description: {desc}")
    out.append("---\n")
    
    # 3. Add Title
    out.append(f"# {title}\n")

    # 4. Fetch Intro (Lead section)
    intro_html = get_section_html(title, section=0, lang=lang, user_agent=user_agent)
    intro_txt = html_to_plain_text(intro_html)
    if intro_txt:
        out.append(intro_txt + "\n")

    if intro_only:
        return "\n".join(out).strip() + "\n"

    # 5. Fetch Sections
    sections = get_sections(title, lang=lang, user_agent=user_agent)

    # Identify sections that have children (to avoid duplicating parent content if empty)
    has_child = set()
    for i, s in enumerate(sections):
        lvl = int(s.get("level", 2))
        idx = int(s.get("index"))
        if i + 1 < len(sections):
            next_lvl = int(sections[i + 1].get("level", 2))
            if next_lvl > lvl:
                has_child.add(idx)

    # Skip sections based on SKIP_HEADINGS
    skip_until_level = None

    for s in sections:
        level = int(s.get("level", 2))
        line = (s.get("line") or "").strip()
        index = int(s.get("index"))

        if not line:
            continue

        if skip_until_level is not None:
            if level > skip_until_level:
                continue
            skip_until_level = None

        if norm_heading(line) in SKIP_HEADINGS:
            skip_until_level = level
            continue

        md_level = min(6, level)
        out.append(f"{'#' * md_level} {line}\n")

        # Skip text for parents that have children (avoids intro duplication sometimes)
        if index in has_child:
            continue

        sec_html = get_section_html(title, section=index, lang=lang, user_agent=user_agent)
        sec_txt = html_to_plain_text(sec_html)
        if sec_txt:
            out.append(sec_txt + "\n")

    return "\n".join(out).strip() + "\n"


def main():
    ap = argparse.ArgumentParser(
        description="Save Wikipedia page as Markdown (Headings + Body only). "
                    "Images, tables, and footnotes are stripped. "
                    "Includes YAML frontmatter with license info."
    )
    ap.add_argument("title", help="Wikipedia page title (e.g., Alsace)")
    ap.add_argument("-o", "--output", help="Output MD path (default: Title.md)")
    ap.add_argument("--lang", default="fr", help="Language code (default: fr)")
    ap.add_argument("--intro-only", action="store_true", help="Output introduction only")
    ap.add_argument("--user-agent", default=DEFAULT_UA, help="HTTP User-Agent")
    args = ap.parse_args()

    try:
        # Fetch data and build markdown
        # Note: We pass args.title, but the function will query API for the canonical title
        md = build_markdown(
            args.title,
            lang=args.lang,
            user_agent=args.user_agent,
            intro_only=args.intro_only,
        )

        # Determine output filename
        # We need to re-fetch the canonical title for the filename if output is not specified
        # but build_markdown returns a string.
        # To keep it simple, if no output is specified, we rely on the first line or args.title.
        # However, to be precise, let's extract the title from the metadata inside build_markdown?
        # A simpler way: just use the sanitized arg title or parse the # Heading from md.
        
        if args.output:
            out_path = Path(args.output)
        else:
            # Try to extract the canonical title from the generated Markdown (# Title)
            # It is located after the YAML block.
            match = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
            filename_title = match.group(1).strip() if match else args.title
            out_path = Path(f"{sanitize_filename(filename_title)}.md")

        out_path.write_text(md, encoding="utf-8")
        print(str(out_path))

    except requests.HTTPError as e:
        print(f"HTTP error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Request error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
