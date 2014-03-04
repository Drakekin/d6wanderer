# coding=utf-8
from collections import defaultdict, Counter
from random import choice
from util.dice import roll, test
from character.professions import Profession

TITLES = {
    11: "Knight",
    12: "Baron",
}
STRENGTH, DEXTERITY, ENDURANCE, INTELLIGENCE, EDUCATION, SOCIAL = range(6)
CHARACTERISTIC, SKILL, BENEFIT = range(3)
NAVY = Profession(
    "Navy",
    ["Ensign", "Lieutenant", "Lieutenant Commander", "Captain", "Admiral"],
    (+8, (INTELLIGENCE, +8), (EDUCATION, +9)),
    (+5, (INTELLIGENCE, +7)),
    (+10, (SOCIAL, +9)),
    (+8, (EDUCATION, +8)),
    +6,
    (
        [
            (CHARACTERISTIC, STRENGTH), (CHARACTERISTIC, DEXTERITY), (CHARACTERISTIC, ENDURANCE),
            (CHARACTERISTIC, INTELLIGENCE), (CHARACTERISTIC, EDUCATION), (CHARACTERISTIC, SOCIAL)
        ],
        [
            (SKILL, "Ships Boat"), (SKILL, "Vacc Suit"), (SKILL, "Forward Observer"),
            (SKILL, "Gunnery"), (SKILL, "Blade Combat"), (SKILL, "Gun Combat")
        ],
        [
            (SKILL, "Vacc Suit"), (SKILL, "Mechanical"), (SKILL, "Electronic"),
            (SKILL, "Engineering"), (SKILL, "Gunnery"), (SKILL, "Jack-of-all-Trades")
        ],
        [
            (SKILL, "Medical"), (SKILL, "Navigation"), (SKILL, "Engineering"),
            (SKILL, "Computer"), (SKILL, "Pilot"), (SKILL, "Admin")
        ]
    ),
    [
        (3, CHARACTERISTIC, SOCIAL),
        (4, CHARACTERISTIC, SOCIAL),
    ],
    1
)
MARINES = Profession(
    "Marines",
    ["Lieutenant", "Captain", "Force Commander", "Lieutenant Colonel", "Colonel", "Brigadier"],
    (+9, (INTELLIGENCE, +9), (STRENGTH, +9)),
    (+6, (ENDURANCE, +8)),
    (+9, (EDUCATION, +7)),
    (+9, (SOCIAL, +8)),
    +6,
    (
        [
            (CHARACTERISTIC, STRENGTH), (CHARACTERISTIC, DEXTERITY), (CHARACTERISTIC, ENDURANCE),
            (SKILL, "Gambling"), (SKILL, "Brawling"), (SKILL, "Blade Combat"),
        ],
        [
            (SKILL, "ATV"), (SKILL, "Vacc Suit"), (SKILL, "Blade Combat"),
            (SKILL, "Blade Combat"), (SKILL, "Blade Combat"), (SKILL, "Gun Combat"),
        ],
        [
            (SKILL, "Vehicle"), (SKILL, "Mechanical"), (SKILL, "Electronic"),
            (SKILL, "Tactics"), (SKILL, "Blade Combat"), (SKILL, "Gun Combat"),
        ],
        [
            (SKILL, "Medical"), (SKILL, "Tactics"), (SKILL, "Tactics"),
            (SKILL, "Computer"), (SKILL, "Leader"), (SKILL, "Admin"),
        ]
    ),
    [
        (0, SKILL, "Cutlass"),
        (0, SKILL, "Revolver"),
    ],
    1
)
ARMY = Profession(
    "Army",
    ["Lieutenant", "Captain", "Major", "Lieutenant Colonel", "Colonel", "General"],
    (+5, (DEXTERITY, +6), (ENDURANCE, +5)),
    (+5, (ENDURANCE, +6)),
    (+5, (ENDURANCE, +7)),
    (+6, (ENDURANCE, +7)),
    +7,
    (
        [
            (CHARACTERISTIC, STRENGTH), (CHARACTERISTIC, DEXTERITY), (CHARACTERISTIC, ENDURANCE),
            (SKILL, "Gambling"), (CHARACTERISTIC, EDUCATION), (SKILL, "Brawling"),
        ],
        [
            (SKILL, "ATV"), (SKILL, "Air/Raft"), (SKILL, "Gun Combat"),
            (SKILL, "Forward Observer"), (SKILL, "Gun Combat"), (SKILL, "Blade Combat"),
        ],
        [
            (SKILL, "Vehicle"), (SKILL, "Mechanical"), (SKILL, "Electronic"),
            (SKILL, "Tactics"), (SKILL, "Blade Combat"), (SKILL, "Gun Combat"),
        ],
        [
            (SKILL, "Medical"), (SKILL, "Tactics"), (SKILL, "Tactics"),
            (SKILL, "Computer"), (SKILL, "Leader"), (SKILL, "Admin"),
        ]
    ),
    [
        (0, SKILL, "Rifle"),
        (0, SKILL, "SMG"),
    ],
    1
)
SCOUTS = Profession(
    "Scouts",
    ["Scout"],
    (+7, (INTELLIGENCE, +6), (STRENGTH, +8)),
    (+7, (ENDURANCE, +9)),
    (None, None),
    (None, None),
    +3,
    (
        [
            (CHARACTERISTIC, STRENGTH), (CHARACTERISTIC, DEXTERITY), (CHARACTERISTIC, ENDURANCE),
            (CHARACTERISTIC, INTELLIGENCE), (CHARACTERISTIC, EDUCATION), (SKILL, "Gun Combat")
        ],
        [
            (SKILL, "Air/Raft"), (SKILL, "Vacc Suit"), (SKILL, "Mechanical"),
            (SKILL, "Navigation"), (SKILL, "Electronic"), (SKILL, "Jack-of-all-Trades"),
        ],
        [
            (SKILL, "Vehicle"), (SKILL, "Mechanical"), (SKILL, "Electronic"),
            (SKILL, "Jack-of-all-Trades"), (SKILL, "Gunnery"), (SKILL, "Medical"),
        ],
        [
            (SKILL, "Medical"), (SKILL, "Navigation"), (SKILL, "Engineering"),
            (SKILL, "Computer"), (SKILL, "Pilot"), (SKILL, "Jack-of-all-Trades"),
        ]
    ),
    [
        (0, SKILL, "Pilot"),
    ],
    2
)
MERCHANTS = Profession(
    "Merchants",
    ["4th Officer", "3rd Officer", "2nd Officer", "1st Officer", "Captain"],
    (+7, (STRENGTH, +7), (INTELLIGENCE, +6)),
    (+5, (INTELLIGENCE, +7)),
    (+4, (INTELLIGENCE, +6)),
    (+10, (INTELLIGENCE, +9)),
    +4,
    (
        [
            (CHARACTERISTIC, STRENGTH), (CHARACTERISTIC, DEXTERITY), (CHARACTERISTIC, ENDURANCE),
            (CHARACTERISTIC, STRENGTH), (SKILL, "Blade Combat"), (SKILL, "Bribery")
        ],
        [
            (SKILL, "Vehicle"), (SKILL, "Vacc Suit"), (SKILL, "Jack-of-all-Trades"),
            (SKILL, "Steward"), (SKILL, "Electronics"), (SKILL, "Gun Combat"),
        ],
        [
            (SKILL, "Streetwise"), (SKILL, "Mechanical"), (SKILL, "Electronic"),
            (SKILL, "Navigation"), (SKILL, "Gunnery"), (SKILL, "Medical"),
        ],
        [
            (SKILL, "Medical"), (SKILL, "Navigation"), (SKILL, "Engineering"),
            (SKILL, "Computer"), (SKILL, "Pilot"), (SKILL, "Admin"),
        ]
    ),
    [
        (3, SKILL, "Pilot")
    ],
    1
)
OTHER = Profession(
    "Other",
    ["Professional"],
    (+3, None, None),
    (+5, (INTELLIGENCE, +9)),
    (None, None),
    (None, None),
    +5,
    (
        [
            (CHARACTERISTIC, STRENGTH), (CHARACTERISTIC, DEXTERITY), (CHARACTERISTIC, ENDURANCE),
            (SKILL, "Blade Combat"), (SKILL, "Brawling"), (CHARACTERISTIC, SOCIAL),
        ],
        [
            (SKILL, "Vehicle"), (SKILL, "Gambling"), (SKILL, "Brawling"),
            (SKILL, "Bribery"), (SKILL, "Blade Combat"), (SKILL, "Gun Combat"),
        ],
        [
            (SKILL, "Streetwise"), (SKILL, "Mechanical"), (SKILL, "Electronic"),
            (SKILL, "Navigation"), (SKILL, "Gunnery"), (SKILL, "Medical"),
        ],
        [
            (SKILL, "Medical"), (SKILL, "Forgery"), (SKILL, "Electronics"),
            (SKILL, "Computer"), (SKILL, "Streetwise"), (SKILL, "Jack-of-all-Trades"),
        ]
    ),
    [],
    1
)
DRAFT = [
    NAVY,
    MARINES,
    ARMY,
    SCOUTS,
    MERCHANTS,
    OTHER
]


