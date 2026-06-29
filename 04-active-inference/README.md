# 🔎 The Curious Agent

An agent that gets **curious on its own**. Instead of only chasing reward, it also tries to
reduce its uncertainty — so it learns to gather information before acting. That takes it from
**48% → 100%** on a simple task. Part 2 adds a cost + an unreliable hint to show the
trade-off has no hidden "exploration knob."

No GPU, no API key. Runs in under a second.

## Run

```bash
python demo.py
```

## How it works (the flow)

```mermaid
flowchart TD
    A["Reward is behind LEFT or RIGHT (50/50). A HINT can reveal which."] --> B{"Is checking worth it? info-edge = (reliability - 0.5) x reward > cost?"}
    B -- yes --> C["Check the hint first"]
    C --> D["Open the door the hint points to"]
    B -- no --> E["Skip the hint → just guess a door"]
    D --> F["Score the round"]
    E --> F
    F --> G["Reward-chaser never checks → ~50%. Curious agent checks when it pays → up to 100%."]
```

**Steps:**
1. The reward hides behind one of two doors; a hint reveals which — if you look.
2. Before acting, the agent weighs **how much the hint improves its odds** against
   **what checking costs**.
3. If the edge beats the cost → check first, then open the right door.
4. If the hint is too noisy or too expensive → it skips and just guesses.
5. Curiosity isn't bolted on; it falls out of "being unsure has a cost" — and switches off
   on its own when checking wouldn't pay.
