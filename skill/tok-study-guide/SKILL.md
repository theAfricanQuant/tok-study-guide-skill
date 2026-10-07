---
name: tok-study-guide
description: Turn learning materials (YouTube videos, PDFs, articles, slide decks, GitHub repos, transcripts) into a long, beautiful, beginner-friendly HTML lesson; create a PDF copy only when explicitly requested. Lessons use simple 12th-grade English, Nigerian and wider African / Global South metaphors (okada / boda boda, danfo / matatu, keke / tuk-tuk, jollof, injera, ugali), openly licensed photos, original SVG diagrams, tested code with real outputs, short histories, every story from the sources, a step-by-step plan, a glossary and a References section. Use this skill whenever the user shares videos, PDFs, links or repos and asks to "study this", "break it down", "explain this simply", "make a lesson / study guide / textbook chapter", "turn this into an HTML page or PDF", "do the same as before", or uploads earlier guides and asks for more like them.
---

# Materials → HTML lesson (PDF only on request)

Turn whatever the user provides into one self-contained HTML lesson that a complete beginner reads start to finish. Create a colorful PDF copy only when the user explicitly asks for one. Write the lesson like a good textbook chapter or blog post meant for students, not a reply to the user.

## Paths and environment (read first)

- **Skill directory (`$SKILL_DIR`)**: the folder containing this `SKILL.md`. All scripts are in `$SKILL_DIR/scripts/`. Run them from anywhere with the full path, e.g. `python3 "$SKILL_DIR/scripts/assemble.py" …` (or `uv run --no-project python …`).
- **Output folder (`$OUTPUT_DIR`)**: where the finished `.html` lesson goes; `.pdf` is written here only when explicitly requested. Default: `./lesson-output/` in the current project. In the Claude.ai sandbox use `/mnt/user-data/outputs/`.
- **Work folder (`$WORK_DIR`)**: scratch space for body parts, transcripts and photos. Default: `./lesson-work/`. In the Claude.ai sandbox use `/home/claude/` and `/tmp/`.
- **Delivery**: if an Artifact/publish tool exists (Claude.ai), publish the HTML; else if `present_files` exists, present it; otherwise just save it to `$OUTPUT_DIR` and tell the user the path and to open it in a browser.
- **Python to use**: if `$SKILL_DIR/.venv/bin/python` (Windows: `$SKILL_DIR\.venv\Scripts\python.exe`) exists, run every script with it instead of `python3`; it has all dependencies installed (created by `npx tok-study-guide-skill setup`).
- **Dependencies**: Python 3.10+, `yt-dlp`, `pillow`, `playwright` (+ Chromium), `curl`, `git`, and `pdftoppm` (poppler). If something is missing, run `npx tok-study-guide-skill doctor` (when installed via npm) or install it before starting.

## Inputs you may get (often several at once)

| Material | How to get the content |
|---|---|
| YouTube link or ID | `scripts/fetch_transcript.py` (below). It saves readable transcript text plus a timestamped cue sidecar. On access blocks, follow the local-only cookie guidance below or ask for captions. |
| PDF (article, paper, slides) | If its text is already in context, use it. Otherwise read the `pdf-reading` (or `file-reading`) skill and extract it from the uploads folder (Claude.ai: `/mnt/user-data/uploads/`). |
| GitHub repo | `git clone --depth 1 <url> "$WORK_DIR/repo"`, then read the README, docs and main code files. |
| Web article URL | `curl -sL -A "Mozilla/5.0" <url>` and strip tags; if blocked, ask for a PDF or paste. |
| Earlier guide (HTML) to "do the same" with | Pull its source links (`youtube.com/watch`, `youtu.be`, `github.com`) from the file, re-fetch the materials, and rebuild from scratch in this format. |

When several materials are given, make **one combined lesson** that flows from basics to advanced, unless the user asks for separate guides.

## Workflow

### 1. Gather sources and establish the learning goal
```bash
python3 "$SKILL_DIR/scripts/fetch_transcript.py" "<url>" --out "$WORK_DIR/<slug>.txt"
```
For YouTube, the script writes readable transcript text, `<out>.timestamps.txt` (caption cues with time anchors), and `<out>.meta.json` (title, channel, URL). Use the readable transcript to understand the argument and the timestamp sidecar to locate and cite spoken moments. A transcript does not show what is on screen: inspect a relevant video moment or supplied frame when a visual matters, and never claim to have seen a visual you could not access.

