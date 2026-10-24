# tok-study-guide-skill

The name **TOK** draws on the Berom verb *tɔk*, “to know; to understand; to know how to” (p. 162). It is a verb, not a noun meaning “knowledge” or “ability.” The dictionary separately lists *tɔk tsik* (“understanding”; p. 162, finderlist p. 243) and *tɔk ciwil* (“intelligence”; p. 162, finderlist p. 213). For “cleverness; skill; wisdom,” it lists *nèsisɛng* (p. 116), with *nètsitsɛng* as a synonym.

The Berom are an Indigenous people of Plateau State in north-central Nigeria, living mainly around the Jos Plateau, including Jos North, Jos South, Barkin Ladi, and Riyom ([Jos South LGA](https://jossouthlga.pl.gov.ng/ova_por/berom-art-and-culture-museum/)).

An agent skill for two kinds of learning work:

1. **Understand material:** get a full chapter-by-chapter or section-by-section breakdown of a book, document, video, course, or other source.
2. **Learn a topic or skill:** work toward a specific learning goal with teaching, focused practice, assessment, feedback, and progress records.

The learner can choose either path or combine them. When they launch the skill, it identifies the path and asks whether they have materials to use. The skill creates a suitable project folder before work begins. A source breakdown follows the source; a goal-focused course follows the learner's target. If they ask for both, the relevant ideas in the source support practice toward the target.

**Defaults:** clear Grade 12 English; chapter-by-chapter guides in HTML; metaphors only when requested; PDF only on request. In goal-focused learning, the learner can emphasize memorization, durable recall, performance, or a combination, and choose explanation-first, quiz-me, or mixed teaching. Quiz questions build toward the goal and adapt to actual answers. When a learner says they are tired or ready to stop, the skill consolidates the session into a concise HTML review note and records progress only from demonstrated work.

For goal-focused learning, the skill does a focused deep-research pass to check key claims or standards and add useful models or missing context. It tells the learner when it is adding outside sources, cites them, and distinguishes them from the learner's material. A source-only breakdown stays with the supplied source unless an outside check is requested or needed to clarify a significant error, safety issue, or current fact.

It works with **Claude Code**, the **Claude Agent SDK**, **Claude.ai**, and any agent that can read a `SKILL.md` file or an `AGENTS.md` pointer (Codex, Cursor, Gemini CLI, OpenCode, and others).

### Example requests

> Give me a full chapter-by-chapter breakdown of this book.

> I want to learn German grocery conversations. I know some basic grammar. Help me remember useful forms and practise using them; assess my attempts against clear criteria.

> Break down this video, then use its method to build and assess a practice plan for my presentation skills.

### Project folders

Each request gets a project under `./learning-projects/<slug>/` by default. The skill creates a source index and work folder, then adds folders for the selected path:

```text
learning-projects/<slug>/
├── PROJECT.md
├── sources/                 # source index and a place for materials
├── work/                    # transcripts, notes, and planning maps
├── breakdowns/              # when the source-breakdown path is used
├── lessons/                 # when the goal-focused path is used
├── practice/                # goal-focused attempts and feedback
├── assessments/             # goal-focused criteria, rubrics, results
├── progress/                # goal-focused dated learning evidence
└── research/                # only when outside research is added
```

Only create folders needed for the selected path. The skill records the original locations of supplied files; it does not move or overwrite them. A source-only request usually needs `breakdowns/`; a goal-focused request needs `lessons/`, `practice/`, `assessments/`, and `progress/`. Goal-focused teaching proceeds in manageable steps: the agent teaches, waits for an attempt, assesses against stated criteria, gives feedback, and adapts. Learners may choose explanation-first, quiz-me, or mixed interaction. When they signal that they are ready to stop, the agent consolidates the session in a review note. A combined request uses both paths. See [`project-workflow.md`](skill/tok-study-guide/references/project-workflow.md) for the full intake and folder rules and [`learning-design.md`](skill/tok-study-guide/references/learning-design.md) for method choices, assessment, and progress tracking.

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

Then try a request such as:

> Give me a full chapter-by-chapter breakdown of this book.

Or:

> I want to learn a specific skill. Ask what you need to know, set up a project folder, and help me practise and assess it.

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

Windows users: We recommend using [WSL 2 with Ubuntu](https://learn.microsoft.com/en-us/windows/wsl/install) to install and run the skill. Install and use Node.js, Python, and `uv` inside WSL, and run the skill commands from the WSL shell so the tools share one Linux environment.

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

A Netscape cookie file can contain session cookies for multiple sites. Prefer the browser-profile option; if you use a local cookie file, restrict it (`chmod 600 <cookie-file>` on Linux/macOS), delete it after use, and revoke the YouTube session if the file is disclosed. Cookie values are not logged. Choose either `--cookies` or `--cookies-from-browser`; do not use both. The unauthenticated API fallback does not receive browser cookies.

On a network where the default client is blocked, alternate clients can be tried explicitly with `--player-client tv --player-client mweb`. The script always verifies TLS certificates. If a network intercepts TLS, configure its trusted CA rather than disabling certificate checks. For a trusted local automation environment, `YT_DLP_COOKIES`, `YT_DLP_COOKIES_FROM_BROWSER`, and `YT_DLP_PLAYER_CLIENT` can supply the corresponding options; never configure authenticated cookies in a hosted runtime.

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
    ├── metaphors.md         # optional metaphor guidance and examples
    ├── project-workflow.md  # intake paths, project folders, and progress handoff
    └── learning-design.md   # learning-method choices, teaching, assessment, and progress
```

## Where the agent saves things

The skill creates each learning project in `./learning-projects/<slug>/` by default and keeps work files under that project. HTML guides go in `breakdowns/` for source-led work or `lessons/` for goal-focused work. A PDF is added only when requested. Claude.ai projects default to `/mnt/user-data/outputs/learning-projects/<slug>/`. You can request a different folder.

## Responsible use

- Lessons **paraphrase** video and article content and quote only short, attributed passages. Code from materials you supply is quoted with attribution.
- Photos are used only when they help explain the source or a learner-requested metaphor. Embedded photos must be **openly licensed** and credited; news or magazine photos are linked, not embedded.
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
