---
title: "I Built an AI Agent That Rewrites Its Own Code"
subtitle: "A tiny Darwin Gödel Machine that edits itself and keeps only changes that verifiably score higher."
slug: ai-agent-that-rewrites-its-own-code
tags: artificial-intelligence, machine-learning, programming, python
cover: https://cdn.jsdelivr.net/gh/Shridhar-2205/living-software@main/assets/covers/cover-01.png
canonical: https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-rewrites-its-own-code-in-150-lines-3jjo
seoTitle: "I Built an AI Agent That Rewrites Its Own Code"
seoDescription: "A tiny Darwin Gödel Machine that edits its own code and keeps only verifiably-better changes — climbing from 1/8 to 8/8."
---

**TL;DR:** I kept hearing that AI is about to start improving *itself*, and I was skeptical —
so one weekend I built the smallest version I could. It looks at the tasks it's failing,
edits its own code to fix them, and keeps a change only if it actually scores better on a
test. It goes from passing **1 of 8** tasks to **8 of 8** — and nobody wrote those fixes but
the program itself. Runs on a laptop in under a second. No fancy hardware, no API key.

---

## The old dream: software that improves itself

Normally, software only gets better when *we* make it better. You write code, you find a
bug, you fix it, you ship again. The program never improves on its own.

People have wanted "software that improves itself" for decades. The classic version (called
a "Gödel Machine") had one rule that made it impossible to build: before the program could
change a line of its own code, it had to *mathematically prove* the change would help.
Proving that about real code is basically impossible, so the idea never worked.

In 2025, researchers found a way around it with the
**[Darwin Gödel Machine](https://arxiv.org/abs/2505.22954)**. They dropped the "prove it
first" rule and replaced it with something every engineer already trusts:

> **Try the change. Run the tests. If the score went up, keep it. If not, throw it away.**

That's it. It's basically how we all work — make an edit, run the test suite, keep what
passes. The twist is that *the program* is the one making the edits. In the real paper,
this let an AI coding assistant improve its own tooling and jump from solving **20%** to
**50%** of a hard benchmark of real GitHub issues.

I wanted to actually see this happen, so I built the tiniest version I could.

## The 10-second version

| | Start | After improving itself |
|---|---|---|
| What it can do | only `uppercase` | learned 6 more skills on its own |
| Test score | 🔴 **1 / 8** | 🟢 **8 / 8** |
| Who wrote the fixes? | — | **the program did** |

```
Start:  ███░░░░░░░░░░░░░░░░░░░░░  1/8   (only knows: uppercase)
+reverse            ██████░░░░░░░░░░░░  2/8
+dedup_csv          █████████░░░░░░░░░  3/8
+sum_csv            ████████████░░░░░░  4/8
+sort_csv           ███████████████░░░  5/8
+title              ██████████████████  6/8
+normalize_inputs   ████████████████████  8/8   ← one fix unlocked TWO tasks
✅ SOLVED 8/8
```

## How it works (the whole thing)

There are only three pieces.

**1. The "agent" is just a bag of skills.** Each skill is a tiny function — uppercase text,
reverse it, sort a list, etc. It starts out knowing almost nothing.

**2. A test with known answers.** Every task has a correct answer, so checking the score is
a plain equality check — `output == expected`. No human grading it, no second AI judging
it. Just: did it get the right answer or not? (This "write a checker, then measure" idea is
the same trick behind today's reasoning models.)

**3. The loop.** Over and over: look at what's failing, add one skill to try to fix it,
re-run the test, and **keep the change only if the score went up.** It also saves every
improved version, so it can branch off any of them later instead of getting stuck.

```python
new_version = old_version + add_a_skill(things_it_is_failing)
if score(new_version) > score(old_version):   # did the test score actually improve?
    keep(new_version)                          # yes -> save it and build on it
```

## The cool part: small fixes unlock big ones

One of the skills it adds, "clean up the input" (trim weird spacing), does **nothing** by
itself. But the agent had earlier learned a "title-case" skill that kept breaking on messy
text like `"  the   quick   fox "`. The moment it adds the cleanup step, **two stuck tasks
start passing at once** — that's the +2 jump at the end.

This is the whole point in miniature: the agent isn't just adding features. It's making
itself *better at getting better*. A boring little fix becomes the stepping stone that makes
later fixes work. The real research sees the same thing at full scale — the AI invents
helpers like "try a few solutions and pick the best one," which then make *every* future fix
more effective.

## Why I think this is where things are going

For ten years, the way to make AI better was: make the model bigger. The newer idea is to
make it **improve itself while it runs**:

- **This post** — an agent that rewrites its own code.
- **["Language Models Need Sleep"](https://arxiv.org/abs/2606.03979)** (2026) — agents that
  tidy up their own memory during an offline "sleep."
- **Small models that think harder** instead of being bigger.

The common thread: improvement is shifting from *us retraining the model* to *the program
improving itself*, with a simple test telling it whether each change was good. Software that
edits itself starts to feel less like a fixed program and more like something that grows.

## Try it (under a minute)

```bash
git clone https://github.com/Shridhar-2205/living-software
cd living-software/01-self-rewriting-agent
python demo_cli.py     # watch the score climb 1/8 → 8/8
pytest -q              # the same claims, as automated tests
```

One honest note on safety: a *real* self-rewriting agent runs code it wrote itself, which is
risky. In my version the "edits" come from a fixed list of safe skills, so nothing
dangerous ever runs — the *loop* matches the research, the *risk* is zero. (The real one
runs inside a sandbox for exactly this reason.)

## The takeaway

> The old dream needed a mathematical proof before changing any code. The new version just
> needs a **test**. If you can write a check that says "this got better," you can let a
> program improve itself — and watch it find clever fixes you never wrote.

## The rest of the series — *Toward Living Software*

1. **I built an AI agent that rewrites its own code** (you're reading it)
2. [Do AI agents need to sleep?](https://dev.to/shridhar_shah2297/do-ai-agents-need-to-sleep-i-built-one-that-does-53c4)
3. [Can an AI agent pass the Sally-Anne test?](https://dev.to/shridhar_shah2297/can-an-ai-agent-pass-the-test-we-give-4-year-olds-5825)
4. [An AI agent that gets curious on its own](https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-gets-curious-on-its-own-4oe1)
5. [How do you trust an AI agent with your money?](https://dev.to/shridhar_shah2297/how-do-you-trust-an-ai-agent-with-your-money-you-dont-you-check-its-receipt-38ff)
6. [Agents that write their own SKILL.md files](https://dev.to/shridhar_shah2297/agents-are-learning-to-write-their-own-skillmd-files-3foo)

---

**Shridhar Shah** — Senior Software Engineer on the AI team at Cisco. Part 1 of *Toward Living Software*.

[GitHub](https://github.com/Shridhar-2205) · [LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)

> **Source:** Zhang, Hu, Lu, Lange, Clune, "Darwin Gödel Machine: Open-Ended Evolution of
> Self-Improving Agents," arXiv:2505.22954 (2025) — reports SWE-bench 20.0% → 50.0%.
