---
title: "Agents Are Learning to Write Their Own SKILL.md Files"
subtitle: "The Agent Skills open standard today, and the 2026 research on agents that write their own skills."
slug: agents-that-write-their-own-skill-md
tags: artificial-intelligence, llm, programming, python
ignorePost: false  # weekly drip — flip to false (or delete) to release this post
cover: https://cdn.jsdelivr.net/gh/Shridhar-2205/living-software@main/assets/covers/cover-06.png
canonical: https://dev.to/shridhar_shah2297/agents-are-learning-to-write-their-own-skillmd-files-3foo
seoTitle: "Agents That Write Their Own SKILL.md Files"
seoDescription: "How the Agent Skills (SKILL.md) open standard works, plus a demo of an agent that writes and reuses its own spec-compliant skills."
---

**TL;DR:** I've been using skills in Claude Code daily, and one question stuck with me: what
happens when the agent writes them itself? Quick background: "Agent Skills" (late 2025) are a
dead-simple way to teach an agent a task — a folder with a `SKILL.md` file of Markdown
instructions, now an open standard. The wild part is what's coming next: agents that **write
their own skills.** I built a demo where an agent solves a task the hard way once, saves a
real `SKILL.md`, and then reuses it — cutting its total effort almost in half. No API key.

---

## First, what's a "skill"?

If you've used Claude Code or similar tools lately, you've probably seen `SKILL.md` files.
The idea is refreshingly low-tech. A "skill" is just a folder with a Markdown file that
says *how to do something*:

```
---
name: csv-to-markdown
description: Turn comma-separated text into a Markdown table. Use when the input looks
  like CSV and the user wants a table.
---

# CSV to Markdown

## Instructions
Split the text into rows on newlines and columns on commas. Make the first row the
header, add a `---` divider row, then format every row as `| a | b | c |`.
```

