import random


def roll(num, modifier=0, rng=random):
    return sum(rng.randint(1, 6) for _ in xrange(num)) + modifier


def test(difficulty, roll):
    if difficulty < 0:
        return roll <= abs(difficulty)
    else:
        return roll >= difficulty
