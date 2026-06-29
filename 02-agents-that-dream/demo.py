"""
Agents That Dream — does an AI agent need to "sleep"? (a simple demo)

Two agents learn the same facts over many noisy days, then take a memory test.
  - The no-sleep agent only keeps the last few notes, so old facts fall off and are lost.
  - The sleeping agent turns each day's notes into a running tally, then clears the notes.
    Because it counts what it heard across many days, the occasional wrong note gets
    outvoted by the truth.

Same experiences, same noise. Sleep is the only difference. Runs in under a second.
"""

import random

# The real facts we want the agent to remember.
TRUTH = {
    "Alice": "coffee",
    "Bob": "tea",
    "Carol": "water",
    "Dave": "juice",
}
WRONG_ANSWERS = ["soda", "milk", "beer"]


def make_one_day_of_notes(rng, count=12):
    """One day of observations. About 1 in 5 is wrong, like real-world logs."""
    notes = []
    for _ in range(count):
        person = rng.choice(list(TRUTH))
        if rng.random() < 0.2:
            drink = rng.choice(WRONG_ANSWERS)   # a mistaken note
        else:
            drink = TRUTH[person]               # the correct note
        notes.append((person, drink))
    return notes


def most_common(items):
    counts = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1
    return max(counts, key=counts.get)


class NoSleepAgent:
    """Remembers only the last few notes. Never tidies up."""

    def __init__(self, max_notes=10):
        self.max_notes = max_notes
        self.recent_notes = []

    def live_a_day(self, notes):
        self.recent_notes += notes
        # Keep only the most recent notes; older ones are forgotten.
        self.recent_notes = self.recent_notes[-self.max_notes:]

    def sleep(self):
        pass  # this agent never sleeps

    def recall(self, person):
        drinks = [drink for (p, drink) in self.recent_notes if p == person]
        return most_common(drinks) if drinks else None


class SleepingAgent:
    """Each night, folds the day's notes into a running tally, then clears the notes."""

    def __init__(self):
        self.todays_notes = []
        self.tally = {}  # person -> {drink: how many times we heard it}

    def live_a_day(self, notes):
        self.todays_notes += notes

    def sleep(self):
        for (person, drink) in self.todays_notes:
            counts = self.tally.setdefault(person, {})
            counts[drink] = counts.get(drink, 0) + 1
        self.todays_notes = []  # forget the raw notes, keep the tally

    def recall(self, person):
        counts = self.tally.get(person)
        return max(counts, key=counts.get) if counts else None


def test_memory(agent, days, seed):
    rng = random.Random(seed)
    for _ in range(days):
        agent.live_a_day(make_one_day_of_notes(rng))
        agent.sleep()
    correct = sum(agent.recall(person) == drink for person, drink in TRUTH.items())
    return correct / len(TRUTH)


def main():
    days = 30
    no_sleep = test_memory(NoSleepAgent(), days, seed=1)
    sleeping = test_memory(SleepingAgent(), days, seed=1)

    print("\nAgents That Dream — does an AI agent need to sleep?\n")
    print(f"  After {days} days of noisy facts, then a memory test:\n")
    print(f"   No-sleep agent (keeps only recent notes):  {no_sleep:.0%} correct")
    print(f"   Sleeping agent (tidies up each night):     {sleeping:.0%} correct\n")
    print("  The no-sleep agent forgets old facts and gets fooled by bad notes.")
    print("  The sleeping agent keeps a tidy summary, so facts stick and the noise")
    print("  gets outvoted. Same experiences. Sleep is the difference.\n")


if __name__ == "__main__":
    main()
