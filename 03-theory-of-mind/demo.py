"""
An Agent With a Theory of Mind — the Sally-Anne test, in simple code.

The test kids pass around age 4:
  1. Sally puts her marble in the BASKET, then leaves the room.
  2. While she's gone, Anne moves it to the BOX.
  3. Sally comes back. Where will she look?

Right answer: BASKET. Sally never saw it move, so she still believes it's in the basket.
What's really true (box) and what Sally believes (basket) are different things.

  - The simple agent only tracks what's really true -> says "box" (fails, like a toddler).
  - The smart agent tracks what EACH person believes -> says "basket" (passes).

The only trick: a person's belief updates only when they're in the room to see it happen.
"""


def run_the_test():
    # What's REALLY true about where the marble is.
    real_location = {}
    # What each PERSON believes about where the marble is.
    beliefs = {"Sally": {}, "Anne": {}}

    def move_marble(place, people_in_the_room):
        real_location["marble"] = place
        for person in people_in_the_room:
            beliefs[person]["marble"] = place  # only people who see it update their belief

    # 1. Sally puts the marble in the basket. Both are in the room.
    move_marble("basket", ["Sally", "Anne"])
    # 2. Sally leaves. 3. Anne moves it to the box. Only Anne sees this.
    move_marble("box", ["Anne"])

    return real_location, beliefs


def main():
    real_location, beliefs = run_the_test()
    correct_answer = "basket"

    # The simple agent just reports reality.
    simple_answer = real_location["marble"]
    # The smart agent answers from Sally's point of view.
    smart_answer = beliefs["Sally"]["marble"]

    print("\nThe Sally-Anne test\n")
    print("  Sally hides her marble in the BASKET, then leaves.")
    print("  Anne secretly moves it to the BOX. Sally comes back.")
    print("  Q: where will Sally look for her marble?\n")

    simple_result = "PASS" if simple_answer == correct_answer else "FAIL (only knows reality)"
    smart_result = "PASS (it tracks Sally's belief)" if smart_answer == correct_answer else "FAIL"
    print(f"   Simple agent (knows only reality):  '{simple_answer}'   {simple_result}")
    print(f"   Smart agent (models other minds):   '{smart_answer}'   {smart_result}")
    print("\n  Reality says BOX. But Sally never saw it move, so she still believes BASKET.")
    print("  Tracking what other people believe is what makes an agent a good teammate.\n")


if __name__ == "__main__":
    main()
