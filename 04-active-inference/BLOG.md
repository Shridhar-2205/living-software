---
title: "I Built an AI Agent That Gets Curious On Its Own"
subtitle: "Active inference: curiosity emerges for free from minimizing surprise — 48% vs 100% on a foraging task."
slug: ai-agent-that-gets-curious
tags: artificial-intelligence, machine-learning, llm, python
ignorePost: false  # weekly drip — flip to false (or delete) to release this post
cover: https://cdn.jsdelivr.net/gh/Shridhar-2205/living-software@main/assets/covers/cover-04.png
canonical: https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-gets-curious-on-its-own-4oe1
seoTitle: "An AI Agent That Gets Curious On Its Own"
seoDescription: "Active inference in practice: an agent that minimizes surprise develops curiosity for free, going from 48% to 100% on a foraging task."
---

**TL;DR:** Most AI agents chase rewards — they pick whatever action scores the most points.
I wanted to see what happens if you build one that just tries not to be *surprised*. Something
neat happened — the agent became **curious without being told to.** It goes looking for
information before acting, and that takes it from 48% to 100% on a simple task.

---

## Two different ways to make decisions

Most AI agents are "reward chasers." Give them points for doing well, and they'll pick
whatever action they expect to score highest. Simple and effective.

There's another idea from brain science: instead of chasing points, **try to avoid being
surprised** — act so the world matches what you expected. It sounds almost too simple, but
it leads to a surprising bonus: **when you're trying not to be surprised, going and finding
out what you don't know becomes valuable all by itself.** In other words, curiosity isn't
something you have to bolt on. It comes for free.

This is called *active inference*, and in 2026 it jumped from neuroscience into AI as a
serious approach ([here's a 2026 paper](https://arxiv.org/abs/2606.22813)). Here's the
smallest demo that makes it click.

## The 10-second version

The task: a reward is hidden behind either the **LEFT** door or the **RIGHT** door (50/50).
There's also a **hint** you can check that tells you which door — *if you bother to look.*

| | ❌ Reward-chaser | ✅ Curious agent |
|---|---|---|
| What it cares about | getting the reward, right now | getting the reward **+ not being unsure** |
| What it does | guesses a door | checks the hint first, *then* opens the right door |
| Success (400 tries) | **48%** | **100%** |

Nobody told the second agent "go check the hint." It did it on its own, because being unsure
*bothered* it.

## How it works

Before acting, the agent scores each option on two things:

- **Does this get me closer to the reward?**
- **Does this make me less unsure about what's going on?**

```python
value_of_checking_the_hint = how_unsure_am_i    # high when it's a total coin-flip
value_of_just_guessing     = chance_of_being_right  # only ~50% on a blind guess

if value_of_checking_the_hint > value_of_just_guessing:
    check_the_hint()     # this is where curiosity shows up
open(best_door)          # now actually go get the reward
```

When it's a total coin-flip, checking the hint is worth a lot (it removes all the doubt),
way more than a 50/50 guess. So it looks first. Once it *knows*, there's nothing left to be
unsure about, so it just grabs the reward. The reward-chaser never sees any value in the
hint, so it flips a coin forever.

## Why this matters

Two reasons engineers should care:

1. **Curiosity for free.** A long-standing headache in AI is agents getting stuck doing the
   same thing, never trying anything new. People hand-tune "exploration bonuses" to force
   them to explore. This approach gives you curiosity automatically — the agent looks for
   info exactly when it's unsure, and stops once it isn't.

2. **It handles surprises.** An agent built to avoid surprises is built to deal with
   situations it wasn't trained for. When reality stops matching its expectations, closing
   that gap *becomes* its goal — so it keeps adapting instead of breaking.

> A reward-chaser asks "what gets me the most points?" A surprise-avoider asks "what don't I
> understand yet?" — and that second question is what makes it adapt.

## Try it

```bash
git clone https://github.com/Shridhar-2205/living-software
cd living-software/04-active-inference
python demo.py
```

Honest note: the full version of this idea has a fair bit of math behind it. I've boiled it
down to the one decision that makes it obvious — *being unsure has a cost* — so you can watch
curiosity appear in just a little code.

## The rest of the series — *Toward Living Software*

1. [I built an AI agent that rewrites its own code](https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-rewrites-its-own-code-in-150-lines-3jjo)
2. [Do AI agents need to sleep?](https://dev.to/shridhar_shah2297/do-ai-agents-need-to-sleep-i-built-one-that-does-53c4)
3. [Can an AI agent pass the Sally-Anne test?](https://dev.to/shridhar_shah2297/can-an-ai-agent-pass-the-test-we-give-4-year-olds-5825)
4. **An AI agent that gets curious on its own** (you're reading it)
5. [How do you trust an AI agent with your money?](https://dev.to/shridhar_shah2297/how-do-you-trust-an-ai-agent-with-your-money-you-dont-you-check-its-receipt-38ff)
6. [Agents that write their own SKILL.md files](https://dev.to/shridhar_shah2297/agents-are-learning-to-write-their-own-skillmd-files-3foo)

---

**Shridhar Shah** — Senior Software Engineer on the AI team at Cisco. Part 4 of *Toward Living Software*.

[GitHub](https://github.com/Shridhar-2205) · [LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)

> **Background:** Karl Friston's "Free Energy Principle" (the brain-science origin);
> "Active Inference as the Test-Time Scaling Law for Physical AI Agents" (arXiv:2606.22813).
