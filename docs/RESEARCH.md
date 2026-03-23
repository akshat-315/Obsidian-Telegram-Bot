# Deep Research: Science of Learning, Memory, and Habit Formation
## For Telegram Bot Note-Resurfacing System

---

## 1. Spaced Repetition Science

### The Forgetting Curve (Ebbinghaus, 1885)

**Original Experiment:** Hermann Ebbinghaus tested himself on nonsense syllables (CVCs like "WID", "ZOF") from 1880-1885, measuring "savings" — how much less time it took to relearn a list after a delay.

**Exact retention percentages from Ebbinghaus's data:**
| Time After Learning | Retention |
|---|---|
| 20 minutes | 58% |
| 1 hour | 44% |
| 24 hours | 33% |
| 1 week | 25% |
| 1 month | 21% |

**Mathematical formula (Ebbinghaus's original):**
```
Q(t) = 1.84 / ((log10(t))^1.25 + 1.84)
```
This is a **power function**, not exponential.

**Modern simplified formula:**
```
R = e^(-t/S)
```
Where R = retrievability, t = time elapsed, S = memory stability.

**Key insight:** Forgetting is initially rapid then slows dramatically. The steepest drop is in the first 24 hours. After that, the curve flattens — what you still remember after a week, you'll mostly still remember after a month.

**Important caveat:** When memories of different complexity are mixed, the forgetting curve changes shape and may be better approximated with a negative power function (as Ebbinghaus originally found). Pure exponential decay applies to single-complexity memories.

### Wozniak's Two-Component Model of Memory (1995)

Piotr Wozniak, with Gorzelanczyk and Murakowski, proposed that long-term memory has two independent components:

1. **Stability (S):** How deeply embedded a memory is. Determines how long before retrievability drops to zero. Increases with well-timed repetitions.
2. **Retrievability (R):** How easily a memory can be accessed right now. Fluctuates based on recency of exposure.

**Critical property:** Repetitions have NO power to increase stability when retrievability is high (this IS the spacing effect). You must wait until retrievability drops before reviewing — reviewing too early is wasted effort.

### Algorithm SM-2 (Wozniak, 1987)

The foundational algorithm used by Anki, Mnemosyne, and many other SRS tools.

**Exact algorithm:**
```
Intervals:
  I(1) = 1 day
  I(2) = 6 days
  I(n) = I(n-1) × EF   (for n > 2)

Easiness Factor update:
  EF' = EF + (0.1 - (5 - q) × (0.08 + (5 - q) × 0.02))
  Minimum EF = 1.3
  Initial EF = 2.5

Grade scale (0-5):
  5 = perfect response
  4 = correct after hesitation
  3 = correct with serious difficulty
  2 = incorrect, but correct answer seemed easy
  1 = incorrect, correct answer remembered
  0 = complete blackout

Rules:
  - If grade < 3: restart from I(1)
  - Continue session until all items score >= 4
```

**What this means in practice (EF = 2.5):**
- Review 1: 1 day after learning
- Review 2: 6 days after Review 1
- Review 3: 15 days after Review 2
- Review 4: 38 days after Review 3
- Review 5: 94 days after Review 4

### Algorithm SM-18 (Wozniak, 2019)

Latest SuperMemo version. Key difference from SM-2: **item difficulty is no longer assumed to be constant** — it changes over time based on the two-component memory model. SM-18 introduced the "stabilization curve." The algorithm is proprietary.

### FSRS (Free Spaced Repetition Scheduler)

Open-source algorithm created by Jarrett Ye, now default in Anki. Based on the **DSR (Difficulty, Stability, Retrievability) three-component model.**

**Three components:**
- **Retrievability (R):** Probability of recall, range [0, 1]
- **Stability (S):** Days for R to decay from 1.0 to 0.9
- **Difficulty (D):** Inherent complexity, range [1, 10]

**Core equations:**
```
Forgetting curve:  R(t, S) = (1 + F × (t/S))^C
Interval:          I = S / (1 - DR)^(1/w20)
                   (When desired retention = 90%, interval = stability)

Initial difficulty: D₀ = w4 - (G - 3) × w3  (clamped to [1, 10])
Stability update:   S' = S × SInc
  where SInc = f(D) × f(S) × f(R)
  f(D) = (11 - D) / 10
```

**21 parameters** optimized per-user via machine learning on review history.

**Benchmark results vs SM-2:**
- **20-30% fewer reviews** for the same retention rate
- Default parameters trained on ~700 million reviews from 20,000 users
- Personalized parameters further improve performance

### Leitner System (1970s)

Sebastian Leitner's physical box method:
- All cards start in Box 1 (review daily)
- Correct → move to next box (longer intervals)
- Incorrect → back to Box 1
- Typical intervals: Box 1 = daily, Box 2 = every 2 days, Box 3 = every 4 days, Box 4 = every 8 days, Box 5 = every 16 days

**Advantage:** Simple, no algorithm needed. Forces focus on hardest material.

### Optimal Spacing Intervals (Research Consensus)

**Wozniak's recommendation:** Day 1 → Day 7 → Day 23 → Day 58

**Cepeda, Pashler et al. (2008) — landmark study with 1,350+ participants:**
- Optimal spacing gap depends on how long you need to remember
- For a 1-week test: optimal gap = 20-40% of delay (1-3 days)
- For a 1-year test: optimal gap = 5-10% of delay (18-36 days)
- **Too little spacing AND too much spacing both hurt retention**

**Pimsleur's graduated intervals:** 5s → 25s → 2min → 10min → 1hr → 5hr → 1day → 5days → 25days → 4months → 2years

**Practical consensus schedule:** 1 day → 3 days → 7 days → 14 days → 30 days → 90 days → 180 days

### What's Popular But Wrong
- **Fixed schedules are suboptimal.** Adaptive algorithms that respond to performance outperform any fixed interval schedule.
- **Reviewing too early is wasted effort.** Wozniak's key insight: repetitions cannot increase stability when retrievability is still high.
- **"Just review everything daily" is counterproductive.** It violates the spacing effect and leads to burnout without improving retention.

### Application to Telegram Bot
- First resurface a note 1 day after creation
- Second resurface at ~3-7 days
- Third at ~2-4 weeks
- Use a simplified Leitner-like system: if user engages well, extend interval; if user struggles or doesn't engage, shorten interval
- Don't resurface notes whose retrievability is still high — it wastes the user's attention
- FSRS-style adaptive scheduling is ideal but complex; a simplified version with 4-5 interval buckets would capture most of the value

---

## 2. Active Recall vs Passive Review

### The Testing Effect (Roediger & Karpicke, 2006)

**Landmark study:** Students studied prose passages, then either took free-recall tests or restudied. Results:
- After 5 minutes: restudying group performed BETTER
- After 2 days: testing group performed significantly BETTER
- After 1 week: testing group recalled **61%** vs restudying group's **40%** — a 21 percentage point advantage

**Key finding:** Practicing retrieval ONE TIME doubled long-term retention. REPEATED retrieval produced a **400% improvement** in retention.

### Why Passive Rereading Fails

**Dunlosky et al. (2013)** — comprehensive review of 10 study techniques:

**HIGH utility (actually work):**
- Practice testing (retrieval practice)
- Distributed/spaced practice

**MODERATE utility:**
- Elaborative interrogation
- Self-explanation
- Interleaved practice

**LOW utility (popular but ineffective):**
- Summarization
- Highlighting
- Keyword mnemonic
- Imagery for text learning
- **Rereading**

### The Illusion of Competence / Fluency Illusion

Rereading creates a sense of **processing fluency** — the text feels familiar, so students believe they know it. This is false confidence. Bjork, Dunlosky, and Kornell documented this extensively:

- Students confuse **recognition** (I've seen this before) with **recall** (I can produce this from memory)
- Rereading always "feels successful" because the material is present — unlike self-testing, which reveals gaps
- Students who reread rate their learning higher but perform worse on delayed tests

### Is Passive Rereading Completely Useless?

Not completely, but nearly:
- It provides marginal benefit for **recognition tasks** (multiple choice) but almost none for **recall tasks** (free response)
- Rereading is only beneficial when spaced out over time (but at that point, you're using spacing, not rereading)
- It's a **terrible use of time** compared to active alternatives — same time spent on retrieval practice yields dramatically better results

### Application to Telegram Bot
- **Never just re-show a note passively.** Always include a prompt that requires the user to think before revealing content.
- Possible prompts: "What do you remember about [topic]?" or "What was the key idea from your note on [topic]?"
- Show the note AFTER the user has attempted recall (even mentally)
- Even a simple "Tap to reveal" creates a micro-moment of retrieval attempt
- The bot should ask questions ABOUT the note content, not just display it

---

## 3. Habit Formation Science

### BJ Fogg's Behavior Model (Stanford)

**Core equation:** B = MAP (Behavior = Motivation × Ability × Prompt)

All three must be present simultaneously for a behavior to occur.

**Three types of prompts:**
1. **Spark:** Raises motivation (highlights benefits)
2. **Facilitator:** Raises ability (makes it easier)
3. **Signal:** Works when motivation + ability already exist (just a reminder)

**Tiny Habits Recipe:** "After I [ANCHOR MOMENT], I will [TINY BEHAVIOR]"
- Anchor = reliable existing behavior
- Tiny Behavior = takes **< 30 seconds** and minimal effort
- Example: "After I pour my morning coffee, I will open Telegram"

**Minimum Viable Behavior:** Make the habit so small it's impossible to fail. "Floss one tooth." "Do two pushups." "Review one note."

**The Celebration:** Immediately after the tiny behavior, generate positive emotion (fist pump, "Yes!", mental high-five). This reinforces the behavior neurologically.

**Key finding:** Leaders who began with minimal viable habits and gradually scaled up were **2.7x more likely** to maintain long-term habits than those who started with ambitious targets.

### James Clear's Atomic Habits Framework

**The Habit Loop:** Cue → Craving → Response → Reward

**Four Laws of Behavior Change:**
1. **Make it obvious** (Cue) — visible triggers, environment design
2. **Make it attractive** (Craving) — pair with something enjoyable
3. **Make it easy** (Response) — reduce friction, 2-minute rule
4. **Make it satisfying** (Reward) — immediate gratification

**Habit Stacking:** "After [CURRENT HABIT], I will [NEW HABIT]"

**Breaking habits (inversions):** Make it invisible, unattractive, difficult, unsatisfying.

### Phillippa Lally's Research (UCL, 2009)

**How long does habit formation actually take?**
- Average: **66 days** to reach automaticity
- Range: **18 to 254 days**
- Simple behaviors (drinking water) → faster
- Complex behaviors (50 sit-ups) → much slower
- **The "21 days" myth** comes from Dr. Maxwell Maltz's 1960 book about plastic surgery patients adjusting to new faces — has nothing to do with habit formation

**Key finding:** Missing a single day did NOT significantly derail habit formation. What matters is getting back on track, not perfection.

### Why People Ghost Habits

**From the Anki burnout research — 80% of SRS learners quit:**
1. **Review backlog terror:** Miss a few days → 500+ cards pile up → psychological barrier to return
2. **Leech cards:** Hardest 5-10% of flashcards consume **50% of review time** — demoralizing
3. **Setup fatigue:** Creating cards takes as long as studying
4. **No visible progress:** Effort doesn't feel connected to real-world ability
5. **All-or-nothing mindset:** "If I can't do all reviews, I won't do any"
6. **Complexity:** Anki has a 200-page manual — friction kills adoption

### Application to Telegram Bot
- **Start absurdly small:** Send ONE note per day. "Review one note" is the habit, not "review all notes."
- **Never create a backlog.** If the user misses days, don't pile up. Just pick the most important note and send that.
- **Anchor to existing behavior:** Send at the time the user already checks Telegram (morning routine, commute, etc.)
- **Make it satisfying immediately:** Show progress, acknowledge completion, use a "streak" that has a freeze mechanism
- **2-minute rule:** Each review interaction should take < 2 minutes
- **Celebrate completion:** Positive feedback after review ("Nice, you've reviewed 3 notes this week")
- **Never guilt-trip:** If user misses days, welcome them back warmly. Duolingo learned that lenient streaks (with freezes) dramatically increase retention vs. strict ones
- **Cap daily reviews:** Set a ceiling on daily notes to prevent overwhelm

---

## 4. Note-Taking and Knowledge Retention

### The Generation Effect (Slamecka & Graf, 1978)

**Classic experiment:** Participants either read complete word pairs (KING-CROWN) or generated the second word from a cue (KING-CR___).

**Result:** Generated words were consistently better remembered than read words, across:
- Cued and uncued recognition
- Free and cued recall
- Confidence ratings
- All encoding rules tested
- Both between- and within-subjects designs

**Core principle:** Information you CREATE yourself is far more memorable than information you passively receive.

### Writing Notes vs. Reading Others' Notes

**Handwriting research (University of Tokyo):**
- Handwritten notes activated more brain activity in language areas, imaginary visualization, and the **hippocampus** (memory center)
- Writing forces prioritization, consolidation, and connection to prior knowledge
- Typing allows transcription without processing — "in through ears, out through fingertips"

**Meta-analysis finding (2021):** The apparent advantage of longhand over digital notetaking can be explained partly by digital devices enabling distractions. When distractions are controlled, the gap narrows — but the generation/processing advantage remains.

**Key insight for the bot:** The USER's own notes are inherently more memorable to them than someone else's notes. The generation effect means their own words carry stronger memory traces.

### The Testing Effect Applied to Notes

**Karpicke (2012) — "Active Retrieval Promotes Meaningful Learning":**
- Retrieval practice doesn't just strengthen rote memory — it promotes deeper, more meaningful learning
- Students who practiced retrieval could better apply knowledge to new situations
- Testing doesn't just measure learning; it CAUSES learning

### What Makes Knowledge "Stick" Long-Term

Research consensus on durable learning:
1. **Generate it yourself** (generation effect)
2. **Test yourself on it** (testing effect)
3. **Space the reviews** (spacing effect)
4. **Interleave with other topics** (interleaving effect)
5. **Connect it to what you know** (elaborative interrogation)
6. **Use it in varied contexts** (desirable difficulty)

### Application to Telegram Bot
- **Surface the user's OWN notes** — never generic content. Their words carry the generation effect.
- **Ask them to recall before showing:** "What was your key insight about [topic]?" → then show the note
- **Prompt elaboration:** "How does this connect to [other note topic]?" — forces elaborative interrogation
- **Don't just re-display notes** — transform the interaction into a micro-test
- **Leverage the generation effect:** When resurfacing, ask the user to rewrite or summarize the note in their own words (even briefly)

---

## 5. Microlearning / Low-Friction Learning

### Evidence For Effectiveness

**Journal of Applied Psychology:** Learning in smaller segments improves knowledge retention by up to **17%** compared to traditional longer sessions.

**Cognitive Load Theory basis:** Working memory holds only **4-7 chunks** simultaneously. Microlearning respects this limit by delivering small, digestible content.

**Randomized controlled trials:** Students receiving microlearning modules performed significantly better on post-tests than those in traditional instruction.

**Workplace studies:** Employees receiving microlearning showed significantly enhanced job performance vs. traditional training.

**Optimal duration:** Typically **2-10 minutes** per unit. Under 5 minutes is the sweet spot for mobile/casual learning contexts.

### When Microlearning Works
- Factual knowledge and terminology
- Procedural skills with discrete steps
- Reinforcement of previously learned concepts
- Review and retrieval practice
- Just-in-time learning (need it now, apply it now)
- When used as a COMPLEMENT to deeper learning

### When Microlearning Fails
- **Complex, systemic topics** requiring deep analysis — you cannot teach team leadership in 5-minute bursts
- **When it's the ONLY format** — user satisfaction drops significantly when microlearning isn't complemented by deeper engagement
- **Topics requiring synthesis and critical thinking** — bite-sized chunks lack context for big-picture understanding
- **Without scaffolding** — if learners jump between micro-units without knowing how they connect, "it just feels like noise"
- **Strategic/lateral thinking** — develops best through extended sessions, not scattered chunks

### Application to Telegram Bot
- **Perfect fit:** Note review is inherently micro — revisiting a note you already wrote is a 1-3 minute interaction
- **Keep each interaction under 3 minutes** — one note, one prompt, one response
- **Don't try to teach new concepts** — the bot resurfaces EXISTING knowledge, which is microlearning's strength
- **Provide context links:** When showing a note, mention related notes to maintain big-picture coherence
- **Scaffold complexity:** For complex topics with multiple notes, resurface them in a logical sequence, not randomly

---

## 6. Interleaving and Desirable Difficulty

### Bjork's Desirable Difficulties Framework (1994)

**Definition:** A learning task that requires considerable but beneficial effort, improving long-term performance despite reducing short-term performance.

**Storage Strength vs. Retrieval Strength:**
- **Storage strength:** How deeply information is embedded (stable, builds over time)
- **Retrieval strength:** How easily accessible right now (fluctuates with recency)
- Desirable difficulties work by **deliberately reducing retrieval strength**, which paradoxically **strengthens storage strength** through effortful reconstruction

**The four desirable difficulties (Bjork, 1994):**
1. Spacing
2. Interleaving
3. Retrieval practice (testing)
4. Generation

### Interleaving Research

**Rohrer and Taylor (2007):** Interleaved practice produced **43% better performance** on delayed tests vs. blocked practice.

**Pan et al. (2019) meta-analysis:** Moderate-to-large effect size (d = 0.67) favoring interleaving for discriminative learning.

**General finding:** 20-50% performance increase on delayed tests with interleaved practice.

**University physics study:** Students using interleaved homework problems showed **50% improvement on test 1** and **125% improvement on test 2** compared to blocked practice.

### The Interleaving Paradox

- During practice, **blocked study FEELS better** and **performance is higher**
- On delayed tests, **interleaved study produces superior retention**
- Students consistently PREFER blocking despite interleaving being more effective
- This is another instance of the fluency illusion — easy practice feels like better learning

### When Interleaving Doesn't Work
- **When learners lack foundational knowledge** — they can't handle the cognitive demands of switching
- **For rule-finding tasks** — blocking is more effective when trying to discover an underlying rule
- **For very low-achieving students** — interleaving can be an "undesirable difficulty" if the material is too challenging

### Application to Telegram Bot
- **Mix note topics by default.** Don't show all notes about "Project X" in sequence — interleave with "Philosophy" and "Cooking" notes.
- **But respect relatedness:** Interleaving works best when concepts are related enough for meaningful connections but distinct enough to require discrimination.
- **Practical approach:** Within a day's reviews, never show two notes from the same topic back-to-back.
- **For new users:** Start with less interleaving (build foundational comfort), increase mixing as they build the habit.

---

## 7. Motivation and Engagement

### Self-Determination Theory (Deci & Ryan, 1985)

**Three innate psychological needs:**
1. **Autonomy:** Feeling in control of your choices
2. **Competence:** Feeling capable and effective
3. **Relatedness:** Feeling connected to others

**Key finding:** All expected tangible rewards made contingent on task performance **reliably undermine intrinsic motivation.** Also: threats, deadlines, directives, pressured evaluations, and imposed goals all diminish intrinsic motivation.

**What enhances intrinsic motivation:** Choice, acknowledgment of feelings, opportunities for self-direction.

**Educational finding:** Students taught with controlling approaches lose initiative AND learn less effectively, especially for conceptual/creative tasks.

### Why People Abandon Anki (80% Quit Rate)

1. **Review backlog spiral:** Miss days → hundreds of overdue cards → overwhelming → quit
2. **Leech cards eat 50% of time:** The hardest 5-10% of cards consume half of study time
3. **No connection to real ability:** 95% recognition memory but 10% speaking ability
4. **Setup tax:** Creating cards takes as long as studying
5. **Software complexity:** 200-page manual = friction barrier
6. **56% of users use premade decks** — losing the generation effect
7. **All-or-nothing psychology:** SRS demands daily commitment; missing feels like failure

### What Makes Duolingo Work

**Streaks:**
- Users with 7-day streaks are **3.6x more likely** to stay engaged long-term
- Streaks increase commitment by **60%**
- Leverages **loss aversion** — losing progress hurts more than gaining rewards
- **Critical finding:** Being LENIENT with streaks (streak freezes) dramatically improves retention. Losing a 500-day streak causes permanent dropout.

**XP and Leaderboards:**
- Leaderboards drive **40% more engagement**
- Badges boost completion rates by **30%**
- Limited-time events (Double XP Weekend) cause **50% activity surge**

**What Duolingo Gets Wrong:**
- Guilt-based retention creates resentment
- Gamification without learning depth → "completing lessons" without actually learning
- Heavy extrinsic motivation can undermine intrinsic interest in the language

### Variable Ratio Reinforcement

**From operant conditioning research:**
- Variable ratio schedules (unpredictable rewards) produce the **highest and most consistent engagement**
- They're **resistant to extinction** — people continue even without immediate reward
- This is the slot machine effect
- **Ethical concern:** Can cross from engagement into compulsive behavior

### Duolingo's Key Retention Numbers
- **55% next-day retention** rate
- Days 2-10 are the **danger zone for churn**
- Users reaching 7-day streak are **2.4x more likely** to continue the next day
- ~30% of learners 60+ maintain year-long streaks vs. <5% of teens

### Application to Telegram Bot

**Do:**
- Give users **choice** in what they review (autonomy)
- Show them their **progress and growth** (competence)
- Use **gentle streaks with freezes** — never punish missed days
- Keep interactions under 2 minutes (ability)
- Send at consistent, user-chosen times (prompt)
- Celebrate completion (positive reinforcement)
- Occasionally surface a surprising or delightful connection between notes (variable reward)
- Let users control frequency and volume

**Don't:**
- Create review backlogs
- Use guilt or pressure ("You haven't reviewed in 3 days!")
- Require complex setup
- Make it feel like homework
- Overwhelm with quantity
- Use only extrinsic rewards (points/badges) without intrinsic value
- Demand daily perfection

---

## Summary: Design Principles for the Telegram Bot

### Evidence-Based Architecture

1. **Adaptive spacing** based on simplified FSRS/Leitner: Start at 1 day, extend to 3→7→14→30→90 days based on engagement quality
2. **Active recall prompts** before showing notes: "What do you remember about [topic]?"
3. **Interleaved topics** by default: Never two notes from same topic in sequence
4. **Micro-interactions only**: Each review = 1-3 minutes maximum
5. **No backlogs ever**: If user misses days, just show the highest-priority note next time
6. **User's own notes only**: Leverages the generation effect
7. **Celebration on completion**: Positive feedback after each review
8. **Lenient streaks**: Track consistency but offer freezes; never guilt-trip
9. **User-controlled timing**: Let them pick when they get messages
10. **Gradual scaling**: Start with 1 note/day, slowly increase only if user wants

### The Science Stack (in order of impact)

| Technique | Effect Size | Priority |
|---|---|---|
| Spaced repetition | Massive (prevents forgetting curve) | Core mechanic |
| Active recall/testing | 400% improvement over rereading | Every interaction |
| Generation effect | Robust across all measures | Use user's own notes |
| Interleaving | d = 0.67, 20-50% improvement | Mix topics |
| Microlearning | 17% retention improvement | Keep it short |
| Desirable difficulty | Enhances long-term storage | Make it slightly effortful |
| Tiny habit design | 2.7x more likely to stick | Start absurdly small |
| Lenient streak mechanics | 3.6x engagement at 7 days | Forgive, don't punish |

---

## Key Sources

### Spaced Repetition
- Ebbinghaus, H. (1885). Memory: A Contribution to Experimental Psychology
- Wozniak, P., Gorzelanczyk, E., Murakowski, J. (1995). Two components of long-term memory
- Cepeda, N.J., Vul, E., Rohrer, D., Wixted, J.T., Pashler, H. (2008). Spacing Effects in Learning: A Temporal Ridgeline of Optimal Retention
- SM-2 Algorithm: https://super-memory.com/english/ol/sm2.htm
- FSRS Technical Explanation: https://expertium.github.io/Algorithm.html
- FSRS Benchmark: https://expertium.github.io/Benchmark.html

### Active Recall
- Roediger, H.L. & Karpicke, J.D. (2006). Test-Enhanced Learning
- Karpicke, J.D. (2012). Active Retrieval Promotes Meaningful Learning
- Dunlosky, J. et al. (2013). Improving Students' Learning With Effective Learning Techniques

### Habit Formation
- Fogg, B.J. (2020). Tiny Habits: The Small Changes That Change Everything
- Clear, J. (2018). Atomic Habits
- Lally, P. et al. (2010). How are habits formed: Modelling habit formation in the real world (UCL)

### Note-Taking and Knowledge
- Slamecka, N.J. & Graf, P. (1978). The Generation Effect: Delineation of a Phenomenon
- Matuschak, A. — Evergreen note maintenance approximates spaced repetition

### Interleaving and Difficulty
- Bjork, R.A. (1994). Memory and metamemory considerations in the training of human beings
- Rohrer, D. & Taylor, K. (2007). Interleaving effects on learning
- Pan, S.C. et al. (2019). Meta-analysis of interleaving effects

### Motivation and Engagement
- Deci, E.L. & Ryan, R.M. (1985/2000). Self-Determination Theory
- Duolingo streak research: https://blog.duolingo.com/how-duolingo-streak-builds-habit/
- Anki burnout analysis: https://my-senpai.com/insights/ankiburnout.html
