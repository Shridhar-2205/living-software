"""
The claims, as simple tests. The whole demo rests on a test score, so the claims
("it starts weak", "it ends perfect", "it never keeps a change that made things worse")
are just asserts you can run.

    pip install pytest
    pytest -q
"""

from dgm import BENCHMARK, CLEANUP_SKILL, Agent, evolve, score_agent


def test_it_starts_weak():
    base = Agent({"uppercase"})
    score, _ = score_agent(base)
    assert score < len(BENCHMARK) // 2


def test_it_improves_itself():
    result = evolve()
    assert result["best_score"] > result["base_score"]


def test_it_reaches_a_perfect_score():
    result = evolve()
    assert result["best_score"] == result["total"]


def test_it_never_keeps_a_bad_change():
    # Every change it kept must have raised the score (its rule instead of a proof).
    result = evolve()
    for attempt in result["history"]:
        if attempt["kept"]:
            assert attempt["child_score"] > attempt["parent_score"]


def test_one_fix_unlocks_another():
    # The cleanup skill does nothing alone, but pays off once 'title' is present.
    base = Agent({"uppercase"})
    cleanup_only = Agent({"uppercase", CLEANUP_SKILL})
    title_only = Agent({"uppercase", "title"})
    both = Agent({"uppercase", "title", CLEANUP_SKILL})

    assert score_agent(cleanup_only)[0] == score_agent(base)[0]   # cleanup alone: no gain
    assert score_agent(both)[0] > score_agent(title_only)[0]      # together: a gain


def test_same_seed_gives_same_result():
    assert evolve(seed=7)["best_score"] == evolve(seed=7)["best_score"]
