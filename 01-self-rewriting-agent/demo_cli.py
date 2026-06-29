"""
A simple terminal demo: watch the agent teach itself, going from 1/8 to 8/8.

    python demo_cli.py
"""

import time

from dgm import Agent, evolve, score_agent


def bar(score, total, width=24):
    filled = int(width * score / total)
    return "#" * filled + "." * (width - filled)


def main():
    result = evolve()
    total = result["total"]

    print("\nThe Agent That Rewrites Its Own Code")
    print("It edits its own code and keeps only the changes that make the score go up.\n")

    # Start with just the one skill, then replay each fix the winner taught itself.
    skills = {"uppercase"}
    score, _ = score_agent(Agent(skills))
    print(f"  start (only 'uppercase')".ljust(34) + f"[{bar(score, total)}] {score}/{total}")

    for step in result["best"].history:
        if not step.startswith("added "):
            continue
        skill = step[len("added "):]
        skills.add(skill)
        score, _ = score_agent(Agent(skills))
        time.sleep(0.4)
        print(f"  it adds '{skill}'".ljust(34) + f"[{bar(score, total)}] {score}/{total}")

    print(f"\n  Done: {score}/{total}. The agent wrote every one of those fixes itself.\n")


if __name__ == "__main__":
    main()
