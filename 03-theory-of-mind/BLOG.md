---
title: "Can an AI Agent Pass the Test We Give 4-Year-Olds?"
subtitle: "Theory of Mind and the Sally-Anne false-belief test, in plain Python."
slug: can-an-ai-agent-pass-the-sally-anne-test
tags: artificial-intelligence, machine-learning, programming, python
ignorePost: false  # weekly drip — flip to false (or delete) to release this post
cover: https://cdn.jsdelivr.net/gh/Shridhar-2205/living-software@main/assets/covers/cover-03.png
canonical: https://dev.to/shridhar_shah2297/can-an-ai-agent-pass-the-test-we-give-4-year-olds-5825
seoTitle: "Can an AI Agent Pass the Sally-Anne Test?"
seoDescription: "An agent with a Theory of Mind models what other people believe, not just reality — and passes the classic Sally-Anne false-belief test."
---

**TL;DR:** There's a famous test that kids pass around age 4, and a lot of AI still trips on
it — I had to build it to see where the line really is. It checks whether you understand that
*other people can believe things that aren't true.* I built two AI agents: one that only
knows "what's actually happening" (fails, like a toddler) and one that keeps track of what
*each person* believes (passes). It's the foundation for agents that can actually work
*together*.

---

## The test

1. Sally puts her marble in the **basket**, then leaves the room.
2. While she's gone, Anne moves the marble to the **box**.
3. Sally comes back. **Where will she look for her marble?**

If you said *basket*, nice — you just used something called "theory of mind." Sally never
saw the marble move, so in her head it's still in the basket. What's *actually* true (it's in
the box) and what *Sally believes* (it's in the basket) are two different things, and you
kept them separate without even thinking about it.

A 3-year-old says "box" — they can't yet separate what *they* know from what *Sally* knows.
A 4-year-old says "basket." It's one of the most famous tests in child psychology, and in
2026 it's become a real test for AI agents too.

## The 10-second version

| | ❌ Agent with no "theory of mind" | ✅ Agent that models other minds |
|---|---|---|
| What it tracks | only what's actually true | what *each person* believes, separately |
| Where will Sally look? | "box" | "basket" |
| Result | FAIL (only knows reality) | **PASS** |

## How it works (the whole trick)

The only difference between the two agents is one rule: **a person's belief only updates
when that person is actually in the room to see it happen.**

```python
def someone_moves_the_marble(new_place, who_is_watching):
    for person in who_is_watching:        # only people in the room
        beliefs[person] = new_place        # update THEIR mental picture
```

So when Anne moves the marble while Sally is out, only Anne's mental picture updates. Sally's
is frozen at "basket." Ask the simple agent and it just reports reality ("box"). Ask the
smarter agent and it answers from *Sally's* point of view ("basket").

That's the whole thing. But keeping a separate picture of "what does each *other* person
know" is the difference between an agent that's a good teammate and one that isn't.

## Why this isn't just a cute puzzle

Almost everything useful about multiple agents (or an agent working with a human) needs this:

- **Handing off work:** to delegate, I need to know what you already know.
- **Explaining things:** I should tell you the part you're *missing*, not dump everything.
- **Warning someone:** "Heads up, Sally still thinks the marble's in the basket" only works
  if I can track Sally's wrong belief.
- **Not causing chaos:** an agent that assumes everyone knows what *it* knows will skip
  important info and make bad assumptions.

Most AI today reasons about *the world*. The 2026 shift is reasoning about *the people in the
world* — including when they're wrong. That's what turns a smart tool into a real
collaborator.

> Being smart about the world makes a good tool. Being smart about *other people* makes a
> good teammate.

## Try it

```bash
git clone https://github.com/Shridhar-2205/living-software
cd living-software/03-theory-of-mind
python demo.py
```

Honest note: real versions have to *figure out* what someone believes by watching their
behavior, which is much harder. Here I just tell the agent who was in the room, so the core
idea — track beliefs separately from reality — is as clear as possible.

## The rest of the series — *Toward Living Software*

1. [I built an AI agent that rewrites its own code](https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-rewrites-its-own-code-in-150-lines-3jjo)
2. [Do AI agents need to sleep?](https://dev.to/shridhar_shah2297/do-ai-agents-need-to-sleep-i-built-one-that-does-53c4)
3. **Can an AI agent pass the Sally-Anne test?** (you're reading it)
4. [An AI agent that gets curious on its own](https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-gets-curious-on-its-own-4oe1)
5. [How do you trust an AI agent with your money?](https://dev.to/shridhar_shah2297/how-do-you-trust-an-ai-agent-with-your-money-you-dont-you-check-its-receipt-38ff)
6. [Agents that write their own SKILL.md files](https://dev.to/shridhar_shah2297/agents-are-learning-to-write-their-own-skillmd-files-3foo)

---

**Shridhar Shah** — Senior Software Engineer on the AI team at Cisco. Part 3 of *Toward Living Software*.

[GitHub](https://github.com/Shridhar-2205) · [LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)

> **Background:** the Sally-Anne false-belief test (Baron-Cohen, Leslie & Frith, 1985);
> Kosinski, "Evaluating Large Language Models in Theory of Mind Tasks" (PNAS 2024 /
> [arXiv:2302.02083](https://arxiv.org/abs/2302.02083)); and a 2026 follow-up showing how
> brittle this still is — "Understanding Artificial Theory of Mind"
> ([arXiv:2602.22072](https://arxiv.org/abs/2602.22072)).
