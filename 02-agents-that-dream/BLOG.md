---
title: "Do AI Agents Need to Sleep? I Built One That Does"
subtitle: "A sleep-like phase that consolidates noisy daily experience into durable memory — 75% vs 100% recall."
slug: do-ai-agents-need-to-sleep
tags: artificial-intelligence, machine-learning, llm, python
ignorePost: false  # weekly drip — flip to false (or delete) to release this post
cover: https://cdn.jsdelivr.net/gh/Shridhar-2205/living-software@main/assets/covers/cover-02.png
canonical: https://dev.to/shridhar_shah2297/do-ai-agents-need-to-sleep-i-built-one-that-does-53c4
seoTitle: "Do AI Agents Need to Sleep?"
seoDescription: "Sleep-like memory consolidation for AI agents: an offline phase folds noisy daily notes into durable memory and lifts recall from 75% to 100%."
---

**TL;DR:** Everyone "fixes" AI memory by making the context window bigger. I wanted to try
the opposite idea, so I built a demo of a 2026 research trend: giving an agent a "sleep"
phase — time spent *not* answering questions, just tidying up what it learned that day. The
agent that "sleeps" remembers **100%** of what it learned. The exact same agent *without*
sleep remembers only **75%** and gets confused by bad info. Runs on a laptop.

---

## The memory problem every AI app hits

If you've built anything with an LLM, you know the pain: the model only "remembers" what's
in its current context window. Once the conversation gets long enough, the oldest stuff
scrolls off the top and is just... gone. Forgotten.

The usual fix is "make the context window bigger." But that's like fixing a messy desk by
buying a bigger desk. It's expensive, and the model still gets worse as you cram more in (a
real, measured effect — more text in the window can actually *lower* accuracy).

Your brain doesn't work this way. You don't remember every sentence anyone said today. While
you sleep, your brain replays the day, keeps the important bits as long-term memory, and
dumps the rest. That's how you remember "I like coffee" without remembering every single cup.

A couple of 2026 papers ask the obvious question:
**[Do Language Models Need Sleep?](https://arxiv.org/abs/2605.26099)** Their answer:
giving an AI a quiet "offline" phase to consolidate memories makes it remember better. So I
built the simplest version that shows why.

## The 10-second version

| | ❌ Agent with no sleep | ✅ Agent that sleeps |
|---|---|---|
| How it remembers | keeps only the last N messages | saves a tidy summary every night |
| After 30 noisy days | **75% recall** | **100% recall** |
| Tricked by bad info? | yes | no — it goes with what it saw most often |

Same experiences, same noise, same memory test. The only difference is whether the agent
sleeps.

## How it works

Each "day," the agent hears facts like `Alice → drinks → coffee`. To make it realistic,
about 1 in 5 facts is wrong (people misremember, logs have errors).

- The **no-sleep agent** only keeps the last 10 things it heard. Anything older falls off
  the edge and is forgotten. And one bad recent day can flip its answer.
- The **sleeping agent** does one extra thing each night: it goes back through the day,
  updates a small running tally of what it heard, and then clears out the raw log:

```python
def sleep(self):
    for (person, fact, value) in todays_notes:
        memory[person][value] += 1   # add today's notes to the long-term tally
    todays_notes.clear()             # forget the raw firehose, keep the summary
```

That tiny step buys two things:

1. **It doesn't forget.** The summary sticks around even after the raw messages are gone.
2. **It filters out bad info.** Because it counts how often it heard each thing across many
   days, the occasional wrong fact gets outvoted by the truth.

## Why this matters

Everyone's trying to fix AI memory by making the context window huge. But a bigger window is
still just a bigger pile of raw text — expensive, and it still overflows.

Sleep is a smarter bet: **do the cleanup when the agent is idle.** Spend a little time while
nobody's waiting to turn today's messy notes into a clean, permanent summary — so when
someone *does* ask, the answer is fast, cheap, and correct. It's the same theme as an agent
that improves its own code: get better while you run, not just when a human retrains you.

> The better AI agent doesn't have a bigger memory. It has a *tidier* one — because it
> sleeps.

## Try it

```bash
git clone https://github.com/Shridhar-2205/living-software
cd living-software/02-agents-that-dream
python demo.py
```

Honest note: real systems fold these summaries into the model itself with fancier methods.
Mine just uses a plain dictionary. The *idea* (replay the day → save a summary → clear the
raw log) is exactly the same; the code is kept tiny on purpose.

## The rest of the series — *Toward Living Software*

1. [I built an AI agent that rewrites its own code](https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-rewrites-its-own-code-in-150-lines-3jjo)
2. **Do AI agents need to sleep?** (you're reading it)
3. [Can an AI agent pass the Sally-Anne test?](https://dev.to/shridhar_shah2297/can-an-ai-agent-pass-the-test-we-give-4-year-olds-5825)
4. [An AI agent that gets curious on its own](https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-gets-curious-on-its-own-4oe1)
5. [How do you trust an AI agent with your money?](https://dev.to/shridhar_shah2297/how-do-you-trust-an-ai-agent-with-your-money-you-dont-you-check-its-receipt-38ff)
6. [Agents that write their own SKILL.md files](https://dev.to/shridhar_shah2297/agents-are-learning-to-write-their-own-skillmd-files-3foo)

---

**Shridhar Shah** — Senior Software Engineer on the AI team at Cisco. Part 2 of *Toward Living Software*.

[GitHub](https://github.com/Shridhar-2205) · [LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)

> **Sources:** "Do Language Models Need Sleep?" (arXiv:2605.26099); "Language Models Need
> Sleep: Learning to Self-Modify and Consolidate Memories" (arXiv:2606.03979).
