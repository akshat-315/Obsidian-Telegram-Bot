# Obsidian Workflow Bot — Product Design Document

## Philosophy

The bot is a **peer with perfect memory** — not a teacher, not a tool. It knows everything you've ever thought about and casually brings up the right thing at the right time. You never "study." You just have a conversation.

### Core Constraints

1. **No added friction** — If it feels like homework, you'll mute it in 3 days
2. **No AI-generated content** — AI writes for you = surface-level knowledge. You must do the thinking and writing. Your words, always.
3. **AI for search and matching, never for generation** — Embeddings, similarity scores, scheduling = math. The bot is a librarian with perfect memory, not a conversationalist trying to be smart.
4. **Notes are a byproduct of conversation** — You never "sit down to write." You reply to a message. The reply becomes a note.
5. **The bot comes to you** — You never open an app to study. It arrives in Telegram, in the flow of your day.

---

## The Problem We're Solving

Most knowledge vaults become **write-only graveyards**. Notes go in, nothing comes out. People ghost their vaults because:

- Writing a "note" feels like a commitment (mental overhead kills it)
- Work consumes all bandwidth — no time for "extra" reading/writing
- No system brings old knowledge back to the surface
- Knowledge decays silently — you don't notice what you've forgotten

---

## Features

### 1. Resurface (Core — Build First)

Send the user their own note at the right interval. Their words. Zero generation. Just a database query + a timer.

**How it works:**
- Bot sends **just the title** of the note
- User naturally tries to remember what they wrote (involuntary recall — the 2-second gap IS the retrieval practice)
- User taps/replies to see the full note
- No quiz. No grading. No pressure.

