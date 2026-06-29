# 🌱 Living Software — 6 Tiny, Runnable AI-Agent Demos (2026)

> A 6-part blog series of tiny, runnable POCs on the frontier of **self-improving AI
> agents** — software that evolves, dreams, models other minds, gets curious, writes its
> own skills, and proves itself. Each one runs on a laptop in seconds (no GPU, no API key
> needed) and is grounded in a 2026 research paper.

**Repo:** [github.com/Shridhar-2205/living-software](https://github.com/Shridhar-2205/living-software)
— ⭐ star it if you find it useful.

**Topics:** `ai-agents` · `llm` · `agent-memory` · `theory-of-mind` · `active-inference` ·
`self-improving-agents` · `agent-skills` · `python`

The thesis: we spent a decade making AI models *bigger*. The 2026 frontier is making them
*alive-like* — improving at **runtime**, not just at training time. Each post is one glimpse
of that shift, with code you can run in under a minute.

## The series

| # | Post | The idea | Grounded in (2026) |
|---|------|----------|--------------------|
| 1 | [The Agent That Rewrites Its Own Code](01-self-rewriting-agent/) | An agent edits its own code and keeps only changes that verifiably score higher → climbs 1/8 → 8/8 | Darwin Gödel Machine (arXiv:2505.22954) |
| 2 | [Agents That Dream](02-agents-that-dream/) | A "sleep" phase consolidates noisy daily experience into durable memory → 75% vs 100% recall | "Do Language Models Need Sleep?" (2605.26099) |
| 3 | [An Agent With a Theory of Mind](03-theory-of-mind/) | Passes the Sally-Anne false-belief test by modeling *other minds*, not just reality | Theory of Mind in LLMs (Kosinski, PNAS / arXiv:2302.02083; arXiv:2602.22072) |
| 4 | [The Surprise-Minimizing Agent](04-active-inference/) | Active inference: curiosity emerges for free → 48% vs 100% on a foraging task | Active Inference as the Test-Time Scaling Law for Physical AI Agents (arXiv:2606.22813) |
| 5 | [Verifiable Agent Behavior](05-verifiable-agent/) | Cryptographic proof an agent ran the *approved* policy → swap/edit/forge all rejected | Verifiable ML via zkSNARKs (arXiv:2402.02675; survey arXiv:2502.18535) |
| 6 | [Agents That Write Their Own Skills](06-agent-skills/) | An agent solves a task once, writes a real `SKILL.md`, then reuses it → cost 35 vs 19 | Agent Skills standard + MUSE-Autoskill / Skill-Pro (2026) |

### The gist of all blogs

- **Rewrites its own code** — fixes its own bugs by trying a change, running a test, and
  keeping it only if the score improves (like keeping only the homework edits that raise your
  grade).
- **Agents that dream** — gets a nightly "sleep" step that replays the day and saves a tidy
  summary, just like your brain, so it remembers what matters instead of drowning in notes.
- **Theory of mind** — learns that other people can believe wrong things: it predicts where
  someone will *look* for an object, not where the object actually is.
- **Surprise-minimizing** — give it one goal, "avoid surprises," and curiosity appears on its
  own: it checks the hint before guessing, so it's right every time. Nobody programmed that in.
- **Verifiable behavior** — hands you a tamper-proof "receipt" proving it followed the exact
  rules you approved; swapping, editing, or forging anything gets rejected.
- **Writes its own skills** — writes a how-to note (`SKILL.md`), solves a task once, then
  reuses the recipe forever — so it gets cheaper and faster instead of re-solving the same thing.

## Run any of them

```bash
cd 01-self-rewriting-agent && python demo_cli.py   # or python dgm.py
cd 02-agents-that-dream     && python demo.py
cd 03-theory-of-mind        && python demo.py
cd 04-active-inference      && python demo.py
cd 05-verifiable-agent      && python demo.py
cd 06-agent-skills          && python demo.py
```

Each folder has a `BLOG.md` (the write-up) and a small, intentionally simple demo. These are
POCs: the *mechanism* is faithful to the paper, the implementation is kept tiny on purpose.

---

*By **Shridhar Shah**, Senior Software Engineer at Outshift by Cisco — I work on AI agents,
RAG, and cognition. [GitHub](https://github.com/Shridhar-2205) ·
[LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)*
