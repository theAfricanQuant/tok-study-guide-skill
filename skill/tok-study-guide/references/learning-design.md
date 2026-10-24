# Learning design and method map

This is an internal design guide for making lessons teach, not just explain. It turns selected ideas from the learning and communication books into decisions that should be visible in the finished lesson. The lesson itself does not need to name these books unless the learner asks or they are lesson sources.

This is a selective toolkit, not a complete replacement for reading any book and not a checklist to apply in full. The method cards are self-contained for using the skill; the book files are not a runtime dependency. Chapter anchors record the source set used to distill this version, rather than claiming that every tip in each book is included. Choose methods because they support the lesson's finish line. Do not claim that an author or book endorses a specific generated example unless the source has been checked. Keep source evidence for lesson facts separate from this internal method lineage.

## Choose the learning emphasis with the learner

In the goal-focused path, learners may choose to memorize, retain, apply or perform, or combine these aims. Ask this only when their request does not make the priority clear. Respect a preference for memorization; explain what it will demonstrate and whether their larger goal also needs application or transfer.

- **Memorize a form, fact, sequence, or definition:** teach an accurate, compact representation; use cues, recall, and corrective feedback. A mnemonic or memory palace may help when the material has stable items or a spatial/order structure. Recommend it when it fits, present it as an option, and follow the learner’s choice. Do not use a memory palace as a default or as a substitute for checking recall.
- **Remember it later:** use retrieval after teaching, space return attempts, and check confidence against actual performance. Interleave related items only after the basic forms are understood.
- **Use or perform a skill:** set a task and standard, take a baseline, target a trainable gap, model a sound attempt, give focused practice and useful feedback, then retry and vary the conditions. Use the *Peak* card below to distinguish purposeful practice from deliberate practice in its stricter setting.
- **Combine aims:** plan each kind of evidence separately and connect them. For grammar, for example, the learner may recall a form or rule, retrieve it later from a cue, then use it to make new sentences. Score recall and sentence use as separate criteria; explain how one supports the other.

Do not insist that one method is always best. Recommend a combination when the stated finish line requires more than one ability, explain the reason plainly, and retain the learner's chosen emphasis.

## Teach, test, grade, and decide what comes next

Before practice, share the success criteria in language the learner can use. Choose criteria that reflect the task: a correct answer key for a calculation, a rubric for an explanation or written response, a language criterion for a conversation, a coach's standard for a physical skill, or a reliable domain standard. Do not invent a formal certification or imply a score is official.

Use a low-stakes baseline to find the starting point, not to label the learner. Teach one needed element, give a task that reveals it, and assess the learner's actual attempt against the stated criteria. Report what is correct, what evidence supports the score, the most important gap, and one useful correction or retry. Where recall and application are both goals, grade them separately. Never grade silence, confidence, time spent, or page completion as mastery.

Progression is criterion-based, not lesson-count-based. If evidence meets the agreed standard, update the learning record and move to the next dependency or a transfer task. If it does not, use the error to choose a smaller reteaching or practice target. Keep the result and feedback visible to the learner. After the agreed finish line is reached, summarize demonstrated abilities and invite the learner to choose another skill or topic.

A static HTML guide can provide answer keys, self-checks, rubrics, and a suggested progress-log format, but it cannot observe, grade, or track the learner by itself. Grade and record an attempt only when the learner supplies an answer, work sample, recording, or other usable evidence. Mark self-scoring in a page as a self-check, not as an agent-assigned grade.

### Choose the interaction rhythm and consolidate

Honor a learner’s request for **quiz-me** mode, explanation-first teaching, or a mix. In quiz-me mode, questions should build toward the stated finish line: give enough grounding for a fair first attempt, ask one meaningful question at a time, and respond to the learner’s actual answer. Explain the reason for a correction and choose a targeted retry or changed task only when the evidence calls for it. When the learner has demonstrated a subskill, move on instead of asking the same check again for reassurance. A sequence of short questions can be effective when it is building one connected idea; keep each exchange useful and make the overall path visible.