**Scheduling (Simplified Leitner + Cepeda's research):**
- First review: **1 day** after writing
- If user engages: **3 days → 7 days → 21 days → 60 days → 180 days**
- If user doesn't engage: stays in the short interval pool
- Signal is implicit — did they open it or not. No "easy/hard" buttons.

**Anti-Anki Rules:**
- **Zero backlog, ever.** Miss 5 days → come back to zero pending, not 50. Missed reviews reschedule silently.
- **One note per day to start.** BJ Fogg: start absurdly small. The habit locks in before the volume increases.
- **Interleave topics.** Never two notes from the same topic back-to-back. Mixing = 43% better retention (Rohrer & Taylor, 2007).
- **Lenient streaks.** Miss a day → streak doesn't break. Miss a week → streak pauses. Bot never guilt-trips. Ever.
- **Cap daily reviews.** Ceiling prevents overwhelm.

**Why this is the first feature to build:**
- Solves knowledge retention AND engagement in one feature
- The resurfacing message IS the trigger for new notes (you re-read → you think "oh actually..." → new note)
- Self-sustaining loop: resurface → re-engage → new thought → capture → resurface

---

### 2. Daily Prompt (Static, No AI)

A fixed rotating bank of questions. Hardcoded, curated. Can't hallucinate.

**Example prompts:**
- "What did you figure out today?"
- "What problem did you solve today?"
- "What changed your mind recently?"
- "What's something you'd explain differently now than a month ago?"
- "What surprised you today?"
- "What's something you're stuck on?"
- 20-30 of these, rotating.

**Why it works:**
- Your work IS the content. You just need the trigger to extract it.
- Fogg's model: the prompt arrives when motivation + ability already exist
- You reply in 15 seconds between tasks. Reply becomes a note. Zero extra time.

---

### 3. Connection Nudges (Embeddings, No Generation)

When a new note comes in, compute embedding similarity against existing vault.

- If similarity score is high → reply: "This might relate to: [[note title]]"
- Shows **user's own note titles**, not generated text
- Worst case: irrelevant nudge. Never a hallucination.
- User decides if the connection is real. They write the link if they want.

**The dot-connecting is deterministic math. The meaning-making is human.**

---

### 4. Content Curation (User's Sources, Not AI)

User subscribes to RSS feeds, YouTube channels, newsletters they trust.

- Bot forwards items from their sources
- No AI summary. No rewriting. Just delivery.
- Arrives in Telegram between other messages — ambient exposure
- If it sparks a thought, user replies → new note

---

### 5. Gap Illumination (Pure Data Analysis)

Monthly analysis of vault topic clusters.

- "You have 15 notes on investing, 0 on risk management."
- "You haven't written about [topic] in 3 months."
- Pure counting and clustering. No interpretation.
- Makes blind spots visible. User fills them or ignores them.

---

## The Daily Loop

```
Morning (or whenever user is active on Telegram):

Bot sends → Note title only (resurface)
       ↓
User recalls → (2 seconds, involuntary)
       ↓
User taps/replies → Full note revealed
       ↓
Optionally → User drops a new thought triggered by re-reading
       ↓
Bot saves new note → Schedules for future resurfacing
       ↓
Evening → Daily prompt: "What did you figure out today?"
       ↓
User replies in one sentence → New note created
       ↓
Cycle sustains itself
```

---

## The Dashboard: A Mirror of Your Mind

The bot is the daily interface (pocket, conversational, low-friction).
The dashboard is the reflective interface (weekly/monthly, visual, big-picture).
One feeds the other. Neither is complete alone.

### Knowledge Graph (Centerpiece)

Visual node graph:
- **Each node** = a topic cluster derived from notes
- **Node size** = depth (number of notes, connections)
- **Node color** = retention health:
  - Green = recently engaged, strong
  - Amber = fading (hasn't been resurfaced/engaged in a while)
  - Red = gone cold (months without engagement)
- **Edges** = connections between topics (from explicit links + embedding similarity)
- **Empty space** = gaps you haven't explored

You literally see the shape of your knowledge. Where you're deep, where you're shallow, what's decaying.

### Retention Health Score

A single number: "You can likely recall ~72% of your vault right now."

Based on spacing data — which notes you've engaged with recently vs. which have gone cold. Computed from the Ebbinghaus forgetting curve applied to each note's last engagement date.

### Topic Heatmap Over Time

GitHub-contributions-style grid but for topics. Shows what you were thinking about each week/month. Your intellectual seasons visualized.

### Fading Knowledge

List of notes/topics that are slipping away based on spacing intervals.
Not a guilt-trip: "These 5 ideas are fading. Any worth revisiting?"
User picks, or lets them go. Not everything needs to be retained forever.

### Growth Trajectory

- New topics explored vs. existing topics deepened over time
- Broad exploration vs. deep focus — neither is wrong, but seeing the pattern is valuable

### Connection Density

How interconnected is your thinking? Isolated islands vs. a web?
Watching connections grow over time is inherently satisfying and meaningful.

### Belief Evolution Timeline

Click on any topic → see your earliest note vs. latest note → how your understanding evolved. A timeline of your own intellectual growth.

---

## What We Avoid (Anti-Patterns)

### From Anki's Failures
| Anki Problem | Our Solution |
|---|---|
| Backlog guilt spiral | Zero backlog — missed reviews reschedule silently |
| Leech cards drain time | No grading — if a note never gets engagement, it quietly fades out |
| Feels like homework | Title-first reveal feels like a message, not a flashcard |
| All-or-nothing streaks | Lenient streaks with auto-freeze |
| Requires dedicated study time | Arrives in Telegram, 30 seconds in existing flow |
| Users must rate difficulty | Engagement signal is implicit — did you open it or not |
| 200-page manual | Zero setup beyond "send a message" |

### From AI Hallucination Risk
| Risky Approach | Our Approach |
|---|---|
| AI generates questions about notes | Static prompt bank, no generation |
| AI summarizes articles | Forward from user's RSS feeds, no summary |
| AI writes provocations/counter-examples | Show related notes (embedding math), user connects |
| AI auto-categorizes | Tag-based clustering, user's own tags |

---

## Technical Architecture (High-Level)

### New Components Needed

| Component | Purpose | Tech |
|---|---|---|
| Note metadata store | Track creation date, review dates, engagement, intervals, tags | PostgreSQL or SQLite |
| Embedding service | Generate + store note embeddings for similarity | OpenAI embeddings + pgvector / Chroma |
| Scheduler | Manage resurface timing, daily prompts | APScheduler (in FastAPI) or cron |
| Dashboard frontend | Knowledge graph, heatmap, metrics | Web app (React / Next.js / plain HTML) |
| RSS ingestion | Pull from user-configured feeds | feedparser + background task |

### Data Model (Core)

```
Note:
  - id
  - title
  - content
  - created_at
  - tags[]
  - embedding (vector)
  - github_path

ReviewSchedule:
  - note_id
  - next_review_at
  - interval_days (current interval)
  - times_engaged (count)
  - last_engaged_at
  - leitner_box (1-6)

DailyPrompt:
  - id
  - prompt_text
  - last_sent_at

UserSettings:
  - review_time (when to send resurface)
  - max_daily_reviews
  - streak_count
  - streak_freeze_available
```

---

## Build Order

1. **Resurface engine** — Scheduling, title-first reveal, implicit engagement tracking, zero backlog
2. **Daily prompts** — Static bank, evening delivery, reply-to-note capture
3. **Connection nudges** — Embedding pipeline, similarity matching on new notes
4. **Dashboard v1** — Knowledge graph, retention score, topic heatmap
5. **Gap illumination** — Topic clustering, monthly report
6. **Content curation** — RSS integration, source management

---

## Science Foundation

See [RESEARCH.md](./RESEARCH.md) for complete citations and findings. Key numbers:

- **Forgetting curve**: 67% lost within 24 hours without review (Ebbinghaus)
- **Active recall**: 400% improvement over re-reading (Roediger & Karpicke, 2006)
- **Interleaving**: 43% better retention on delayed tests (Rohrer & Taylor, 2007)
- **Tiny habits**: 2.7x more likely to stick when starting small (Fogg)
- **Lenient streaks**: 3.6x engagement at 7-day mark (Duolingo data)
- **Optimal spacing**: 10-20% of desired retention period (Cepeda & Pashler, 2008)
- **80% of Anki users quit** — primarily due to backlogs and all-or-nothing psychology
