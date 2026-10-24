# Matthew Eyre: engineering portfolio

Live site: **https://m2eyre.github.io**

A static site (HTML, CSS, a little JavaScript) hosted free on GitHub Pages.
Every push to `main` republishes it within about a minute.

## Quick edits

| I want to… | Edit this |
|---|---|
| Replace my resume | Overwrite `assets/resume/Matthew-Eyre-Resume.pdf` (keep the name) |
| Change my intro, skills, experience or contact links | `index.html` |
| Edit a project write-up | `projects/<project>.html` |
| Add a new project | Copy `projects/_template.html`, then add a card in `index.html` |
| Add images | Put WebP files in `assets/img/` |
| Change colours or fonts | Top of `assets/css/style.css` |

Detailed instructions are in `CLAUDE.md`, which is also what Claude Code reads.

## Preview locally

```bash
python3 -m http.server 8000
```
Then open http://localhost:8000. Add `?draft` to any URL to see the "To add" notes
that are hidden on the live site.

## Check for broken links and missing images

```bash
python3 scripts/check_site.py
```
This also runs automatically on GitHub after every push (see the Actions tab).

## Maintain with Claude Code

Open a terminal in this folder and run `claude`. Ask things like
"add my new project from these notes and images", "replace my resume", or
"run the checker and fix whatever it finds". Claude Code reads `CLAUDE.md` first.
