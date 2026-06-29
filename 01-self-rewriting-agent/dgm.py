"""
The Agent That Rewrites Its Own Code (a small, simple demo).

The idea (from a 2025 paper called the "Darwin Gödel Machine"): instead of a human fixing
the program, the program fixes itself. It looks at the tasks it's failing, adds a skill to
try to fix them, runs a test, and keeps the change ONLY if the test score went up. It also
saves every improved version so it can build on any of them later.

Our agent starts knowing one skill and teaches itself the rest, going from 1/8 to 8/8.
Runs in under a second. No special hardware, no API key.
"""

import random


# --- The skills an agent can have. Each one just transforms a piece of text. ---
# The agent starts with almost none of these and has to teach itself the rest.

def clean_up(text):
    # Trim and fix weird spacing: "  the   fox " -> "the fox"
    return " ".join(text.split())


def do_uppercase(text):
    return text.upper()


def do_reverse(text):
    return text[::-1]


def do_title(text):
    return text.title()  # "hello world" -> "Hello World"


def do_sort_csv(text):
    parts = [p.strip() for p in text.split(",") if p.strip() != ""]
    return ",".join(sorted(parts))


def do_sum_csv(text):
    numbers = [int(p) for p in text.split(",") if p.strip() != ""]
    return str(sum(numbers))


def do_dedup_csv(text):
    seen = []
    for p in text.split(","):
        if p not in seen:
            seen.append(p)
    return ",".join(seen)


SKILLS = {
    "uppercase": do_uppercase,
    "reverse": do_reverse,
    "title": do_title,
    "sort_csv": do_sort_csv,
    "sum_csv": do_sum_csv,
    "dedup_csv": do_dedup_csv,
}

# "title" only works right on clean text, so it needs the cleanup skill first.
# This is what makes one fix unlock another later on.
NEEDS_CLEANUP = {"title"}
CLEANUP_SKILL = "normalize_inputs"


# --- The test. Each task has a known correct answer, so scoring is just "==". ---
# A few tasks have messy spacing and only pass once the agent learns the cleanup skill.
# Each task is (skill_to_use, input_text, correct_answer).
BENCHMARK = [
    ("uppercase", "hello", "HELLO"),
    ("reverse", "abcd", "dcba"),
    ("dedup_csv", "a,a,b,b,c", "a,b,c"),
    ("sort_csv", " 3, 1 , 2 ", "1,2,3"),
    ("sum_csv", " 1 , 2 , 3 ", "6"),
    ("title", "hello world", "Hello World"),
    ("title", "  the   quick brown   fox ", "The Quick Brown Fox"),
    ("title", "a  TALE   of two  cities", "A Tale Of Two Cities"),
]


class Agent:
    """An agent is just the set of skills it has learned (plus a history of what it added)."""

    def __init__(self, skills, history=None):
        self.skills = set(skills)
        self.history = list(history) if history else []

    def run(self, skill, text):
        if skill not in self.skills:
            return None  # it simply can't do this yet
        if skill in NEEDS_CLEANUP and CLEANUP_SKILL in self.skills:
            text = clean_up(text)
        return SKILLS[skill](text)


def score_agent(agent):
    """Run every task and count how many the agent gets exactly right."""
    score = 0
    failed = []
    for skill, text, correct_answer in BENCHMARK:
        if agent.run(skill, text) == correct_answer:
            score += 1
        else:
            failed.append((skill, text, correct_answer))
    return score, failed


def pick_next_fix(agent, failed):
    """Look at what's failing and choose ONE skill to add next."""
    needs_cleanup = False
    missing_skills = []
    for skill, text, correct_answer in failed:
        if skill not in agent.skills:
            missing_skills.append(skill)
        elif skill in NEEDS_CLEANUP and CLEANUP_SKILL not in agent.skills:
            # It HAS the skill but still fails because the text is messy -> add cleanup.
            needs_cleanup = True

    if needs_cleanup:
        return CLEANUP_SKILL
    if missing_skills:
        return sorted(set(missing_skills))[0]
    return None


def evolve(generations=80, seed=7):
    """The self-improvement loop: try a fix, keep it only if the score goes up."""
    random.seed(seed)
    total = len(BENCHMARK)

    base = Agent({"uppercase"}, ["start: only knows uppercase"])
    base_score, _ = score_agent(base)

    # The archive remembers every improved version, so we can branch from any of them.
    # We use the set of skills as the key so we never store the same version twice.
    archive = [base]
    best = base
    best_score = base_score
    history = []  # a log of every attempt, for the tests and the write-up

    for gen in range(1, generations + 1):
        # Pick a version to improve. Favor the better ones, but allow weaker ones too.
        weights = [score_agent(a)[0] + 1 for a in archive]
        parent = random.choices(archive, weights=weights, k=1)[0]
        parent_score, failed = score_agent(parent)

        fix = pick_next_fix(parent, failed)
        if fix is None:
            continue

        child = Agent(parent.skills | {fix}, parent.history + [f"added {fix}"])
        child_score, _ = score_agent(child)

        already_have_it = any(a.skills == child.skills for a in archive)
        keep_it = child_score > parent_score and not already_have_it
        history.append({
            "generation": gen, "fix": fix,
            "parent_score": parent_score, "child_score": child_score, "kept": keep_it,
        })

        if keep_it:
            archive.append(child)
            if child_score > best_score:
                best, best_score = child, child_score

        if best_score == total:
            break

    return {
        "base_score": base_score,
        "best": best,
        "best_score": best_score,
        "total": total,
        "archive": archive,
        "history": history,
    }


if __name__ == "__main__":
    result = evolve()
    print(f"Start score:             {result['base_score']}/{result['total']}")
    print(f"After improving itself:  {result['best_score']}/{result['total']}")
    print("What it taught itself:")
    for step in result["best"].history:
        print(f"  - {step}")
    print(f"Versions it kept along the way: {len(result['archive'])}")
