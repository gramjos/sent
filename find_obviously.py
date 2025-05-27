import re
from dataclasses import dataclass
from typing import List, Iterable

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
    """Return lines that contain the word 'obviously'."""
    pattern = re.compile(r"\bobviously\b", re.IGNORECASE)
    return [line for line in text.splitlines() if pattern.search(line)]


def search_and_scan(query: str, max_results: int = 50) -> Iterable[ObviouslyMatch]:
    """Search arXiv and yield matches where a line starts with 'Obviously'."""
    if arxiv is None or extract_text is None or requests is None:
        raise RuntimeError("Required packages are not installed")

    search = arxiv.Search(query=query, max_results=max_results)
    for result in search.results():
        pdf_url = result.pdf_url
        resp = requests.get(pdf_url, timeout=10)
        resp.raise_for_status()
        text = extract_text(resp.content)
        for line in scan_text_for_obviously(text):
            yield ObviouslyMatch(result.title, [a.name for a in result.authors], line)


if __name__ == "__main__":  # pragma: no cover
    for match in search_and_scan("cat:math", max_results=5):
        print(f"{match.title} - {', '.join(match.authors)}")
        print(f"\t{match.line}")
