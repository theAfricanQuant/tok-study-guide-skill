---
name: tok-study-guide
description: Help learners either understand supplied material through chapter-by-chapter HTML breakdowns or learn a chosen topic or skill through goal-focused teaching, practice, assessment, and progress tracking. On launch, identify the path and available materials. Use Grade 12 English by default; include metaphor styles only when requested. Use when someone asks to study, break down, learn, or practise a subject or skill.
---

# Learn from materials or build a skill

This skill supports two paths: a chapter-by-chapter breakdown of material the learner introduces, and goal-focused learning for a topic or skill. The learner may choose either path or combine them. Use Grade 12 English by default, adjusting when requested. A source breakdown is normally a standalone HTML guide. Goal-focused learning is interactive by default: teach one manageable part, ask for an attempt, assess it, give feedback, and adapt the next step. Save HTML lesson or practice material when it helps the learner or they request it. Create a PDF only when explicitly requested.

## Paths and environment (read first)

- **Skill directory (`$SKILL_DIR`)**: the folder containing this `SKILL.md`. All scripts are in `$SKILL_DIR/scripts/`. Run them from anywhere with the full path, e.g. `python3 "$SKILL_DIR/scripts/assemble.py" …` (or `uv run --no-project python …`).
- **Project folder (`$PROJECT_DIR`)**: scaffold one learning project per topic or source request. Default: `./learning-projects/<slug>/` in the current project. In the Claude.ai sandbox use `/mnt/user-data/outputs/learning-projects/<slug>/`. Follow `references/project-workflow.md` for the minimal path-specific folders; never place a project inside the installed skill directory.
- **Work folder (`$WORK_DIR`)**: scratch space for source extractions, maps, transcripts, and HTML parts. Default: `$PROJECT_DIR/work/`. Keep working files out of the published guide.
- **Output folders (`$OUTPUT_DIR`)**: use `$PROJECT_DIR/breakdowns/` for source-led guides and `$PROJECT_DIR/lessons/` for saved goal-focused lesson materials. In a combined project, save each output to its matching folder. Create a requested PDF beside its HTML file.
- **Delivery**: source breakdowns are normally delivered as HTML. For goal-focused learning, begin the interactive teach–attempt–feedback sequence in chat and save useful lesson or practice artifacts in the project. If an Artifact/publish tool exists, publish requested HTML; else if `present_files` exists, present it; otherwise save the artifact and tell the user its path.
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

When several materials are given, assign each a clear role in the selected learning path. Combine them into one coherent breakdown or goal-focused course unless the learner asks for separate outputs.

## Workflow

### 1. Choose the learning path and scaffold the project
At the start of a new request, identify whether the learner wants a full breakdown of material, to learn a particular topic or skill, or both, and whether they have material to include. If their request already makes the path clear, do not ask them to repeat it. Read [references/project-workflow.md](references/project-workflow.md), ask only the next questions needed for the chosen path, and create the project folders before beginning source extraction or teaching. In a goal-focused path, present a short route to the goal, then begin teaching the first manageable subskill in the interaction.

### 2. Gather sources and establish the learning brief
For a YouTube source, fetch its transcript into `$WORK_DIR`:
```bash
python3 "$SKILL_DIR/scripts/fetch_transcript.py" "<url>" --out "$WORK_DIR/<slug>.txt"
```
The script writes readable transcript text, `<out>.timestamps.txt` (caption cues with time anchors), and `<out>.meta.json` (title, channel, URL). Use the transcript to understand the argument and the timestamp sidecar to locate and cite spoken moments. A transcript does not show what is on screen: inspect a relevant video moment or supplied frame when a visual matters, and never claim to have seen a visual you could not access.

#### When YouTube blocks transcript access
The fetcher tries several player clients, then an unauthenticated API fallback. If YouTube blocks the current runtime, ask for a transcript or captions. If the user explicitly chooses local browser authentication, use `--cookies-from-browser` only when this script is running on that user's trusted machine. A local `--cookies <file>` option is also available for a private cookie file. Never ask for or accept an uploaded, pasted, emailed, or committed logged-in cookie jar; these cookies grant account access. Do not access a browser profile without explicit user direction. Cookie values must never be logged or forwarded to the API fallback. Keep TLS certificate verification enabled; configure a trusted CA if the local network intercepts TLS.

Read each source fully, using ~40,000-character chunks for long transcripts. Keep a compact **source ledger** as you read: assign each source an ID (`V1`, `P1`, `R1`), record its type/title/link, note its main ideas, and capture precise anchors. Use timestamps for videos, page numbers for PDFs, headings for articles, slide numbers for decks, and file/symbol/line or notebook section/cell for code. Mark conflicts or gaps instead of silently blending them. Correct caption-garbled names only when confident.