That's it. No SDK, no config. Anthropic introduced this in October 2025 and then published
it as an **open standard** ([agentskills.io](https://agentskills.io)) in December 2025, so
the same skill folder now works across ~30+ different agent tools (Claude Code, Cursor,
Copilot, and more).

The full rules are short ([agentskills.io/specification](https://agentskills.io/specification)):
the only **required** fields are `name` (1–64 chars, lowercase-with-hyphens, and it must
match the folder name) and `description` (≤1024 chars, saying *what it does and when to use
it*). Everything else — `license`, `metadata`, `compatibility`, `allowed-tools` — is
optional. That's the whole spec. The `SKILL.md` files my demo writes follow it to the
letter, so they'd load unmodified in any compatible CLI.

## The clever trick: progressive disclosure

Here's the smart part. If you just dumped 50 skills' worth of instructions into the agent's
context, you'd fill it up and leave no room for actual work. So skills load in **stages**:

1. **Always loaded:** just the `name` and one-line `description` of every skill (tiny).
2. **Loaded only when it matches:** the full instructions, once a task actually needs them.
3. **Loaded only if referenced:** extra files or scripts the skill bundles.

So the agent can have *hundreds* of skills installed and barely pay for it — it only reads
the short descriptions until one matches, then pulls in the details. My demo shows the
math: to use 1 skill out of 3 installed, loading everything costs ~1500 "tokens"; the
SKILL.md way costs ~560. That gap gets huge as your library grows.

This is also why people say skills and **MCP** are teammates, not rivals: MCP is how an
agent *connects to tools*; a skill is how an agent *knows the procedure* for using them.

## The frontier: agents that write their own skills

Today, humans write `SKILL.md` files. The 2026 research is about agents that write their
**own** — and get better over time as their skill library grows. This goes back to
**Voyager** (2023), an agent that played Minecraft and saved working code as reusable
skills, getting dramatically faster at the game. The new wave makes it general:

- **[MUSE-Autoskill](https://arxiv.org/html/2605.27366)** (2026) treats a skill as a
  *living asset* with a full lifecycle — create it, give it its own memory file, manage it,
  test it, and refine it. Each skill even keeps a `.memory.md` of notes about itself.
- **[Memento-Skills](https://arxiv.org/pdf/2603.18743v1)** (2026) stores skills as Markdown
  files that double as the agent's evolving memory, and turns task *failures* into new
  skills automatically.
- **[Skill-Pro](https://arxiv.org/abs/2602.01869)** (2026) defines a skill as "when to use
  it + how to do it + when to stop," and only keeps a new skill if it passes a quality gate
  — so the library improves instead of filling up with junk.

The common thread: **solve it once, save the recipe, reuse it forever** — and let the
collection get smarter on its own.

> 📄 **The "this is the future" link:** Anthropic's own writeup,
> [*Equipping agents for the real world with Agent Skills*](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills),
> and the open standard at **[agentskills.io](https://agentskills.io)**. For the research
> direction, [MUSE-Autoskill (arXiv:2605.27366)](https://arxiv.org/abs/2605.27366) and
> [Skill-Pro (arXiv:2602.01869)](https://arxiv.org/abs/2602.01869) are the clearest reads on
> agents that grow their own skill libraries.

## You can do this *today* in the Claude Code CLI

This isn't theoretical — the exact pattern from my demo already ships in coding CLIs. In
**Claude Code**, a skill is just a folder under `.claude/skills/` in your repo:

```bash
# Anywhere in your project — drop a skill in and the CLI auto-discovers it
mkdir -p .claude/skills/csv-to-markdown
$EDITOR .claude/skills/csv-to-markdown/SKILL.md   # same SKILL.md format as my demo
```

Now the agent loads only that skill's one-line `description` until a task matches — then
pulls in the full instructions (that's progressive disclosure doing its job). Type `/skills`
inside the CLI to see what's loaded.

The best part: because it's an **open standard**, the *same* folder works unmodified across
tools. You're not locked in:

- **[Claude Code](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)** — Anthropic's CLI, where the format started.
- **[opencode](https://github.com/sst/opencode)** — a popular open-source terminal agent.
- **[Goose](https://github.com/block/goose)** — Block's open-source agent.
- Plus Cursor, GitHub Copilot, and 30+ others.

Write the skill once, use it everywhere. The future bit my demo points at: instead of *you*
hand-writing that file, the agent writes it for itself after solving the task the first
time — and from then on, your repo quietly accumulates a library of skills your agent
earned.

## The 10-second version (my demo)

Same stream of 7 tasks. "Cost" is how much effort each one took.

| | No-skills agent | Skill-writing agent |
|---|---|---|
| What it does | re-solves everything from scratch | learns a task once, saves a `SKILL.md`, reuses it |
| Total cost | **35** | **19** |
| Both correct? | 7/7 | 7/7 |

```
[5] csv-to-markdown  learned it and wrote SKILL.md
[5] slugify          learned it and wrote SKILL.md
[1] csv-to-markdown  reused skill 'csv-to-markdown'   ← cheap now
[5] extract-emails   learned it and wrote SKILL.md
[1] slugify          reused skill 'slugify'
[1] csv-to-markdown  reused skill 'csv-to-markdown'
[1] extract-emails   reused skill 'extract-emails'
```

It writes **real `SKILL.md` files** into a `./skills` folder you can open. The first time
it sees a task it pays full price; after that, it finds its own saved skill and reuses it
for cheap.

## Why this matters

Two big reasons engineers should care:

1. **Agents stop repeating themselves.** Right now most agents re-derive the same thing
   over and over, paying for it every time. A skill library means "figure it out once, then
   it's free" — like a teammate who writes things down instead of relearning them daily.

2. **A whole new ecosystem.** There are already 65,000+ shared skills and a scramble to
   build "the npm of agent skills" — registries and marketplaces where you install a skill
   like a package. Skills are becoming a unit of *shareable expertise*: a senior engineer's
   know-how, packaged in a folder, that any agent can pick up.

> Tools tell an agent *what it can do*. Skills tell it *how to do things well* — and soon,
> agents will write that part themselves, and trade it with each other.

## Try it

```bash
git clone https://github.com/Shridhar-2205/living-software
cd living-software/06-agent-skills
python demo.py
cat skills/csv-to-markdown/SKILL.md   # a skill the agent wrote itself
```

Honest note: this is a POC. Real systems decide *when* a new skill is worth saving, test
it, and refine it over time (that's exactly what the 2026 papers above tackle). Mine keeps
that part simple so the core idea — *learn once, save a SKILL.md, reuse it* — is easy to
see.

## The rest of the series — *Toward Living Software*

1. [I built an AI agent that rewrites its own code](https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-rewrites-its-own-code-in-150-lines-3jjo)
2. [Do AI agents need to sleep?](https://dev.to/shridhar_shah2297/do-ai-agents-need-to-sleep-i-built-one-that-does-53c4)
3. [Can an AI agent pass the Sally-Anne test?](https://dev.to/shridhar_shah2297/can-an-ai-agent-pass-the-test-we-give-4-year-olds-5825)
4. [An AI agent that gets curious on its own](https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-gets-curious-on-its-own-4oe1)
5. [How do you trust an AI agent with your money?](https://dev.to/shridhar_shah2297/how-do-you-trust-an-ai-agent-with-your-money-you-dont-you-check-its-receipt-38ff)
6. **Agents that write their own SKILL.md files** (you're reading it)

---

**Shridhar Shah** — Senior Software Engineer on the AI team at Cisco. Part 6 of *Toward Living Software*.

[GitHub](https://github.com/Shridhar-2205) · [LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)

> **Sources:** Anthropic, "Equipping agents for the real world with Agent Skills" (2025) and
> the Agent Skills open standard (agentskills.io); Voyager (arXiv:2305.16291);
> MUSE-Autoskill (arXiv:2605.27366); Memento-Skills (arXiv:2603.18743); Skill-Pro
> (arXiv:2602.01869); MemSkill (arXiv:2602.02474).