At a natural checkpoint, let the learner choose whether to continue, switch style, or consolidate. If the learner explicitly says they are tired, exhausted, or ready to stop, end new practice and prepare a concise HTML review note in the project’s `lessons/` folder. Consolidate the concepts, a useful worked example, the learner’s demonstrated work, corrections that helped, open gaps, and the next step or spaced-return cue. Never infer exhaustion from silence, brevity, or an incorrect answer. Keep routine progress-file updates unobtrusive; surface a progress summary when it helps the learner decide what to do next.

## 1. Make a short learning map before drafting

Create `$WORK_DIR/<slug>/learning-map.md` before writing the HTML parts. Keep it brief enough to guide the work. It is a planning aid, not part of the finished lesson.

Record:

- **Finish line:** one observable thing the learner will be able to explain, decide, calculate, build, write, say, or perform.
- **Starting point:** what the learner likely knows, what is uncertain, and any essential prerequisite.
- **Path:** for each major section, what it teaches, what it uses from the previous section, and what it unlocks next.
- **Method choice:** the method card(s) that help with this particular outcome, why they fit, and the exact part of the HTML where the learner will use them.
- **Evidence and limits:** source IDs and precise anchors for claims; distinguish source facts from the guide's examples, analogy, calculations, and interpretation.
- **Practice loop:** the learner's attempt, what feedback the page can give, and a retry or transfer task when useful.

A compact planning table works well:

| Section | Learner action or outcome | Builds on → unlocks | Method card and reason | Visible HTML evidence |
|---|---|---|---|---|
| … | … | … | … | e.g. a worked example, a question before its answer, feedback, and a related retry |

If a technique has no concrete place in the lesson, leave it out. If a lesson is very short, a few bullets can replace the table.

## 2. Distilled method cards

Use these cards as decision rules. Their “visible evidence” is how another skill user can tell the method shaped the lesson. A method may be present without naming its book in the learner-facing page.

### Make ideas clear and memorable — *Made to Stick*

