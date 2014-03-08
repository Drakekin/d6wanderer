from random import choice
from util.dice import roll, test


class Profession(object):
    def __init__(self, name, ranks, enlistment, survival, commission,
                 promotion, reenlist, skills, autoskills, advancements):
        self.name = name
        self.ranks = ranks
        self.enlistment, self.enlistment_skill_one, self.enlistment_skill_two = enlistment
        self.survival, self.survival_skill = survival
        self.commission, self.commission_skill = commission
        self.promotion, self.promotion_skill = promotion
        self.reenlist = reenlist
        self.skills = skills
        self.autoskills = autoskills
        self.advancements = advancements

    def test_enlistment(self, character, rng):
        dm = 0
        if self.enlistment_skill_one is not None:
            skill, req = self.enlistment_skill_one
            if character.get_characteristic(skill) >= skill:
                dm += 1
            skill, req = self.enlistment_skill_two
            if character.get_characteristic(skill) >= skill:
                dm += 2
        return test(self.enlistment, roll(2, dm, rng=rng))

    def test_survival(self, character, rng):
        skill, req = self.survival_skill
        if character.get_characteristic(skill) >= skill:
            dm = 2
        else:
            dm = 0
        return test(self.survival, roll(2, dm, rng=rng))

    def test_commission(self, character, rng):
        if self.commission_skill is None:
            return False
        skill, req = self.commission_skill
        if character.get_characteristic(skill) >= skill:
            dm = 1
        else:
            dm = 0
        return test(self.commission, roll(2, dm, rng=rng))

    def test_promotion(self, character, rng):
        if self.promotion_skill is None:
            return False
        skill, req = self.commission_skill
        if character.get_characteristic(skill) >= skill:
            dm = 1
        else:
            dm = 0
        return test(self.promotion, roll(2, dm, rng=rng))

    def test_reenlist(self, character, rng, voluntary=True):
        result = roll(2, rng=rng)
        return (test(self.reenlist, result) and voluntary) or result == 12

    def pick_skill(self, character, rng):
        return rng.choice(choice(self.skills[:3 if character.education >= 8 else 4]))

    def __str__(self):
        return self.name

    def __json__(self):
        return str(self)