#### When YouTube blocks transcript access
The fetcher tries several player clients, then an unauthenticated API fallback. If YouTube blocks the current runtime, ask for a transcript or captions. If the user explicitly chooses local browser authentication, use `--cookies-from-browser` only when this script is running on that user's trusted machine. A local `--cookies <file>` option is also available for a private cookie file. Never ask for or accept an uploaded, pasted, emailed, or committed logged-in cookie jar; these cookies grant account access. Do not access a browser profile without explicit user direction. Cookie values must never be logged or forwarded to the API fallback. Keep TLS certificate verification enabled; configure a trusted CA if the local network intercepts TLS.

Read each source fully, using ~40,000-character chunks for long transcripts. Keep a compact **source ledger** as you read: assign each source an ID (`V1`, `P1`, `R1`), record its type/title/link, note its main ideas, and capture precise anchors. Use timestamps for videos, page numbers for PDFs, headings for articles, slide numbers for decks, and file/symbol/line or notebook section/cell for code. Mark conflicts or gaps instead of silently blending them. Correct caption-garbled names only when confident.

Set a short **learning brief** from the request and source: what the learner should be able to do, what they likely know already, and any practical context. If prior knowledge is uncertain, open with a quick, low-stakes self-check and give the answer or feedback; do not make the whole guide depend on an unsupported assumption. Ask a question only when the missing context would materially change the lesson.

### 2. Design one connected learning path
Choose the length and number of sections to fit the user's request and the material. Do not pad a short source to hit a chapter, quiz, analogy, or glossary quota. For a broad or technical subject, a useful path is:
1. **Orient:** state the practical mission, why it matters, prerequisite ideas, and how the sources fit together.
2. **Build knowledge:** explain the concepts in an order where each depends on what came before; define notation and terms before relying on them.
3. **Practice a skill:** work a concrete example, calculation, code change, observation, or interpretation grounded in the source.
4. **Use judgment:** explain what the result means, its assumptions and limits, when to use the idea, and how to recognize a case where it does not apply.
5. **Connect and retrieve:** revisit the core chain of ideas, use short recall/application checks with clear feedback, and end with an actionable plan plus references and a focused glossary when they help.

Give each major section one clear learner outcome. Make transitions explicit: say what the current idea uses from the previous one and what it unlocks next. Explain why examples are concrete: readers can calculate, observe, run, compare, or decide something with them. If the sources disagree, show the disagreement and identify which source supports each account. Use an analogy only when it makes a specific relationship easier to picture; do not force one into every section. Draw diagrams selectively when they clarify a relationship that prose alone would make harder to see.

### 3. Teach from evidence across media
Use the source ledger while writing, not just when assembling References. Attach a source anchor close to each important claim, worked example, or interpretation. Link video citations to the exact YouTube time; cite PDF pages, article headings, slide numbers, or code/notebook locations as appropriate. A claim supported by several sources can cite several anchors. Keep source-derived claims distinct from your own explanation, calculations, and checks. Never invent a timestamp, page, cell, result, or visual detail.

For a mixed-source lesson, give each source a job in the same learning path: for example, a video introduces the intuition, a notebook makes the calculation visible, and a paper explains the assumptions. Explain that connection at the point where it helps the learner. For YouTube, make citations clickable at the cue time by linking to the video's canonical URL with `&t=<seconds>s` (or `?t=` when there is no existing query), converting `HH:MM:SS` to seconds. If a transcript is available but its visual content is not, cite the spoken explanation and say that the visual could not be checked.

For a continuing course or a user who wants future sessions to build on this one, read [references/learning-design.md](references/learning-design.md). Use its mission, source, and learning records only when ongoing continuity is useful; a one-off guide should stay self-contained.

### 4. Test everything you can (this is what makes the lesson trustworthy)
Run all code from the materials, and any code you add, in the sandbox (install missing Python packages with `uv pip install …` or `pip install …`). Download the sample datasets the sources use. Then:
- Show genuine results in `pre.out` "real output" boxes. Never invent outputs.
- Where it helps, run small **benchmarks** (same data, two tools; time and peak memory in fresh processes) and chart them, saying they're from the test machine.
- When the materials contain a bug, an impossible value or an outdated detail, explain it in a `.warn` box with the tested fix.
- If something can't run (no API key, paid service), say so and, if useful, rehearse with the real helper code plus a clearly labeled scripted stand-in.