The book file was not part of the local study-methods source set used for this version. This card is based on the Heath brothers’ official SUCCESs model sheet, not a full local review of the book. See the [official model sheet](https://heathbrothers.com/wp-content/uploads/resources/mts-made-to-stick-model.pdf). The six traits are options, not six required sections:

- **Simple:** identify the core message and remove detail that does not help the finish line. Simple means prioritized, not shallow.
- **Unexpected:** open a useful curiosity gap or reveal a mistaken expectation when that helps the learner notice a distinction. Do not use surprise as clickbait.
- **Concrete:** anchor an abstract idea in a real situation, named objects, values with units, a worked calculation, tested code, an original diagram, or a specific decision. Explain what the example shows and where its limits are. A metaphor alone is not evidence.
- **Credible:** show the source, calculation, test, example, or limitation that lets a reader judge a claim. A confident tone is not evidence.
- **Emotional / relevant:** make clear why the idea matters to a real person or goal without inventing stakes or manipulating the reader.
- **Story:** use a short case when its sequence lets the learner rehearse a decision, cause, consequence, or change. Do not add an anecdote that does no teaching work.

**Check:** can a reader state the lesson’s core point, picture at least one important idea, judge why it is believable, and see what to do with it? Use only the traits that genuinely help.

### Durable learning — *Make It Stick*

Source anchors in the study-methods set used for this skill version are *Make It Stick*, Chapters 1–5. The card distills retrieval practice, spacing, interleaving, generation, elaboration, and calibration. Select by purpose:

- **Retrieval:** after an idea has been taught, ask the learner to recall or apply it without the answer in view. Put the attempt first, then an explanation that teaches the reasoning.
- **Generation:** when the needed foundations are already in place, let learners predict or attempt a solution before showing a worked answer. Do not withhold an explanation of a genuinely new concept.
- **Elaboration:** ask learners to explain the idea in their own words, connect it to prior knowledge, or explain why an example works. “Add more words” is not elaboration.
- **Spacing:** plan a return after time has passed when durable learning matters. In a static HTML page, give a realistic cue or action plan; do not imply the page will remind or track the learner.
- **Interleaving:** teach the foundations first, then mix related examples when the learner needs to tell methods apart or choose between them. Do not randomly mix unfamiliar material.
- **Calibration:** compare confidence with an actual recall, solution, or performance and useful feedback. Never infer mastery from rereading, a revealed answer, or finishing the page.

### Targeted performance — *Peak*

Use this card when the learner's goal is to do something: solve, explain aloud, write, speak, build, decide, or perform. *Peak* separates three ideas:

- **Naive practice:** repeat a familiar activity without a specific improvement target or a change based on evidence. Repetition can build familiarity, but repetition alone does not show progress.
- **Purposeful practice:** pursue a clear, suitably challenging goal with focused effort, useful feedback, and a changed next attempt. The task should reveal a gap the learner can work on and stretch current ability by a manageable step. It need not make every attempt feel maximally difficult.
- **Deliberate practice, in the book's stricter sense:** purposeful practice in a developed field with established training methods and knowledgeable teachers or coaches who can choose and adapt exercises. Do not use the term as a synonym for hard work, a plan, or any repeated exercise. When the learner is self-directed or the field lacks such a training tradition, call the method purposeful practice informed by deliberate-practice principles.

The book also uses **mental representations**: learned internal models that help a performer notice meaningful patterns, choose actions, anticipate likely results, and judge an attempt. Strong practice develops both the performance and these models, so feedback and explanation should help the learner see why an attempt worked or failed, not only reveal a score. No fixed number of hours guarantees expertise.

For a self-directed practice plan, adapt this loop to the task:

1. **Set a performance target and criterion.** Name the action, its conditions, and what a successful attempt would show. “Get better at German” is too broad; “explain a grocery need in connected sentences, ask a follow-up, and clarify one reply” can be checked.
2. **Take a baseline.** Try a representative task before reviewing the answer or model. Save the attempt, score, recording, or error notes when useful.
3. **Find the current bottleneck.** Look for the first important breakdown, not every imperfection. Choose a subskill small enough to practice and relevant to the finish line.
4. **Use a sound model or standard.** Prefer an effective teacher, coach, worked example, answer key, rubric, recording, or tested reference. A knowledgeable coach can detect and sequence work on errors that a beginner may not notice.
5. **Practice, inspect, and retry.** Keep attention on the target, get timely and specific feedback, correct one priority gap, and try again. Adjust support and challenge from what the learner actually did.
6. **Vary and reconnect.** When the isolated part becomes more reliable, change one relevant condition and return it to the whole task. A memorized script or one copied example is not evidence of transfer.
7. **Check again later.** Repeat a comparable task after a delay to test whether the ability is available without the original cues.

These steps are a practical design synthesis, not a claim that every skill follows one identical training protocol. For safety-critical or technically demanding performance, use qualified guidance and safe practice conditions. A static HTML page cannot observe a learner; it can provide a model, criterion, self-check, and next practice task, but must not claim the learner demonstrated the skill. If a learner submits an attempt in chat, respond to that evidence and choose one useful next correction. Source anchors in *Peak*: Chapter 1, PDF pp. 44–52 (printed pp. 14–22), for purposeful practice; Chapter 3, PDF pp. 80–113 (printed pp. 50–83), for mental representations; Chapter 4, PDF pp. 114–144 (printed pp. 84–114), for the stricter definition; Chapter 6, PDF pp. 175–190 (printed pp. 145–160), for everyday practice and Benjamin Franklin's model-based writing practice.

### Build usable understanding — *A Mind for Numbers*

For mathematics, science, and other cumulative material, help learners form a usable chunk rather than memorize disconnected steps. Source anchors in *A Mind for Numbers* are Chapters 2 (focused and diffuse thinking), 4 (chunking), 8 (tools and practice), and 10–11 (memory):

1. Name the central idea and the conditions under which it applies.
2. Work one example slowly, showing why each step follows.
3. Ask the learner to solve a related example with less support.
4. Compare it with a nearby case so they can recognize when the method does and does not apply.
5. Include a brief recall or synthesis after the worked explanation.

For longer study, a short planned break or a change of task can help when someone is stuck. Treat this as a study option, not a guaranteed brain mechanism or a universal timer.

### Preview and manage the study session — *Learning How to Learn*

When the source is long or visually structured, preview headings, figures, captions, and questions before close study; then return to the parts that support the goal. For procrastination or a study plan, make the first action small and concrete and let the learner choose a workable session length. Use mixed practice only after basic methods are understood. Avoid prescribing one routine, break interval, or “learning style” as right for everyone. Source anchors in *Learning How to Learn* are Chapters 3–4 and 7–9 for procrastination, brain-links, attention, memory, and self-questioning.

### A practical learner toolkit — *Learn Like a Pro*

Use the book’s broad toolkit selectively: help learners get unstuck by changing representation or taking a short break; manage working-memory demands with clear notes and chunks; use active recall and spaced review for remembering; and turn reading into questions or an explanation rather than copying passages. Prefer an action a learner can check over generic advice like “study harder.” Source anchors in *Learn Like a Pro* are Chapters 2–5 and 9–11: getting unstuck, deep learning, working memory, memorization, reading, tests, and the final learner checklist.

### Transfer and motivation — *Mindshift*

When context makes it relevant, connect a learner’s past knowledge or experience to the new skill and identify what transfers and what must be relearned. Frame motivation around a meaningful next use or a feasible first step; do not assume a learner must already feel passionate, be young, or follow one career path. This card is mainly useful for continuing courses and career or cross-domain learning, not every one-off guide. Source anchors in *Mindshift* are Chapters 4–5 and 8: past experience, nontraditional learning, and career paths.

### Teach concepts and procedures — *Uncommon Sense Teaching*

Check whether the learner needs to **know what** a concept means, **know how** to use it, or both. Explain concepts in manageable pieces, then give the learner an active task; for a procedure, model it and let the learner perform it. Consider prior knowledge and working-memory load when deciding what to introduce together. Use peer explanation or collaborative tasks only when the subject and format support them. A static page cannot observe a class or provide individualized teacher feedback, so do not imply that it did. Source anchors in *Uncommon Sense Teaching* are Chapters 1–3, 6, and 10: memory, working-memory capacity, declarative and procedural active learning, and lesson planning.

## 3. Connect every section to the finish line

A connected lesson should read as one path, not as a set of mini-essays:

1. **Orient:** state the practical mission, why it matters, what the learner may need first, and what the sources contribute.
2. **Build:** introduce prerequisite ideas in order. Define notation and terms before using them. Say how each idea depends on the previous one and what it makes possible next.
3. **Make it concrete:** show the important idea in a worked example, source case, actual value, original diagram, code result, or specific situation. Explain what the representation means; do not assume an image or analogy explains itself.
4. **Model and practise:** show key choices where there is a procedure. Ask for an attempt before feedback when the learner has enough grounding to try.
5. **Interpret and transfer:** explain what the result means, its assumptions and limits, and how the learner can use it in a different but relevant situation.
6. **Return and remember:** use a focused self-check and a later retrieval cue when the goal benefits from them. End with a next action that supports the same finish line.

The opening and final activity should point toward the same practical goal. A reader should be able to answer: “What is this for?”, “Why does this example make the idea clearer?”, and “How does this part prepare me for the next part?”

## 4. Match practice to the intended performance, not the source format

A PDF, video, slide deck, article, podcast, and code repository are ways information arrives. None determines the practice method by itself. A PDF can teach a concept or a procedure; a video can explain an idea or demonstrate a movement. First identify the learner's intended action and standard of success. Then let the source supply the examples, evidence, models, and feedback needed for that action. If a lesson has several finish lines, give each important ability a fitting practice task rather than forcing one generic exercise to cover everything.

| Learner needs to… | Practice that makes the ability visible |
|---|---|
| **Remember facts or terms** | Retrieve from memory without the answer in view, check omissions or confusions, and return after a delay. Use examples that distinguish easily confused terms. |
| **Understand or explain a concept** | Explain the relationship in their own words, compare a nearby concept or counterexample, and apply the explanation to a new case. Ask for the reasoning, not just a label. |
| **Solve problems or use a procedure** | Study one worked example, predict or perform the next step, try a related problem with less support, inspect the first point of error, then use a changed problem. For code, predict, run, inspect real output, modify, and debug. |
| **Speak or understand a language** | Combine comprehension and production around a communicative goal. Retrieve words from intent cues, listen to a manageable reply, respond or request clarification, then vary one detail. Include pronunciation only to the extent it serves the learner's stated goal and intelligibility. |
| **Write or create** | Study a short model for one feature, produce an original attempt, compare against a criterion or informed reader's feedback, revise one feature, and try that feature on a fresh prompt. |
| **Perform a physical or musical skill** | Use a safe demonstration, isolate a manageable part, repeat with a precise cue and observable feedback, then reconnect it to the whole performance. Use a qualified coach for hidden technique, high risk, or demands beyond self-observation. |
| **Judge evidence or make an argument** | Separate source claim, evidence, and interpretation; evaluate the support; build a conclusion; then test it against a counterexample or a new source. Preserve disagreement between sources instead of blending it away. |

The source format still affects *how to inspect and cite the material*: listen to a timestamped audio segment, inspect a figure or slide, run code, or anchor a PDF claim to a page. That is source handling, not necessarily the learner's practice. For example, repeatedly playing a language tape may help recognition, but if the goal is to form a spoken request, pause it and produce the request from an intention cue, then handle a reply. Benjamin Franklin's practice in *Peak* followed this principle: he studied a model, recreated it from short cues after the wording had faded, and compared his version with the source. The useful transfer is retrieval, comparison, correction, and recombination—not copying Franklin's exact writing exercise for every subject.

For languages, identify which CEFR level or communicative situation the learner is targeting when known. A routine exchange can be a useful lower-level task; a higher target may require connected points, reasons, follow-up questions, understanding a reply, and repair. Do not imply that one dialogue, page, or correct sentence proves a whole proficiency level. A text-only lesson can prescribe speaking and listening work, but cannot claim to have heard or assessed it.

Adjust support for age, experience, and context without assuming one fixed learner type. Let learners help choose meaningful targets; make first steps and feedback specific; fit practice around real time, access, rest, and safety. For children and teenagers, use age-appropriate language and support while still respecting their agency. For adults, connect the goal to a relevant use and account for work or family commitments. Do not infer ability, motivation, or a suitable schedule from age alone.

## 5. Review the actual HTML against the learning map

After assembly, check the page itself:

- Is there one clear, achievable finish line?
- Can the reader see how the sections build from first to last?
- Is each selected method visible in a useful action, example, question, feedback, or plan?
- Does each important abstract idea have a concrete representation and an explanation of what it demonstrates?
- Is practice appropriate to the goal, with feedback before or alongside the answer, and a retry or transfer when useful?
- Are citations close to source-derived claims, while guide-created examples and interpretations remain distinguishable?
- Does the closing task or action return to the opening finish line?
- Did any technique become decorative, misleading, inaccessible, or unnecessary? Remove it.

The map should show the intended method-to-page connection. The finished HTML must still stand on its own for someone who has never read the source books or this internal map.

## 6. Keep continuity records only when useful

Use the project folders from `references/project-workflow.md` for an ongoing learning sequence:

- `PROJECT.md`: requested path, learning goal or breakdown scope, starting level if known, constraints, success criteria, and current status.
- `sources/SOURCE_INDEX.md`: source IDs, title/type/link, useful page/time/slide/file anchors, each source's contribution, conflicts, and inaccessible portions.
- `work/NOTES.md`: concise concept explanations, worked examples, and links back to source anchors.
- `progress/learning-record.md`: dated attempts, criteria, results, demonstrated knowledge or skill, misconceptions corrected, remaining gaps, and next step.

Create only files relevant to the chosen path. Start with available files and update records only when the learner provides new evidence. Do not treat silence, a guessed answer, or an unattempted exercise as proof of mastery. Keep records short so they make the next session more tailored instead of becoming a transcript.
