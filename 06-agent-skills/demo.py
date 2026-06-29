"""
Agents That Write Their Own Skills — SKILL.md, and where it's going (a simple demo).

Background: in late 2025 Anthropic introduced "Agent Skills" — a folder with a SKILL.md
file (some YAML at the top + Markdown instructions, plus optional scripts) that teaches an
agent how to do a task. It became an open standard (https://agentskills.io/specification).
The clever bit is "progressive disclosure": the agent only keeps each skill's short
*description* in memory, and reads the full instructions *only* when a task actually matches.

The SKILL.md files this demo writes are spec-compliant: required `name` (kebab-case, must
match the folder) and `description`, plus the optional `license` and `metadata` fields. The
same files would load unmodified in Claude Code, opencode, Goose, and other compatible CLIs.

This demo shows the next step the 2026 research is chasing: an agent that doesn't just
*read* skills a human wrote — it *writes its own*. When it solves something new the hard
way, it saves a real SKILL.md to disk. Next time a similar task shows up, it finds that
skill by its description and reuses it instantly.

We compare two agents over a stream of tasks:
  - No-skills agent: solves everything from scratch, every single time (slow).
  - Skill-writing agent: solves a new task once, writes a SKILL.md, then reuses it (fast).

It writes real SKILL.md files into a local ./skills folder so you can open them. Runs in
under a second, no API key.
"""

import os
import re
import shutil

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "skills")

# We pretend "figuring something out from scratch" is expensive, and "reusing a saved
# skill" is cheap. (In a real agent these are reasoning steps / tokens / dollars.)
COST_FROM_SCRATCH = 5
COST_REUSE = 1


# --- The three things an agent can learn to do. Each has: how to do it, and the SKILL.md
#     text it would save once it has figured the task out. ---

def do_csv_to_markdown(text):
    rows = [line.split(",") for line in text.splitlines() if line.strip()]
    header = "| " + " | ".join(rows[0]) + " |"
    divider = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join([header, divider] + body)


def do_slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def do_extract_emails(text):
    return ", ".join(re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))


# name -> (description, the function that does it, the SKILL.md instructions)
SKILL_SOURCE = {
    "csv-to-markdown": (
        "Turn comma-separated text into a Markdown table. Use when the input looks like "
        "CSV and the user wants a table.",
        do_csv_to_markdown,
        "Split the text into rows on newlines and columns on commas. Make the first row the\n"
        "header, add a `---` divider row, then format every row as `| a | b | c |`.",
    ),
    "slugify": (
        "Turn a title into a URL slug. Use when the user wants a slug, permalink, or "
        "filename from some text.",
        do_slugify,
        "Lowercase the text, replace every run of non-letter/number characters with a single\n"
        "hyphen, and trim hyphens from the ends.",
    ),
    "extract-emails": (
        "Pull all email addresses out of a blob of text. Use when the user wants the emails "
        "found in some text.",
        do_extract_emails,
        "Scan the text for anything shaped like `name@domain.tld` and return them as a\n"
        "comma-separated list.",
    ),
}


def is_valid_skill_name(name):
    """Validate a name against the Agent Skills open standard
    (https://agentskills.io/specification): 1-64 chars, lowercase a-z / 0-9 / hyphens,
    with no leading, trailing, or consecutive hyphens."""
    return 1 <= len(name) <= 64 and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) is not None


def write_skill_md(name):
    """Save a spec-compliant SKILL.md to ./skills/<name>/SKILL.md (the agent 'learning').

    Follows https://agentskills.io/specification: YAML frontmatter with the required
    `name` (kebab-case, must match the folder) and `description` fields, plus the optional
    `license` and `metadata` fields, then a Markdown body of instructions."""
    description, _, instructions = SKILL_SOURCE[name]
    assert is_valid_skill_name(name), f"name '{name}' breaks the Agent Skills spec"
    assert len(description) <= 1024, "description must be <= 1024 chars per the spec"

    folder = os.path.join(SKILLS_DIR, name)
    os.makedirs(folder, exist_ok=True)
    title = name.replace("-", " ").title()
    contents = (
        "---\n"
        f"name: {name}\n"                       # required: matches the folder name
        f"description: {description}\n"          # required: what it does + when to use it
        "license: Apache-2.0\n"                  # optional
        "metadata:\n"                            # optional
        "  author: skill-writing-agent\n"
        '  version: "1.0"\n'
        "---\n\n"
        f"# {title}\n\n"
        "## When to use\n"
        f"{description}\n\n"
        "## Steps\n"
        f"{instructions}\n"
    )
    with open(os.path.join(folder, "SKILL.md"), "w") as f:
        f.write(contents)


