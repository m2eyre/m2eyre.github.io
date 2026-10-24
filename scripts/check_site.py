#!/usr/bin/env python3
"""Site checker for the portfolio.

Run from the repository root:   python3 scripts/check_site.py

It checks every .html file for:
  - internal links and image/script/style paths that point to missing files
  - #anchors that don't exist on the target page
  - root-relative paths ("/assets/...") that break on a GitHub Pages project URL
  - images without alt text, or without width/height (causes layout shift)
  - pages missing a <title>, meta description or <h1>
  - leftover placeholder text (TODO, lorem ipsum, "PLACEHOLDER")
It also lists the "To add" draft notes still on each page, as information only.

Exits with code 1 if any errors are found, so it can run in GitHub Actions.
Uses only the Python standard library.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", ".github"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []        # (attr, value, line)
        self.ids = set()
        self.imgs = []        # (attrs dict, line)
        self.title = ""
        self._in_title = False
        self.has_desc = False
        self.h1 = 0
        self.todos = []
        self._todo_depth = 0
        self._todo_text = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if "id" in a:
            self.ids.add(a["id"])
        for attr in ("href", "src"):
            if attr in a and a[attr] is not None:
                self.refs.append((attr, a[attr], line))
        if tag == "img":
            self.imgs.append((a, line))
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name") == "description" and a.get("content"):
            self.has_desc = True
        if tag == "h1":
            self.h1 += 1
        if "todo" in (a.get("class") or "").split():
            self._todo_depth = 1
            self._todo_text = ""
        elif self._todo_depth:
            self._todo_depth += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if self._todo_depth:
            self._todo_depth -= 1
            if self._todo_depth == 0:
                self.todos.append(" ".join(self._todo_text.split()))

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._todo_depth:
            self._todo_text += data


def html_files():
    for p in sorted(ROOT.rglob("*.html")):
        if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            yield p


def main():
    pages = {}
    for f in html_files():
        parser = Page()
        parser.feed(f.read_text(encoding="utf-8"))
        pages[f.resolve()] = parser

    errors, warnings, notes = [], [], []

    for f, pg in pages.items():
        rel = f.relative_to(ROOT)
        is_template = f.name.startswith("_")

        if not is_template:
            if not pg.title.strip():
                errors.append(f"{rel}: missing <title>")
            if not pg.has_desc:
                errors.append(f"{rel}: missing meta description")
            if pg.h1 != 1:
                errors.append(f"{rel}: should have exactly one <h1> (found {pg.h1})")

        for attr, val, line in pg.refs:
            url = urlparse(val)
            if url.scheme in ("http", "https", "mailto", "tel", "data"):
                continue
            if val.startswith("//"):
                continue
            if val.startswith("/"):
                errors.append(f"{rel}:{line}: '{val}' starts with '/'. Use a relative path so it works on GitHub Pages project URLs")
                continue
            path_part = unquote(url.path)
            target = (f.parent / path_part).resolve() if path_part else f
            if path_part.endswith("/") or (target.is_dir()):
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{rel}:{line}: broken {attr} '{val}' (no file at {target.relative_to(ROOT) if ROOT in target.parents else target})")
                continue
            if url.fragment and target.suffix == ".html":
                tp = pages.get(target)
                if tp and url.fragment not in tp.ids:
                    errors.append(f"{rel}:{line}: link '{val}' points to missing anchor #{url.fragment}")

        for a, line in pg.imgs:
            if "alt" not in a:
                errors.append(f"{rel}:{line}: <img src='{a.get('src')}'> has no alt attribute (use alt=\"\" only for decorative images)")
            if not a.get("width") or not a.get("height"):
                warnings.append(f"{rel}:{line}: <img src='{a.get('src')}'> has no width/height")

        text = f.read_text(encoding="utf-8")
        # Case-sensitive on purpose: class="todo" draft notes are allowed, a stray "TODO" is not.
        for m in re.finditer(r"(?i:lorem ipsum)|PLACEHOLDER|\bTODO\b|\bTBD\b|\bXXX\b", text):
            ln = text.count("\n", 0, m.start()) + 1
            if not is_template:
                warnings.append(f"{rel}:{ln}: placeholder text '{m.group(0)}'")

        if pg.todos and not is_template:
            notes.append((rel, pg.todos))

    # Large images
    for img in (ROOT / "assets" / "img").glob("*"):
        if img.stat().st_size > 400_000:
            warnings.append(f"{img.relative_to(ROOT)}: {img.stat().st_size // 1024} KB, consider compressing (aim for under 400 KB)")

    resume = ROOT / "assets" / "resume"
    if not any(resume.glob("*.pdf")):
        errors.append("assets/resume/: no resume PDF found")

    print(f"Checked {len(pages)} pages.\n")
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARN   ", w)
    if notes:
        print("\nDraft notes still to fill in (hidden on the live site; add ?draft to a URL to see them):")
        for rel, todos in notes:
            print(f"  {rel}")
            for t in todos:
                print(f"    - {t}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
