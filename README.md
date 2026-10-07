# tok-study-guide-skill

The name **TOK** draws on the Berom verb *tɔk*, “to know; to understand; to know how to” (p. 162). It is a verb, not a noun meaning “knowledge” or “ability.” The dictionary separately lists *tɔk tsik* (“understanding”; p. 162, finderlist p. 243) and *tɔk ciwil* (“intelligence”; p. 162, finderlist p. 213). For “cleverness; skill; wisdom,” it lists *nèsisɛng* (p. 116), with *nètsitsɛng* as a synonym.

The Berom are an Indigenous people of Plateau State in north-central Nigeria, living mainly around the Jos Plateau, including Jos North, Jos South, Barkin Ladi, and Riyom ([Jos South LGA](https://jossouthlga.pl.gov.ng/ova_por/berom-art-and-culture-museum/)).

An **agent skill** that turns learning materials (YouTube videos, PDFs, articles, slide decks and GitHub repos) into a long, beautiful, beginner-friendly **HTML lesson**. HTML is the default output. A PDF is created only when explicitly requested, and it accompanies the HTML lesson.

Lessons are written in simple 12th-grade English, like a textbook chapter, and include:

- **Everyday Global South metaphors:** Nigerian first (danfo, okada, jollof, the POS agent), then wider Africa and Asia (boda boda, matatu, injera, ugali, matoke, banku, tuk-tuk), always naming both regional words.
- **Openly licensed photos**, found through Openverse and credited under each image.
- **Original SVG diagrams** that teach, with no logos or copyrighted characters.
- **Single-column, fully justified writeups** with a centered prose column, balanced page margins, and large, centered diagrams explained alongside the surrounding text. Photos and diagrams never sit in side columns.
- **Tested code** with genuine "real output" boxes, small benchmarks, and correction boxes when the source material has mistakes.
- **A connected learning path** that moves from understanding to practice to judgment, with clear source anchors and transitions that explain how each material contributes.
- **Short histories**, source-grounded examples, retrieval checks with feedback, an actionable plan, and focused glossary and References sections when they help.

It works with **Claude Code**, the **Claude Agent SDK**, **Claude.ai**, and any agent that can read a `SKILL.md` file or an `AGENTS.md` pointer (Codex, Cursor, Gemini CLI, OpenCode, and others).

---

## Quick start

Install straight from GitHub (works before it's on npm):

```bash
npx github:theAfricanQuant/tok-study-guide-skill install
```

Or from npm:

```bash
# 1. Install the skill (default target: Claude Code, ~/.claude/skills/)
npx tok-study-guide-skill install

# 2. Give the skill its own Python environment + Chromium (uses uv if you have it)
npx tok-study-guide-skill setup

# 3. Check everything
npx tok-study-guide-skill doctor
```

Then ask your agent:

> Make a beginner lesson from https://youtu.be/… and this PDF. Use Naija metaphors and make a PDF copy too.

## Install targets

| Target | Command | Where it goes | Use for |
|---|---|---|---|
| Claude Code, all projects (default) | `npx tok-study-guide-skill install` | `~/.claude/skills/tok-study-guide/` | Claude Code, Claude Agent SDK |
| Claude Code, this project only | `… install --target claude-project` | `./.claude/skills/tok-study-guide/` | Sharing the skill with a team via the repo |
| Any agent that reads AGENTS.md | `… install --target agents` | `./skills/tok-study-guide/` + a pointer block in `./AGENTS.md` | Codex, Cursor, Gemini CLI, OpenCode… |
| Any folder | `… install --dir <path>` | `<path>/tok-study-guide/` | Harnesses with their own skills folder |
| Claude.ai | `npx tok-study-guide-skill pack` | `dist/tok-study-guide.skill` | Upload in Claude.ai settings |

Use the same `--target` or `--dir` with `setup`, `doctor`, `uninstall` and `where`.

If your tool reads `CLAUDE.md` or another instructions file instead of `AGENTS.md`, copy the pointer block from `AGENTS.md` into it.

## Commands

| Command | What it does |
|---|---|
| `install` | Copies the skill into the target (`--force` to overwrite, `--link` to symlink while developing) |
| `setup` | Creates `<skill>/.venv`, installs the Python packages from `requirements.txt`, and downloads Chromium. Add `--with-deps` on Linux for Chromium's system libraries (needs sudo), or `--no-browser` to skip Chromium. |
| `doctor` | Checks Python, packages, Chromium, curl, git, poppler, uv and zip |
| `uninstall` | Removes the skill (and the AGENTS.md pointer for `--target agents`) |
| `where` | Prints the install path |
| `pack` | Builds `dist/tok-study-guide.skill` for Claude.ai |

## Requirements

- **Node.js 18+** (for the installer only; it has no npm dependencies)
- **Python 3.10+.** `setup` installs: `yt-dlp`, `curl_cffi`, `youtube-transcript-api`, `pillow`, `playwright`, `pypdf`
- **Command-line tools:** `curl` and `git`; `pdftoppm` from poppler (recommended, for PDF page previews); `uv` (recommended)

Linux / WSL:
```bash
sudo apt install curl git poppler-utils zip
curl -LsSf https://astral.sh/uv/install.sh | sh
```
macOS:
```bash
brew install poppler uv
```

## When YouTube blocks transcript access

The transcript fetcher tries several player clients and then an unauthenticated API fallback. If YouTube blocks this runtime, the safest fallback is to run the fetcher on the user's own machine and provide the generated transcript, or provide captions directly.

Browser cookies are bearer credentials that grant access to the signed-in account. **Never ask a user to upload, paste, email, or commit a logged-in cookie file.** Only use browser authentication when the user explicitly chooses it and the script is running on their trusted local machine. Prefer reading the local browser profile directly:

```bash
python3 skill/tok-study-guide/scripts/fetch_transcript.py "<url>" \
  --cookies-from-browser chrome
```

If using a local Netscape cookie file instead, keep it private (`chmod 600 <cookie-file>`), do not expose it to a hosted runtime, and remove or revoke it if it is disclosed. Cookie values are not logged. Choose either `--cookies` or `--cookies-from-browser`; do not use both. The unauthenticated API fallback does not receive browser cookies.

The script always verifies TLS certificates. If a network intercepts TLS, configure its trusted CA rather than disabling certificate checks. For a local automation environment, `YT_DLP_COOKIES`, `YT_DLP_COOKIES_FROM_BROWSER`, and `YT_DLP_PLAYER_CLIENT` can supply the corresponding options; keep these settings private.

## What's inside

```
skill/tok-study-guide/
├── SKILL.md                 # the workflow and writing rules the agent follows
├── requirements.txt         # Python packages for the scripts
├── scripts/
│   ├── fetch_transcript.py  # YouTube → transcript + timestamp cues; local auth options
│   ├── find_photos.py       # Openverse search → contact sheets → embedded, credited photos
│   ├── assemble.py          # template + body parts → one HTML file
│   ├── check_page.py        # mobile-overflow check + screenshots
│   └── make_pdf.py          # colorful A4 PDF via headless Chromium
├── assets/
│   ├── template_head.html   # design system: light/dark, code, outputs, warnings, photos
│   ├── template_foot.html   # lightweight scroll script
│   └── print.css            # cover, contents, one chapter per page
└── references/
    ├── components.md        # every HTML building block + SVG diagram cookbook
    ├── metaphors.md         # metaphor rules, concept→metaphor bank, photo search terms
    └── learning-design.md   # optional continuity records for multi-session courses
```

## Where the agent saves things

The skill always saves the finished HTML lesson to `./lesson-output/` by default and scratch files to `./lesson-work/`. It creates a PDF in the output folder only when explicitly requested. In the Claude.ai sandbox, outputs go to `/mnt/user-data/outputs/`. You can ask for a different folder in your prompt.

## Responsible use

- Lessons **paraphrase** video and article content and quote only short, attributed passages. Code from materials you supply is quoted with attribution.
- Photos must be **openly licensed** and credited. News or magazine photos are linked, not embedded.
- Diagrams are **original**. No logos, brand marks or copyrighted characters are drawn.
- YouTube sometimes rate-limits transcript downloads. The script retries several ways; if it still fails, provide a transcript or usable captions. Successful downloads include a timestamped cue sidecar for linking lessons to exact moments.

## Developing

```bash
git clone https://github.com/theAfricanQuant/tok-study-guide-skill
cd tok-study-guide-skill
node bin/cli.js install --link --force   # edits in skill/ take effect immediately
python3 -m unittest discover -s skill/tok-study-guide/tests -v
npm test                                 # installs into ./.test-install and runs doctor
npm run build:skill                      # dist/tok-study-guide.skill
```

Publish to npm with `npm publish` after updating `version` in `package.json`.

## License

MIT