class Character(object):
    def __init__(self, name, profession, death=False):
        self._name = name
        self.age = 18
        self.terms = 0
        self.half_terms = 0
        self.balance = 0
        self.equipment = []
        self.alive = True
        self.commissioned = False
        self.claimed_autoskills = []

        self.strength = roll(2)
        self.dexterity = roll(2)
        self.endurance = roll(2)
        self.intelligence = roll(2)
        self.education = roll(2)
        self.social = roll(2)

        self.skills = defaultdict(int)
        self._rank = 0

        if profession.test_enlistment(self):
            self.profession = profession
            self.drafted = False
        else:
            self.profession = choice(DRAFT)
            self.drafted = True

        terms = 7

        while True:
            survival = self.profession.test_survival(self)

            if not survival:
                if death:
                    self.alive = False
                    return
                else:
                    self.become_older(2)
                    self.half_terms += 1
                    terms -= 1
                    continue

            self.become_older(4)

            for rank, kind, skill in (skill for skill in self.profession.autoskills if not skill in self.claimed_autoskills):
                if self._rank >= rank:
                    if kind == CHARACTERISTIC:
                        self.set_characteristic(skill, 1)
                    elif kind == SKILL:
                        self.skills[skill] += 1
                    self.claimed_autoskills.append((rank, kind, skill))

            if self.terms == 0:
                skills = 2
            else:
                skills = self.profession.advancements

            if not self.drafted:
                if not self.commissioned:
                    if self.profession.test_commission(self):
                        self.commissioned = True
                        skills += 1
                else:
                    if self.profession.test_promotion(self) and self._rank + 2 < len(self.profession.ranks):
                        self._rank += 1
                        skills += 1

            self.drafted = False
            for _ in range(skills*2):
                kind, skill = choice(choice(self.profession.skills))
                if kind == CHARACTERISTIC:
                    self.set_characteristic(skill, 1)
                elif kind == SKILL:
                    self.skills[skill] += 1

            self.terms += 1
            terms -= 1

            if not self.profession.test_reenlist(self, terms > 0):
                break

        mustering_benefits = self.terms
        if self._rank in (0, 1):
            mustering_benefits += 1
        elif self._rank in (2, 3):
            mustering_benefits += 2
        elif self._rank in (4, 5):
            mustering_benefits += 3

        benfits_table = [
            [
                (BENEFIT, "Low Passage"), (BENEFIT, "Low Passage"), (BENEFIT, "Low Passage"),
                (BENEFIT, "Low Passage"), (BENEFIT, "Low Passage"), (BENEFIT, "Low Passage"),
            ],
            [
                (CHARACTERISTIC, (INTELLIGENCE, 1)), (CHARACTERISTIC, (INTELLIGENCE, 2)),
                (CHARACTERISTIC, (INTELLIGENCE, 1)), (CHARACTERISTIC, (INTELLIGENCE, 2)),
                (CHARACTERISTIC, (INTELLIGENCE, 1)), (CHARACTERISTIC, (INTELLIGENCE, 1)),
            ],
            [
                (CHARACTERISTIC, (EDUCATION, 1)), (CHARACTERISTIC, (EDUCATION, 2)),
                (CHARACTERISTIC, (EDUCATION, 2)), (CHARACTERISTIC, (EDUCATION, 2)),
                (CHARACTERISTIC, (EDUCATION, 1)), (CHARACTERISTIC, (EDUCATION, 1)),
            ],
            [
                (BENEFIT, "Gun"), (BENEFIT, "Gun"), (BENEFIT, "Gun"),
                (BENEFIT, "Blade"), (BENEFIT, "Blade"), (BENEFIT, "Blade"),
            ],
            [
                (BENEFIT, "Traveller's Aid Society Membership"), (BENEFIT, "Traveller's Aid Society Membership"),
                (BENEFIT, "High Passage"), (BENEFIT, "High Passage"), (BENEFIT, "Gun"), (BENEFIT, "Blade"),
            ],
            [
                (BENEFIT, "High Passage"), (BENEFIT, "High Passage"), (BENEFIT, "Mid Passage"),
                (BENEFIT, "Scout Ship"), (BENEFIT, "Low Passage")
            ],
            [
                (CHARACTERISTIC, (SOCIAL, 2)), (CHARACTERISTIC, (SOCIAL, 2)), (CHARACTERISTIC, (SOCIAL, 1)),
                (BENEFIT, "Free Trader")
            ],
        ]

        cash_table = [
            [1000, 2000, 2000, 20000, 1000, 1000],
            [5000, 5000, 5000, 5000, 5000, 20000],
            [5000, 5000, 10000, 20000, 5000, 5000],
            [10000, 10000, 10000, 30000, 20000, 10000],
            [20000, 20000, 10000, 50000, 20000, 10000],
            [50000, 30000, 20000, 50000, 40000, 50000],
            [50000, 40000, 30000, 50000, 40000, 100000],
        ]

        money_rolls = 3

        for _ in range(mustering_benefits):
            if money_rolls and choice((True, False)):
                money_rolls -= 1
                self.balance += choice(cash_table[roll(1, 0 if self.skills["Gambling"] else -1)])
            benefit_row_options = range(6) + ([n+1 for n in range(6)] if self._rank in (4, 5) else [])
            kind, benefit = choice(benfits_table[choice(benefit_row_options)])
            if kind == CHARACTERISTIC:
                characteristic, value = benefit
                self.set_characteristic(characteristic, value)
            elif kind == BENEFIT:
                thing = benefit
                while thing == "Traveller's Aid Society Membership" and thing in self.equipment:
                    kind, thing = choice(benfits_table[4])
                if thing == "Blade" and thing in self.equipment:
                    self.skills["Blade Combat"] += 1
                    continue
                elif thing == "Gun" and thing in self.equipment:
                    self.skills["Gun Combat"] += 1
                    continue
                self.equipment.append(benefit)
            elif kind == SKILL:
                skill, value = benefit
                self.skills[skill] += value

        self.equipment = ["{} {}s".format(v, k) if v - 1 else k for k, v in Counter(self.equipment).items()]
        if not self.skills["Gambling"]:
            del self.skills["Gambling"]

    def set_characteristic(self, characteristic, value):
        if characteristic == STRENGTH:
            self.strength += value
        if characteristic == DEXTERITY:
            self.dexterity += value
        if characteristic == ENDURANCE:
            self.endurance += value
        if characteristic == INTELLIGENCE:
            self.intelligence += value
        if characteristic == EDUCATION:
            self.education += value
        if characteristic == SOCIAL:
            self.social += value

    def get_characteristic(self, characteristic):
        if characteristic == STRENGTH:
            return self.strength
        if characteristic == DEXTERITY:
            return self.dexterity
        if characteristic == ENDURANCE:
            return self.endurance
        if characteristic == INTELLIGENCE:
            return self.intelligence
        if characteristic == EDUCATION:
            return self.education
        if characteristic == SOCIAL:
            return self.social
        return 0

    def become_older(self, years):
        if self.age + years >= 74 or self.age >= 34 and (self.age + years % 4 == 0 or self.age % 4 >= self.age + years % 4):
            if self.age < 50:
                if test(roll(2), +8):
                    self.strength -= 1
                if test(roll(2), +7):
                    self.dexterity -= 1
                if test(roll(2), +8):
                    self.endurance -= 1
            elif self.age < 66:
                if test(roll(2), +9):
                    self.strength -= 1
                if test(roll(2), +8):
                    self.dexterity -= 1
                if test(roll(2), +9):
                    self.endurance -= 1
            else:
                if test(roll(2), +9):
                    self.strength -= 2
                if test(roll(2), +9):
                    self.dexterity -= 2
                if test(roll(2), +9):
                    self.endurance -= 2
                if test(roll(2), +9):
                    self.intelligence -= 1
        self.age += years

    @property
    def title(self):
        return TITLES.get(self.social, "Citizen")

    @property
    def rank(self):
        return self.profession.ranks[self._rank]

    @property
    def pension(self):
        return min(self.terms - 4, 0) * 2000 + 2000 if self.terms > 4 else 0

    @property
    def actual_terms(self):
        return "{}{}".format(self.terms, "½"if self.half_terms else "")

    @property
    def name(self):
        if self.social == 11:
            return "Sir {}".format(self._name)
        elif self.social == 12:
            return "{} von {}".format(*self._name.split(" "))
        return self._name

    def __str__(self):
        if not self.alive:
            return "{profession} {rank} {name} DEAD after {terms} Terms".format(
                profession=self.profession, rank=self.rank, name=self.name, terms=self.terms
            )
        template = ("{profession} {rank} {name}, U{str}{dex}{end}{int}{edu}{soc}, Age {age}\n"
                    "{terms} Terms, {balance} Cr (+{pension} Cr/month)\n"
                    "{skills}\n"
                    "{equipment}")

        skills = ", ".join("{}-{}".format(skill, value) for skill, value in self.skills.items())
        equipment = ", ".join(self.equipment)
        return template.format(
            profession=self.profession, rank=self.rank, name=self.name, str=hex(self.strength)[2:],
            dex=hex(self.dexterity)[2:], end=hex(self.endurance)[2:], int=hex(self.intelligence)[2:],
            edu=hex(self.education)[2:], soc=hex(self.social)[2:], age=self.age, terms=self.actual_terms,
            balance=self.balance, pension=self.pension, skills=skills, equipment=equipment,
        )