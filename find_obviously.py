import re
from dataclasses import dataclass
from typing import List, Iterable, Optional, TextIO
import random

try:
    import arxiv  # type: ignore
    import requests
    from pdfminer.high_level import extract_text
except Exception:  # pragma: no cover - optional deps
    arxiv = None  # type: ignore
    extract_text = None
    requests = None


@dataclass
class ObviouslyMatch:
    title: str
    authors: List[str]
    line: str


def scan_text_for_obviously(text: str) -> List[str]:
    """Return lines that start with 'Obviously'."""
    pattern = re.compile(r"^\s*Obviously\b", re.IGNORECASE)
    return [line for line in text.splitlines() if pattern.search(line)]


def extract_random_snippet(text: str, length: int = 80) -> str:
    """Return a random snippet from the given text."""
    text = text.replace("\n", " ").strip()
    if len(text) <= length:
        return text
    start = random.randint(0, len(text) - length)
    return text[start : start + length]


def scan_text(
    text: str,
    title: str,
    authors: List[str],
    log_file: Optional[TextIO] = None,
) -> Iterable[ObviouslyMatch]:
    """Scan the text for matches and optionally log a snippet."""
    if log_file:
        snippet = extract_random_snippet(text, 60)
        log_file.write(f"{title} | {snippet}\n")
    for line in scan_text_for_obviously(text):
        yield ObviouslyMatch(title, authors, line)


def search_and_scan(
    query: str, max_results: int = 50, log_path: Optional[str] = None
) -> Iterable[ObviouslyMatch]:
    """Search arXiv and yield matches where a line starts with 'Obviously'.

    Parameters
    ----------
    query:
        arXiv query string.
    max_results:
        maximum number of results to fetch.
    log_path:
        optional path to a log file where proof-of-work information is written.
    """
    if arxiv is None or extract_text is None or requests is None:
        raise RuntimeError("Required packages are not installed")

    log_file: Optional[TextIO]
    if log_path:
        log_file = open(log_path, "w", encoding="utf-8")
    else:
        log_file = None

    try:
        search = arxiv.Search(query=query, max_results=max_results)
        for result in search.results():
            pdf_url = result.pdf_url
            resp = requests.get(pdf_url, timeout=10)
            resp.raise_for_status()
            text = extract_text(resp.content)
            yield from scan_text(
                text, result.title, [a.name for a in result.authors], log_file
            )
    finally:
        if log_file:
            log_file.close()


if __name__ == "__main__":  # pragma: no cover
    LOG_PATH = "obviously_log.txt"
    for match in search_and_scan("cat:math", max_results=5, log_path=LOG_PATH):
        print(f"{match.title} - {', '.join(match.authors)}")
        print(f"\t{match.line}")
    print(f"Log written to {LOG_PATH}")