Set a short **learning brief** from the request and source: what the learner should be able to do, what they likely know already, and any practical context. If prior knowledge is uncertain, open with a quick, low-stakes self-check and give the answer or feedback; do not make the whole guide depend on an unsupported assumption. Ask a question only when the missing context would materially change the lesson.

### 3. Design the breakdown or learning path
Before designing an output, read [references/learning-design.md](references/learning-design.md). It explains how to select memorization, durable-learning, practice, or combined methods and how to make teaching, testing, grading, and progress evidence fit the learner's goal. Choose practice from the learner's intended performance, not merely from whether the source is a PDF, video, article, slide deck, or code repository. If the goal includes several abilities, map each one to a suitable attempt and feedback method instead of forcing one generic exercise to cover them all. Before drafting, create `$WORK_DIR/learning-map.md` with the finish line, likely starting point, section sequence and links, chosen method cards with reasons, and where each choice will appear in the HTML. Keep this map in the work folder, not the published lesson. After assembly, review the finished page against it and remove any technique that is only decorative. This makes the design repeatable for another skill user without forcing method-book names into the lesson. Keep method-book names and citations out of the lesson unless requested or those books are lesson sources. Use course files and progress records only when ongoing continuity is useful.

For a source-breakdown path, follow the material’s chapters or sections and preserve its structure. For a goal-focused path, organize the lesson around the learner’s observable finish line and the subskills needed to reach it. Choose the length and number of sections to fit the request and material. The guide can be long when the source warrants it; do not pad a short source to hit a chapter, quiz, analogy, or glossary quota. For a broad or technical subject, a useful path is:
1. **Orient:** state the practical mission, why it matters, prerequisite ideas, and how the sources fit together. Set a few observable outcomes. If prior knowledge is uncertain, use a short, low-stakes check and give feedback.
2. **Build knowledge:** explain concepts in an order where each depends on what came before; define notation and terms before relying on them.
3. **Model and practice:** when the goal includes a procedure or performance, demonstrate a worked example and make the key decisions visible. Then give the learner a related task to solve or perform, reducing hints as they gain control.
4. **Use judgment and transfer:** explain what the result means, its assumptions and limits, when the method fits, and how to recognize when it does not. Where useful, ask the learner to apply the idea to a new case or context.
5. **Retrieve and plan:** when retrieval fits the outcome, use a short recall or application check on ideas already taught. Let the learner attempt it before feedback; explain the reasoning and offer a useful correction or retry. End with an actionable next step, including a spaced return when it suits the goal, plus references and a focused glossary when they help.

Give each major section one clear learner outcome. Make transitions explicit: say what the current idea uses from the previous one and what it unlocks next. Match examples and practice to what the learner needs to do: calculate, explain, code, interpret, speak, write, observe, decide, or perform. If the sources disagree, show the disagreement and identify which source supports each account. Use an analogy only when it makes a specific relationship easier to picture; do not force one into every section. Draw diagrams selectively when they clarify a relationship that prose alone would make harder to see.

### 4. Teach from evidence across media
Use the source ledger while writing or tutoring, not just when assembling References. Attach a source anchor close to each important claim, worked example, or interpretation. Link video citations to the exact YouTube time; cite PDF pages, article headings, slide numbers, or code/notebook locations as appropriate. A claim supported by several sources can cite several anchors. Keep source-derived claims distinct from your own explanation, calculations, and checks. Never invent a timestamp, page, cell, result, or visual detail.

For a mixed-source lesson, give each source a job in the same learning path: for example, a video introduces the intuition, a notebook makes the calculation visible, and a paper explains the assumptions. Explain that connection at the point where it helps the learner. For YouTube, make citations clickable at the cue time by linking to the video's canonical URL with `&t=<seconds>s` (or `?t=` when there is no existing query), converting `HH:MM:SS` to seconds. If a transcript is available but its visual content is not, cite the spoken explanation and say that the visual could not be checked.

In goal-focused learning, teach a manageable chunk and elicit the learner’s attempt before giving the answer when they have enough grounding to try. Assess the response they actually gave against the stated criteria: identify what is sound, correct the most important gap, give a retry, and adapt the next challenge. Update the progress record from demonstrated work. Use course files only for useful continuity; never record silence or lesson completion as mastery.

### 5. Verify claims, examples, and code
Run all code from the materials, and any code you add, in the sandbox (install missing Python packages with `uv pip install …` or `pip install …`). Download the sample datasets the sources use. Then:
- Show genuine results in `pre.out` "real output" boxes. Never invent outputs.
- Where it helps, run small **benchmarks** (same data, two tools; time and peak memory in fresh processes) and chart them, saying they're from the test machine.
- When the materials contain a bug, an impossible value or an outdated detail, explain it in a `.warn` box with the tested fix.
- If something can't run (no API key, paid service), say so and, if useful, rehearse with the real helper code plus a clearly labeled scripted stand-in.