### 5. Find photos for the analogies
Read `references/metaphors.md`. Then:
```bash
python3 "$SKILL_DIR/scripts/find_photos.py" search --out $WORK_DIR/photos \
  --q danfo="danfo bus lagos|lagos danfo" --q injera="injera|injera platter"
# view $WORK_DIR/photos/sheet_<key>.jpg with the image viewer, choose the best index for each key
python3 "$SKILL_DIR/scripts/find_photos.py" pick --out $WORK_DIR/photos danfo=0 injera=0
```
`pick` writes `$WORK_DIR/photos/picked.json` (compressed data URIs plus credits). Use `photo_html(key, alt)` from the script, or the snippet in `references/components.md`, to place each photo in the single reading column **with its credit line**. Keep every photo as a centered block figure between paragraphs, using the same balanced left/right gutters as the text. Never place a photo next to or behind prose. Use a photo only when it clarifies a useful analogy or real-world object; there is no photo quota. Skip weak matches rather than using a poor image.

### 6. Write the body in parts
Read `references/components.md` for every snippet. Split long body content into manageable part files (`$WORK_DIR/<slug>/02.html …`); a short guide can use fewer. Use this reading order: header (stacked hero + navigation) → intro → connected sections → actionable plan when useful → focused glossary when useful → references → footer. Keep the full lesson in one centered reading column with visible, even left/right margins. Center prose blocks as well as figures so their edges line up. Put each diagram or photo on its own line within the explanation: introduce what readers should notice, show a large centered figure, then explain what it demonstrates and connect it to the next idea. Captions alone do not replace this explanation. Never use a tiny side-column image or place text and images side by side.

### 7. Assemble, check, publish
```bash
python3 "$SKILL_DIR/scripts/assemble.py" --title "…" --description "…" --accent "#C27C0E" \
  --out $OUTPUT_DIR/<slug>.html $WORK_DIR/<slug>/02.html …
python3 "$SKILL_DIR/scripts/check_page.py" $OUTPUT_DIR/<slug>.html
```
"Mobile overflow" should list nothing except `SPAN`s inside scrolling code blocks; fix anything else (usually `min-width:0` or a long unbroken string). View a few screenshot slices and fix clipped diagram labels. Publish with the Artifact tool if available (update the same artifact URL when revising), otherwise `present_files`.

### 8. PDF export (only when explicitly requested)
```bash
python3 "$SKILL_DIR/scripts/make_pdf.py" $OUTPUT_DIR/<slug>.html --title "Short running title"
pdftoppm -r 40 -png $OUTPUT_DIR/<slug>.pdf $WORK_DIR/pp   # then view a few pages
```
Headless Chromium prints the same single-column layout with `assets/print.css`: a cover, a Contents page, one chapter per page, unsplit boxes and diagrams, wrapped code, open quiz answers, and "Page X of Y" footers. If a diagram is too large on paper, adjust `print.css` and re-run. Deliver with `present_files`.

## Writing rules

**Preserve the established HTML design system.** New lessons should look like the guides this skill already produces: reuse the bundled templates, CSS, palette, font choices, spacing, component styles, and diagram conventions. The teaching workflow changes the explanation and its sequence, not the visual identity. Do not replace the theme, introduce new fonts or colors, or invent a different diagram style unless the user explicitly asks for a design change. Read `references/components.md` and follow its existing components for any new figures or callouts.

**Voice: a textbook for students, not a reply to the user.**
- Never write "you shared", "you asked", "your question", "for you". Write "A common first question is…", "We tested…", "This guide…".
- First person plural ("we built the same table…") for tests; otherwise neutral.
- Mention the source authors by name only in the intro (one sentence) and the References. Elsewhere: "the article", "the first video", "the repo", "the creator".
- Simple English for a curious 12th grader: short sentences, active voice. Define every technical term the first time (inline `term` tooltip) and again in the glossary, and help readers *picture* it (what a table looks like, what a row represents).

