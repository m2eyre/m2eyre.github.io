# CLAUDE.md: maintaining Matthew Eyre's portfolio site

This is the instruction file for Claude Code (or any AI agent) working in this repo.
Read it fully before changing anything.

## What this is

A static portfolio site for Matthew Eyre, a Mechanical Engineering co-op student at the
University of Waterloo. It is aimed at mechanical and aerospace engineering recruiters.
It is hosted free on GitHub Pages at https://m2eyre.github.io from the `main` branch.

Plain HTML, CSS and a little JavaScript. No framework, no build step, no package manager,
no backend. Keep it that way unless Matthew explicitly asks otherwise.

## Rules that matter most

1. **Never invent engineering facts.** No measurements, test results, percentages, team
   achievements, responsibilities, dates or employers that Matthew has not provided.
   If a case-study section needs information you don't have, add a draft note
   (`<p class="todo">…</p>`) describing what's needed and ask Matthew.
2. **Keep "my contribution" separate from team work.** Team projects must say what
   Matthew did himself.
3. **Relative paths only.** Never start a link or asset path with `/`. Pages in
   `projects/` reference assets as `../assets/...`. This keeps the site working on both
   the user-site URL and any project-site URL.
4. **Run the checker before every commit** and fix all errors:
   `python3 scripts/check_site.py`
5. **No secrets, API keys or credentials** in the repo. Contact info is public by design.
   Don't add Matthew's phone number to the HTML.
6. Don't add contact forms that need a backend, analytics trackers, fake testimonials,
   proficiency bars, or stock photos.

## File map

| File | What it holds |
|---|---|
| `index.html` | Home: hero, project cards, skills, experience, about, contact |
| `projects/*.html` | One case-study page per project |
| `projects/_template.html` | Copy this to start a new project page (not published) |
| `assets/css/style.css` | All styles. Colours and fonts are tokens in `:root` at the top |
| `assets/js/main.js` | Mobile menu, `?draft` mode, footer year |
| `assets/img/` | WebP images, favicon, social preview image (`og-image.jpg`) |
| `assets/resume/Matthew-Eyre-Resume.pdf` | The resume every "Resume" link points to |
| `scripts/check_site.py` | Link, asset, alt-text and metadata checker (standard library only) |
| `.github/workflows/check.yml` | Runs the checker on every push and pull request |
| `_config.yml` | Tells GitHub Pages not to publish repo-only files |

## Common tasks

### Replace the resume
Overwrite `assets/resume/Matthew-Eyre-Resume.pdf`, keeping the same file name.
If the name must change, update every link to it: search for `Matthew-Eyre-Resume.pdf`.

### Add a project
1. Copy `projects/_template.html` to `projects/<slug>.html` (lowercase, hyphens).
2. Remove the TEMPLATE comment and the `noindex` meta tag. Fill in the title, meta
   description, title block, sections and table of contents (`case-toc` links must
   match section `id`s).
3. Add images to `assets/img/` (see Images below) and use the
   `<figure class="sheet">` pattern from an existing page, numbering figures per page.
4. Add a card for it in `index.html`: a `project-feature` article for a major project,
   or an `<article>` in the `project-list` grid for a smaller one.
5. Update the previous/next links at the bottom of the neighbouring project pages.
6. Run the checker.

### Images
- Convert to WebP, max 1600 px wide, quality ~80. With Pillow:
  `python3 -c "from PIL import Image; im=Image.open('in.png'); im.thumbnail((1600,1600)); im.save('assets/img/name.webp', quality=82)"`
- Always set `width` and `height` on `<img>` to the file's real pixel size.
- Every content image needs descriptive `alt` text: say what the figure shows.
  Use `alt=""` only for a decorative duplicate of an image that's described nearby.
- Use `loading="lazy"` on everything except the hero image.

### Draft notes
`<p class="todo">` notes are hidden on the live site. Add `?draft` to any URL
(e.g. `projects/cubesat.html?draft`) to see them. The checker lists them all.
When Matthew provides the missing information, replace the note with real content.

### Preview locally
From the repo root: `python3 -m http.server 8000`, then open http://localhost:8000.

## Style

- Palette (in `:root`): navy background, white text, one muted blue accent,
  light "drawing sheet" panels behind images. Don't add new accent colours or gradients.
- Fonts: Archivo (headings, uses width axis via `font-stretch`), IBM Plex Sans (body).
- Every figure is a `.sheet` with a `figcaption` title block ("Fig. n" + caption).
- The dimension-line motif (`.dim`) is used only where it carries real information
  (degree span, job dates). Don't use it as decoration.
- Copy is plain, first person, sentence case. No hype words.
- Keep motion minimal and respect `prefers-reduced-motion`.

## Verifying changes

1. `python3 scripts/check_site.py` must report 0 errors.
2. Preview locally and look at the changed pages at desktop width and at ~375 px wide.
3. Check keyboard navigation (Tab through links, visible focus ring) on new UI.
4. Commit with a clear message and push to `main`. GitHub Pages redeploys in about a minute;
   the check workflow runs automatically.
