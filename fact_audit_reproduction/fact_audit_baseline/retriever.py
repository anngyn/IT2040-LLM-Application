"""Wikipedia-based evidence retriever for FACT-AUDIT RAG pipeline.

Uses the public Wikipedia API (no key required) to search for relevant
articles and extract introductory passages as evidence for fact-checking.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List
from urllib import request
from urllib.parse import urlencode

import json
import re

WIKI_API = "https://en.wikipedia.org/w/api.php"


def _wiki_search(query: str, limit: int = 5, retries: int = 3) -> List[Dict[str, Any]]:
    """Search Wikipedia and return a list of {title, snippet} dicts."""
    params = urlencode({
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
    })
    url = f"{WIKI_API}?{params}"
    for attempt in range(retries):
        try:
            req = request.Request(url, headers={"User-Agent": "FACT-AUDIT-RAG/1.0"})
            with request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            results = data.get("query", {}).get("search", [])
            return [{"title": r["title"], "snippet": r.get("snippet", "")} for r in results]
        except Exception:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    return []


def _wiki_extract(title: str, max_chars: int = 1500, retries: int = 3) -> str:
    """Get plain-text extract of a Wikipedia article's intro section."""
    params = urlencode({
        "action": "query",
        "titles": title,
        "prop": "extracts",
        "exintro": "true",
        "explaintext": "true",
        "exchars": max_chars,
        "format": "json",
    })
    url = f"{WIKI_API}?{params}"
    for attempt in range(retries):
        try:
            req = request.Request(url, headers={"User-Agent": "FACT-AUDIT-RAG/1.0"})
            with request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for page in pages.values():
                extract = page.get("extract", "")
                if extract:
                    return extract.strip()
            return ""
        except Exception:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    return ""


def _strip_html(text: str) -> str:
    """Remove HTML tags from Wikipedia search snippets."""
    return re.sub(r"<[^>]+>", "", text)


def retrieve_wikipedia(
    claim: str,
    top_k: int = 5,
    max_chars_per_article: int = 1500,
    delay: float = 1.0,
) -> List[Dict[str, str]]:
    """Retrieve top-k Wikipedia passages relevant to a claim.

    Returns a list of dicts matching schema_rag.json's retrieved_evidence:
        [{"text": ..., "source": ..., "score": ...}, ...]
    """
    search_results = _wiki_search(claim, limit=top_k)
    evidence: List[Dict[str, str]] = []

    for i, result in enumerate(search_results):
        title = result["title"]
        extract = _wiki_extract(title, max_chars=max_chars_per_article)
        if not extract:
            extract = _strip_html(result.get("snippet", ""))
        if not extract:
            continue

        evidence.append({
            "text": extract,
            "source": f"Wikipedia - {title}",
            "score": round(1.0 - (i * 0.1), 2),
        })

        if delay > 0 and i < len(search_results) - 1:
            time.sleep(delay)

    return evidence