**Page layout and typography**
- Use a single, centered text column with visibly balanced left/right margins and a comfortable line length (about 42–46rem for prose on screen). Center the prose container itself; do not leave a narrow text block pinned to the left of a wider page. Keep the page background, spacing, and chapter rhythm calm and consistent.
- Use the bundled body sans-serif and display serif consistently. Keep body text at a readable size with generous line spacing. Do not introduce extra font families for decoration.
- Justify prose paragraphs, list copy, captions, and explanatory callouts with `text-align: justify; text-justify: inter-word; hyphens: auto;`. Keep headings, navigation, tables, and code left-aligned for legibility.
- Never put a photo, diagram, screenshot, or chart beside prose. Do not use floats, tiny side-column graphics, or a text-plus-image grid. Stack hero text and hero art vertically. Put every figure in the reading column as a centered block, at up to 100% of that column, with its caption directly below. Make diagrams broad enough to read at phone size; if labels would need to be shrunk, simplify or split the diagram instead.
- Preserve the same one-column reading order on narrow screens and in A4 print. Prevent horizontal overflow; use the existing print margins.

**Metaphors** come from Nigeria first and the wider Global South (see `references/metaphors.md`). Name both regional terms when they differ (okada / boda boda, danfo / matatu, keke / bajaj / tuk-tuk). No German, American or European metaphors unless the user asks.

**Your own words, always.** Paraphrase video and article content. Short attributed quotes only. Never paste transcript passages, lyrics, book excerpts, or long periodical passages. Code and short excerpts from documents the user supplied may be quoted with attribution.

**Images:**
- Diagrams are original SVG drawn from simple shapes. Each must teach a point explained in the nearby prose, not act as a tiny decoration. Use a compact, readable viewBox (prefer width ≤ 680 units), main labels of at least 24 units and secondary labels of at least 20 units; stack steps instead of squeezing them into a wide strip. If the information does not fit, simplify the figure or split it into two. Never draw logos, brand marks, film/TV/game/comic characters, movie posters or other existing artwork; name them in text instead.
- Photos must be openly licensed (CC0, CC BY, CC BY-SA, public domain) and credited under the image with title, creator, license and link. `find_photos.py` handles this.
- Do not embed news-outlet or magazine photos. Link to the article instead. Official government pages released under open licences (e.g. GOV.UK's Open Government Licence) may be clipped with the licence noted, but crop out crests and logos.

**Accuracy:**
- Attribute claims ("the video says…"). Present money, follower and benchmark figures from sources as their claims; present your own measurements as from the test machine.
- Flag simplifications (e.g. "this left/right-brain split is a simplification") and correct known errors gently.
- Correct caption-garbled names when confident, and mention it in the reply.
- Python commands shown to readers use `uv` (`uv add …`, `uv run …`).

**History** belongs in the foundations: when a topic has a past (SQL, spreadsheets, file formats, a framework), add a dated timeline with original diagrams and cite primary sources in References.

**Every lesson ends with:**
- **Action plan:** when useful, give ordered, practical steps with timing or "when" cues. Make clear that it synthesizes the sources rather than quoting one of them.
- **Glossary:** include the key terms readers need for this guide; keep it proportional to the material.
- **References:** cite the sources actually used, grouped by type when there are several. Include title, venue/date, direct link and useful anchors where available.

## Bundled files

- `scripts/fetch_transcript.py`: YouTube → readable transcript, timestamped caption-cue sidecar, and metadata. Cycles player clients and subtitle tracks, supports explicit local cookie sources, keeps TLS verification enabled, and gives access-block guidance without asking for credentials.
- `scripts/find_photos.py`: Openverse search → contact sheets → picked photos as data URIs with credits.
- `scripts/assemble.py`: template + body parts → final HTML (derives the accent palette).
- `scripts/check_page.py`: mobile overflow check + desktop/mobile screenshot slices.
- `scripts/make_pdf.py` + `assets/print.css`: colorful A4 PDF via headless Chromium.
- `assets/template_head.html` / `assets/template_foot.html`: design system (light/dark, consistent fonts, justified single-column prose, centered block figures, code/output/warn/table/part/photo styles) and the lightweight scroll script.
- `references/components.md`: every HTML snippet and the SVG diagram cookbook.
- `references/metaphors.md`: metaphor rules, a bank of concept → metaphor mappings, and photo search terms.
- `references/learning-design.md`: optional course mission and learning records for continuing study.