### 6. Use images selectively
Metaphors are opt-in. If the learner requests a metaphor style, read `references/metaphors.md`; otherwise teach with direct explanations, worked examples, and diagrams where useful. Search for photos only when an explicitly requested metaphor or a real source object would be clearer with a photo. Then:
```bash
python3 "$SKILL_DIR/scripts/find_photos.py" search --out "$WORK_DIR/photos" \
  --q object="<requested object or setting>|<alternate wording>"
# view the contact sheet and choose a useful, clearly licensed image
python3 "$SKILL_DIR/scripts/find_photos.py" pick --out "$WORK_DIR/photos" object=0
```
`pick` writes `$WORK_DIR/photos/picked.json` (compressed data URIs plus credits). Use `photo_html(key, alt)` from the script, or the snippet in `references/components.md`, to place each photo in the single reading column **with its credit line**. Keep every photo as a centered block figure between paragraphs, using the same balanced left/right gutters as the text. Never place a photo next to or behind prose. Use a photo only when it clarifies a useful analogy or real-world object; there is no photo quota. Skip weak matches rather than using a poor image.

### 7. Write HTML artifacts when useful or requested
A source-breakdown path normally produces an HTML guide. In a goal-focused path, continue teaching and assessing in the interaction; create an HTML reference or practice module only when it helps the learner or they request one. When preparing HTML, read `references/components.md` for every snippet. Split long body content into manageable part files (`$WORK_DIR/<slug>/02.html …`); a short guide can use fewer. Use this reading order: header (stacked hero + navigation) → intro → connected sections → actionable plan when useful → focused glossary when useful → references → footer. Keep the full lesson in one centered reading column with visible, even left/right margins. Center prose blocks as well as figures so their edges line up. Put each diagram or photo on its own line within the explanation: introduce what readers should notice, show a large centered figure, then explain what it demonstrates and connect it to the next idea. Captions alone do not replace this explanation. Never use a tiny side-column image or place text and images side by side.

### 8. Assemble, check, and publish HTML artifacts
Use this step when a source-breakdown guide or requested/useful goal-focused HTML artifact is being produced.
```bash
python3 "$SKILL_DIR/scripts/assemble.py" --title "…" --description "…" --accent "#C27C0E" \
  --out $OUTPUT_DIR/<slug>.html $WORK_DIR/<slug>/02.html …
python3 "$SKILL_DIR/scripts/check_page.py" $OUTPUT_DIR/<slug>.html
```
"Mobile overflow" should list nothing except `SPAN`s inside scrolling code blocks; fix anything else (usually `min-width:0` or a long unbroken string). View a few screenshot slices and fix clipped diagram labels. Publish with the Artifact tool if available (update the same artifact URL when revising), otherwise `present_files`.

### 9. PDF export (only when explicitly requested)
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
- Clear English at about a Grade 12 level by default: short sentences, active voice. Define every technical term the first time (inline `term` tooltip) and again in the glossary, and help readers *picture* it (what a table looks like, what a row represents).

**Page layout and typography**
- Use a single, centered text column with visibly balanced left/right margins and a comfortable line length (about 42–46rem for prose on screen). Center the prose container itself; do not leave a narrow text block pinned to the left of a wider page. Keep the page background, spacing, and chapter rhythm calm and consistent.
- Use the bundled body sans-serif and display serif consistently. Keep body text at a readable size with generous line spacing. Do not introduce extra font families for decoration.
- Justify prose paragraphs, list copy, captions, and explanatory callouts with `text-align: justify; text-justify: inter-word; hyphens: auto;`. Keep headings, navigation, tables, and code left-aligned for legibility.
- Never put a photo, diagram, screenshot, or chart beside prose. Do not use floats, tiny side-column graphics, or a text-plus-image grid. Stack hero text and hero art vertically. Put every figure in the reading column as a centered block, at up to 100% of that column, with its caption directly below. Make diagrams broad enough to read at phone size; if labels would need to be shrunk, simplify or split the diagram instead.
- Preserve the same one-column reading order on narrow screens and in A4 print. Prevent horizontal overflow; use the existing print margins.

**Metaphors are opt-in.** Do not default to Naija, African, Global South, or other culture-specific metaphors. If the learner explicitly requests metaphors or a particular setting, follow that preference and use `references/metaphors.md` as an optional idea bank. Direct explanation, concrete examples, and diagrams remain the default.

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
- `references/metaphors.md`: optional metaphor guidance and examples, used only when the learner asks for metaphors.
- `references/project-workflow.md`: first-turn path selection, learner questions, project folders, and progress handoff.
- `references/learning-design.md`: method choices, teaching and assessment loops, subject-specific practice, and progress evidence.
