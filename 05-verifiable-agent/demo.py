"""
Verifiable Agent Behavior — the agent hands you a receipt you can check (a simple demo).

When an agent does something important (like a refund), how do you know it followed the
approved rules and didn't fake its log? Answer: it produces a tamper-proof "receipt", and
anyone can check it.

The receipt has three parts:
  1. A fingerprint of the rules it used (so you can tell if it used the approved ones).
  2. A "seal" that chains every step together, so editing any step breaks it.
  3. A signature made with a secret key, so a faked receipt won't check out.

Try to cheat — swap the rules, edit a step, or fake the signature — and the check fails.
Uses only standard hashing (SHA-256). No API key. The "secret key" here is an obvious fake.
"""

import hashlib
import hmac
import os

# In real life this lives in a secure vault. Here it's a clearly-fake placeholder.
SECRET_KEY = os.getenv("AGENT_SIGNING_KEY", "DEMO-ONLY-NOT-A-REAL-KEY").encode()


def fingerprint(text):
    """A short, unique fingerprint of some text (a SHA-256 hash)."""
    return hashlib.sha256(text.encode()).hexdigest()


# The rules that were officially approved.
APPROVED_RULES = "refund only if amount <= 50 and the order is verified"
APPROVED_FINGERPRINT = fingerprint(APPROVED_RULES)


def run_agent(rules, request):
    """Run the agent and produce a receipt of what it did."""
    decision = "approve" if "amount=40" in request else "deny"
    refund = "issue_refund(40)" if decision == "approve" else "none"
    steps = [
        ("rules", rules),
        ("request", request),
        ("decision", decision),
        ("refund", refund),
    ]

    # Build the seal: fold each step into a running hash so changing any step breaks it.
    seal = fingerprint(rules)
    for name, value in steps:
        seal = fingerprint(seal + "|" + name + "=" + value)

    # Sign the seal with the secret key.
    signature = hmac.new(SECRET_KEY, seal.encode(), hashlib.sha256).hexdigest()

    return {
        "rules_fingerprint": fingerprint(rules),
        "steps": steps,
        "seal": seal,
        "signature": signature,
    }


def check_receipt(receipt):
    """Re-check the receipt from scratch. Returns (ok, reason)."""
    # 1. Did it use the approved rules?
    if receipt["rules_fingerprint"] != APPROVED_FINGERPRINT:
        return False, "the rules don't match the approved ones"

    # 2. Rebuild the seal from the steps — catches any edited step.
    seal = receipt["rules_fingerprint"]
    for name, value in receipt["steps"]:
        seal = fingerprint(seal + "|" + name + "=" + value)
    if seal != receipt["seal"]:
        return False, "a step was changed (the receipt doesn't add up)"

    # 3. Is the signature real? (compare_digest avoids timing leaks)
    expected = hmac.new(SECRET_KEY, receipt["seal"].encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, receipt["signature"]):
        return False, "the signature is fake"

    return True, "all good: approved rules, receipt intact, real signature"


def show(label, result):
    ok, reason = result
    mark = "ACCEPT" if ok else "REJECT"
    print(f"   [{mark}] {label}")
    print(f"            -> {reason}")


def main():
    print("\nVerifiable Agent Behavior — prove the agent followed the approved rules\n")

    # 1) Honest run with the approved rules.
    honest = run_agent(APPROVED_RULES, "refund request: amount=40, order verified")
    show("Honest run, approved rules", check_receipt(honest))

    # 2) Someone swaps in sneaky rules that refund anything.
    rogue = run_agent("always refund any amount", "refund request: amount=5000")
    show("Swapped in sneaky rules", check_receipt(rogue))

    # 3) Someone edits a step after the fact (turns a $40 refund into $5000).
    tampered = dict(honest)
    tampered["steps"] = list(honest["steps"])
    tampered["steps"][3] = ("refund", "issue_refund(5000)")
    show("Edited a step afterward", check_receipt(tampered))

    # 4) Someone fakes the receipt without the secret key.
    forged = run_agent(APPROVED_RULES, "refund request: amount=40, order verified")
    forged["signature"] = "0" * 64
    show("Faked signature (no key)", check_receipt(forged))

    print("\n  Only the honest run passes. Swap the rules, edit a step, or fake the")
    print("  signature and the check fails. Don't trust the agent — check the receipt.\n")


if __name__ == "__main__":
    main()