def installed_skill_names():
    """The 'discovery' step: list saved skills. (Progressive disclosure: in real life the
    agent reads only each skill's name + description here, not the full instructions.)"""
    if not os.path.isdir(SKILLS_DIR):
        return []
    return [n for n in os.listdir(SKILLS_DIR)
            if os.path.isfile(os.path.join(SKILLS_DIR, n, "SKILL.md"))]


class NoSkillsAgent:
    """Solves every task from scratch. Never saves anything."""

    def handle(self, task_name, text):
        _, solve, _ = SKILL_SOURCE[task_name]
        answer = solve(text)            # figured out the hard way...
        return answer, COST_FROM_SCRATCH, "solved from scratch"


class SkillWritingAgent:
    """Writes a SKILL.md the first time it solves something, then reuses it after."""

    def handle(self, task_name, text):
        _, solve, _ = SKILL_SOURCE[task_name]
        if task_name in installed_skill_names():
            answer = solve(text)        # found the saved skill -> cheap reuse
            return answer, COST_REUSE, f"reused skill '{task_name}'"
        answer = solve(text)            # first time: solve the hard way...
        write_skill_md(task_name)       # ...then save a SKILL.md so next time is cheap
        return answer, COST_FROM_SCRATCH, f"learned it and wrote SKILL.md for '{task_name}'"


# A stream of tasks. Notice several repeat — that's where reuse pays off.
TASKS = [
    ("csv-to-markdown", "name,age\nAlice,30\nBob,25", "| name | age |\n| --- | --- |\n| Alice | 30 |\n| Bob | 25 |"),
    ("slugify", "Hello World! My First Post", "hello-world-my-first-post"),
    ("csv-to-markdown", "city,pop\nDelhi,32", "| city | pop |\n| --- | --- |\n| Delhi | 32 |"),
    ("extract-emails", "ping a@b.com and c@d.org pls", "a@b.com, c@d.org"),
    ("slugify", "Another Cool Title", "another-cool-title"),
    ("csv-to-markdown", "x,y\n1,2", "| x | y |\n| --- | --- |\n| 1 | 2 |"),
    ("extract-emails", "team: x@y.io, z@w.net", "x@y.io, z@w.net"),
]


def run(agent):
    total_cost = 0
    log = []
    correct = 0
    for task_name, text, expected in TASKS:
        answer, cost, note = agent.handle(task_name, text)
        total_cost += cost
        correct += (answer == expected)
        log.append((task_name, cost, note))
    return total_cost, correct, log


def main():
    # Start clean so the demo is reproducible.
    shutil.rmtree(SKILLS_DIR, ignore_errors=True)

    no_skills_cost, no_skills_ok, _ = run(NoSkillsAgent())

    shutil.rmtree(SKILLS_DIR, ignore_errors=True)
    skill_cost, skill_ok, skill_log = run(SkillWritingAgent())

    print("\nAgents That Write Their Own Skills (SKILL.md)\n")
    print("  Same stream of 7 tasks. Cost = effort to get each one done.\n")
    for task_name, cost, note in skill_log:
        print(f"   [{cost}] {task_name:<16} {note}")

    print(f"\n   No-skills agent (re-solves every time):  cost {no_skills_cost}")
    print(f"   Skill-writing agent (learns + reuses):   cost {skill_cost}")
    print(f"   Both got {skill_ok}/{len(TASKS)} tasks correct.\n")

    # Every file it wrote follows the Agent Skills open standard.
    skills = installed_skill_names()
    all_valid = all(is_valid_skill_name(n) for n in skills)
    print(f"  It wrote {len(skills)} real SKILL.md files (open ./skills to read them).")
    print(f"  All {len(skills)} follow the agentskills.io spec (valid name + description): "
          f"{'yes' if all_valid else 'no'}.\n")

    # Progressive disclosure: why a big skill library stays cheap.
    body_tokens, desc_tokens = 500, 20  # rough sizes
    naive = len(skills) * body_tokens
    progressive = len(skills) * desc_tokens + body_tokens
    print("  Progressive disclosure keeps a big library cheap. To use ONE skill out of")
    print(f"  {len(skills)} installed:")
    print(f"     load every full skill:        ~{naive} tokens")
    print(f"     load descriptions + one body: ~{progressive} tokens  (the SKILL.md way)\n")


if __name__ == "__main__":
    main()
