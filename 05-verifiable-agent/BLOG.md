---
title: "How Do You Trust an AI Agent With Your Money? You Don't — You Check Its Receipt"
subtitle: "Cryptographically verifiable agent behavior: swap, edit, or forge a step and it's rejected."
slug: verifiable-ai-agent-behavior
tags: artificial-intelligence, security, programming, python
ignorePost: false  # weekly drip — flip to false (or delete) to release this post
cover: https://cdn.jsdelivr.net/gh/Shridhar-2205/living-software@main/assets/covers/cover-05.png
canonical: https://dev.to/shridhar_shah2297/how-do-you-trust-an-ai-agent-with-your-money-you-dont-you-check-its-receipt-38ff
seoTitle: "How to Trust an AI Agent: Check Its Receipt"
seoDescription: "A hands-on demo of cryptographically verifiable agent behavior — a tamper-evident receipt proving an agent ran the approved policy."
---

**TL;DR:** We're about to hand agents our refunds, our data, and our prod APIs — and that
made me nervous enough to build this. Once agents do real things, "just trust it" stops being
good enough. The fix: the agent hands you a tamper-proof **receipt** that proves it followed
the *approved* rules and didn't fake anything. Change the rules, edit a step, or fake the
signature, and the check fails every time. Normal everyday crypto, no API key.

---

## The scary question

You're about to let an agent issue refunds, move files, or hit your production APIs. How do
you *actually know* it followed the rules you approved — and not some changed version? And
how do you know the log it gives you afterward wasn't edited?

Right now, the honest answer is usually: you don't. You trust the logs. But logs can be
edited, the rules an agent runs can be quietly swapped, and a compromised agent can claim it
did one thing while doing another.

The 2026 fix is called **verifiable agent behavior** (the research term is "zkML"): the
agent produces a tamper-proof receipt that proves it ran *exactly* the approved process —
and *anyone* can check that receipt without having to trust the agent.

## The 10-second version

| What happened | Result |
|---|---|
| Agent ran the approved refund rules, honestly | ✅ **ACCEPT** |
| Someone swapped in sneaky "refund anything" rules | 🚨 **REJECT** — rules don't match the approved ones |
| Someone edited a step (turned a $40 refund into $5000) | 🚨 **REJECT** — receipt doesn't add up |
| Someone faked the receipt without the secret key | 🚨 **REJECT** — signature is invalid |

Only the honest run passes. Every kind of cheating gets caught.

## How it works (in plain terms)

Three normal building blocks, no magic:

1. **A fingerprint of the approved rules.** Run the rules through a hashing function and you
   get a short, unique fingerprint. Anyone can fingerprint the *approved* rules and compare —
   if the agent used different rules, the fingerprints won't match.

2. **A receipt you can't edit.** Every step the agent takes is chained together so each step
   depends on all the steps before it. Change any one step and the whole thing stops adding
   up — like a tamper-evident seal:

```python
seal = fingerprint(rules)
for step in steps:
    seal = hash(seal + step)   # each step folds into the seal
```

3. **A signature.** The agent signs the final seal with a secret key. If someone tries to
   forge a receipt without that key, the signature won't check out.

To verify, you just redo all three and ask: *Did it use the approved rules? Is the receipt
intact? Is the signature real?* All three have to pass.

## Why this matters

Every other post in this series makes agents *more independent* — they rewrite their own
code, sleep, model other people, get curious. This one is the safety net for all of that:
**independence without a way to check up on it is a liability.**

> The more power we hand to agents, the less we can afford to just trust them — and the more
> we need a way to *check* them.

The end goal of the real research is even stronger: prove an agent followed the approved
rules **without re-running it and without exposing any private data or secret model.** That
lets two companies trust each other's agents — yours proves it behaved, mine checks the
proof, and neither of us has to reveal our secrets.

## Try it

```bash
git clone https://github.com/Shridhar-2205/living-software
cd living-software/05-verifiable-agent
python demo.py
```

Honest note: the real research uses heavier cryptography so the checker doesn't have to
re-run anything and never sees the secret model. My demo re-checks a signed, sealed receipt
instead — much simpler, and it shows the same payoff (cheat in any way ⇒ rejected) so you
can feel what "verifiable behavior" actually buys you. It uses only standard, modern hashing
(SHA-256), and the "secret key" is an obvious fake, never a real credential.

## The rest of the series — *Toward Living Software*

1. [I built an AI agent that rewrites its own code](https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-rewrites-its-own-code-in-150-lines-3jjo)
2. [Do AI agents need to sleep?](https://dev.to/shridhar_shah2297/do-ai-agents-need-to-sleep-i-built-one-that-does-53c4)
3. [Can an AI agent pass the Sally-Anne test?](https://dev.to/shridhar_shah2297/can-an-ai-agent-pass-the-test-we-give-4-year-olds-5825)
4. [An AI agent that gets curious on its own](https://dev.to/shridhar_shah2297/i-built-an-ai-agent-that-gets-curious-on-its-own-4oe1)
5. **How do you trust an AI agent with your money?** (you're reading it)
6. [Agents that write their own SKILL.md files](https://dev.to/shridhar_shah2297/agents-are-learning-to-write-their-own-skillmd-files-3foo)

---

**Shridhar Shah** — Senior Software Engineer on the AI team at Cisco. Part 5 (the finale) of *Toward Living Software*.

[GitHub](https://github.com/Shridhar-2205) · [LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)

> **Background:** "zkML" / verifiable inference — proving an AI model ran exactly as claimed.
> See "Verifiable evaluations of machine learning models using zkSNARKs"
> ([arXiv:2402.02675](https://arxiv.org/abs/2402.02675)) and the survey "Zero-Knowledge Proof
> Based Verifiable Machine Learning" ([arXiv:2502.18535](https://arxiv.org/abs/2502.18535)).
> Tools like [EZKL](https://docs.ezkl.xyz/) do this for real ONNX models today.
