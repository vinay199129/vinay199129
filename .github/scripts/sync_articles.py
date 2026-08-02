#!/usr/bin/env python3
"""Rewrite the ARTICLES block in README.md from articles.json.

Only the text between the ARTICLES:START and ARTICLES:END markers is touched,
so everything else in the README stays hand-authored.
"""

from __future__ import annotations

import json
import pathlib
import sys

SITE = "https://vinay-p-singh.github.io"
MAX_ITEMS = 5
START = "<!-- ARTICLES:START -->"
END = "<!-- ARTICLES:END -->"

readme_path = pathlib.Path("README.md")
articles_path = pathlib.Path("articles.json")


def render(articles: list[dict]) -> str:
    if not articles:
        return "_Nothing published yet._"

    rows = ["| | Article | Topics |", "|---|---|---|"]
    for a in articles[:MAX_ITEMS]:
        slug = a.get("slug", "")
        title = a.get("title", slug).replace("|", "\\|")
        date = a.get("date", "")
        topics = " · ".join(a.get("topics", [])[:3]).replace("|", "\\|")
        rows.append(f"| `{date}` | **[{title}]({SITE}/articles/{slug}/)** | {topics} |")

    rows.append("")
    rows.append(f"[All writing →]({SITE}/)")
    return "\n".join(rows)


def main() -> int:
    data = json.loads(articles_path.read_text(encoding="utf-8"))
    articles = sorted(
        data.get("articles", []),
        key=lambda a: a.get("date", ""),
        reverse=True,
    )

    readme = readme_path.read_text(encoding="utf-8")
    if START not in readme or END not in readme:
        print(f"error: markers {START} / {END} not found in README.md", file=sys.stderr)
        return 1

    head, _, rest = readme.partition(START)
    _, _, tail = rest.partition(END)
    readme_path.write_text(
        f"{head}{START}\n{render(articles)}\n{END}{tail}", encoding="utf-8"
    )
    print(f"Wrote {min(len(articles), MAX_ITEMS)} of {len(articles)} article(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
