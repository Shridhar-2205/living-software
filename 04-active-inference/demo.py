"""
The Curious Agent — curiosity that shows up on its own (a simple demo).

A reward is hidden behind the LEFT or RIGHT door (50/50). There's also a HINT you can
check that tells you which door — if you bother to look.

  - The reward-chaser just guesses a door -> about 50%.
  - The curious agent hates being unsure, so it checks the hint first, then opens the
    right door -> 100%. Nobody told it to gather information; it does it because being
    unsure bothers it more than a coin-flip guess is worth.

This is a tiny taste of "active inference": act to avoid surprises, and curiosity comes
for free. Runs in under a second.

PART 2 answers the obvious follow-up: what if checking the hint COSTS something, or the
hint sometimes LIES (say it's only 70% reliable)? The agent still decides with one rule and
no "exploration knob": check only when the extra reward the hint buys beats what it costs.
So curiosity switches OFF on its own when it isn't worth it.
"""

import random


def other(door):
    return "right" if door == "left" else "left"


def play_one_round(check_the_hint_first, rng):
    reward_door = rng.choice(["left", "right"])
    if check_the_hint_first:
        guess = reward_door            # the hint reveals the correct door
    else:
        guess = rng.choice(["left", "right"])  # a blind guess
    return guess == reward_door


class RewardChaser:
    """Only cares about the reward right now. A guess is 'good enough', so it never checks."""

    def will_check_the_hint(self):
        return False


class CuriousAgent:
    """Hates being unsure. When it's a coin-flip, checking the hint beats guessing."""

    def will_check_the_hint(self):
        how_unsure = 1.0            # totally unsure which door (it's 50/50)
        chance_if_guessing = 0.5   # a blind guess is right only half the time
        return how_unsure > chance_if_guessing


def test_agent(agent, rounds, seed):
    rng = random.Random(seed)
    wins = sum(play_one_round(agent.will_check_the_hint(), rng) for _ in range(rounds))
    return wins / rounds


def hint_is_worth_it(reliability, cost, reward):
    """The whole decision, in one line and in 'reward points' — no exploration knob.

    A blind guess wins half the time. A hint that's right `reliability` of the time lifts
    your odds to `reliability`. So the EXTRA reward the hint buys you is:

        info_edge = (reliability - 0.5) * reward

    Check the hint only if that edge beats what checking costs you. That's it. Perfect free
    hint -> always worth it. Noisy or pricey hint -> the agent skips it on its own.
    """
    info_edge = (reliability - 0.5) * reward
    return info_edge > cost


def play_costed(check, reliability, cost, reward, rng):
    reward_door = rng.choice(["left", "right"])
    score = 0.0
    if check:
        score -= cost                                  # checking the hint costs a move
        hint_correct = rng.random() < reliability      # the hint lies (1 - reliability) of the time
        opened = reward_door if hint_correct else other(reward_door)
    else:
        opened = rng.choice(["left", "right"])         # blind guess
    won = opened == reward_door
    if won:
        score += reward
    return score, won


def run_scenario(reliability, cost, reward, rounds, seed):
    check = hint_is_worth_it(reliability, cost, reward)
    rng = random.Random(seed)
    results = [play_costed(check, reliability, cost, reward, rng) for _ in range(rounds)]
    success = sum(won for _, won in results) / rounds
    net = sum(score for score, _ in results) / rounds
    return check, success, net


def main():
    rounds = 400
    chaser = test_agent(RewardChaser(), rounds, seed=3)
    curious = test_agent(CuriousAgent(), rounds, seed=3)

    print("\nThe Curious Agent\n")
    print("  Find the reward behind LEFT or RIGHT. A hint reveals which — if you check it.")
    print(f"  Over {rounds} rounds:\n")
    print(f"   Reward-chaser (just guesses):   {chaser:.0%} success")
    print(f"   Curious agent (checks hint):    {curious:.0%} success\n")
    print("  Nobody told the curious agent to 'go get information'. It checks the hint")
    print("  because being unsure bothers it. Curiosity falls out on its own.\n")

    print("-" * 72)
    print("\nPART 2: what if the hint COSTS something, or it sometimes LIES?\n")
    print("  Reward for the right door = 1.00 point. The agent uses ONE rule:")
    print("    check only if  (reliability - 0.5) x reward  >  cost")
    print("    i.e. 'the edge the hint buys me' must beat 'what the move costs me'.\n")
    reward = 1.0
    scenarios = [
        (1.00, 0.00),   # perfect, free hint  -> obviously check
        (0.70, 0.00),   # lies 30% but free   -> still worth it
        (0.70, 0.15),   # lies 30%, cheap     -> still worth it
        (0.70, 0.30),   # lies 30%, pricey    -> NOT worth it, skip
        (0.55, 0.10),   # barely better, pricey -> skip
    ]
    print(f"   {'hint reliability':<18}{'cost to check':<15}{'agent decides':<16}{'success':<10}{'net score'}")
    print(f"   {'-'*16:<18}{'-'*13:<15}{'-'*14:<16}{'-'*8:<10}{'-'*9}")
    for reliability, cost in scenarios:
        check, success, net = run_scenario(reliability, cost, reward, rounds, seed=7)
        decision = "CHECK" if check else "SKIP -> guess"
        cost_label = "0.00 (free)" if cost == 0 else f"{cost:.2f}"
        print(f"   {reliability:<18.0%}{cost_label:<15}{decision:<16}{success:<10.0%}{net:.2f}")
    print("\n  Same rule every row. Curiosity is still 'free' (no exploration weight) — but")
    print("  now you can see it pays for itself, and switches OFF when it wouldn't.\n")


if __name__ == "__main__":
    main()
