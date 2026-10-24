# Project workflow: choose a path, create a place to learn

Read this when a learner begins a new subject, skill, source-breakdown, or continuing study request.

## 1. Start with a short choice

If the learner's request does not already make it clear, ask in one concise prompt:

> What would you like to do: get a full breakdown of material, learn a particular topic or skill, or do both? Do you have material to include, such as a book, document, video, or link, or should we start without it?

Use the learner's message and attached material as answers when possible. Do not make them repeat information they already gave. A request such as “break this video down” selects the source-breakdown path; “teach me German grammar so I can form correct sentences” selects goal-focused learning; a request to understand a book and use its ideas selects both.

## 2. Create the project scaffold before beginning

Create a project for the request at `./learning-projects/<slug>/` by default, or at the learner's requested location. In Claude.ai, use `/mnt/user-data/outputs/learning-projects/<slug>/`. Never create the project inside the installed skill directory. Check for an existing project first; continue it when it clearly matches, and do not overwrite its files. Keep the original learner-provided files where they are unless the learner asks to copy or organize them. Add their original paths, links, and identifiers to `sources/SOURCE_INDEX.md` so the learner can place more material in that folder later.

Always create:

```text
learning-projects/<slug>/
├── PROJECT.md             # chosen path, goal or request, level, and current status
├── sources/
│   └── SOURCE_INDEX.md    # files, URLs, formats, access limits, and source anchors
└── work/                  # transcripts, extractions, source ledger, and learning map
```

Add only the folders needed for the selected path:

```text
├── breakdowns/             # full source-by-source or chapter-by-chapter guides
├── lessons/                # goal-focused teaching modules
├── practice/               # attempts, practice prompts, examples, and feedback
├── assessments/            # criteria, rubrics, answer keys, and results
├── progress/               # dated evidence and next learning step
└── research/               # external research and its citations, when used
```

A source-only request usually needs `breakdowns/`; a topic- or skill-focused project usually needs `lessons/`, `practice/`, `assessments/`, and `progress/`; a combined project gets the relevant folders from both paths. Add `research/` only when external research is used. Do not create empty folders for unused modes. Keep a copy of a provided file only when the environment makes that appropriate; never move or overwrite the original.

## 3. Source-breakdown path

Use this path when the learner wants to understand a supplied book, document, video, article, course, or repository, or asks for a full/long summary. Follow the source's chapters or natural sections. For videos, use meaningful sections and timestamp anchors; for articles, use headings; for code, use files or modules. Produce the established HTML guide with source claims anchored close to the relevant explanation. Default to a full chapter-by-chapter breakdown when the material has chapters and the learner asks for a full breakdown. Do not turn it into a deliberate-practice course unless the learner also names a skill or performance goal.

## 4. Goal-focused path

When the learner wants to learn a topic or skill, gather only the information needed to plan it. Ask for or infer:

- **Goal:** what they want to know, explain, produce, decide, or perform, and in what situation.
- **Starting point:** what they already know or can currently do. Use a brief, low-stakes baseline task when uncertain and suitable.
- **Success criteria:** how a correct or effective result will be judged; use a suitable standard, rubric, worked answer, coach, or observable outcome.
- **Constraints:** time, tools, access to feedback, safety, and practice opportunities when these change the plan.
- **Materials:** any books, documents, videos, examples, or links they want included.
- **Method preference:** whether they want to memorize something by heart, make it stick through durable recall, deliberately practise using or performing it, or combine these. If they are unsure, explain a suitable recommendation and let them choose.

A topic and a performance can require different evidence. For example, grammar learning may need a learner to recall a rule or inflection, retrieve it after a delay, and use it to form meaningful sentences. Assess recall and use separately when the learner wants both. Do not assume that memorizing a rule proves the learner can use it.

After the goal, starting point, and criteria are clear, sketch the sequence and start the first manageable unit in the interaction. Teach a small part, ask for an attempt, wait for the learner, assess and grade it against the agreed criteria, give specific feedback and a retry, then adjust the next step. Do not deliver a whole course before the learner has a chance to try, and do not mark a skill complete before the evidence meets its criteria. Save reusable lesson and practice materials when useful; the interaction is where the agent can assess the learner’s actual work.

## 5. Combined path

Use a full breakdown when the learner wants to understand the whole material, then select the relevant ideas and source anchors for the goal-focused practice sequence. If the learner only wants to achieve a goal with a source as support, teach the relevant parts rather than producing an unnecessary complete breakdown. Keep source-derived claims distinct from external research and from newly created examples.

## 6. Research and learner communication

For goal-focused learning, do a focused deep-research pass by default to check key claims or standards and find useful models or gaps. Tell the learner that outside sources will supplement or check their materials, and identify those additions in the lesson. If the subject is simple and stable or external sources add nothing meaningful, keep the check brief and say so. Use authoritative sources appropriate to the subject, cite claims, and note disagreements or uncertainty. For a source-only breakdown, preserve the source’s account; add outside checks when requested or needed to clarify a significant error, safety issue, or current fact. Record research notes and citations in `research/` when that folder is present.

## 7. Finish one project and open the next

Update progress only from an actual learner response or demonstrated task. Record the date, task, criteria, result, feedback, remaining gap, and next step in `progress/learning-record.md`. Never infer progress from silence, reading, or completing a page. When the learner meets the agreed criteria, summarize what the evidence shows and offer the next suitable subskill or topic. Ask what they want to work on next; create a separate project for a genuinely new topic so its sources and progress stay clear.
