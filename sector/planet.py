from util.dice import roll


class Planet(object):
    government_types = [
        "No Formal Government",
        "Corporate World",
        "Participating Democracy",
        "Self-Perpetuating Oligarchy",
        "Representative Democracy",
        "Feudal Technocracy",
        "Captive Government",
        "Balkanized",
        "Civil Service Bureaucracy",
        "Impersonal Bureaucracy",
        "Charismatic Dictator",
        "Non-Charismatic Leader",
        "Charismatic Oligarchy",
        "Religious Dictatorship"
    ]
    atmosphere_types = [
        "No Atmosphere",
        "Trace",
        "Very Thin, Tainted",
        "Very Thin",
        "Thin, Tainted",
        "Thin",
        "Standard",
        "Standard, Tainted",
        "Dense",
        "Dense, Tainted",
        "Exotic",
        "Corrosive",
        "Insidious"
    ]
    starport_types = {
        "A": "Excellent Facilities",
        "B": "Full Facilities",
        "C": "Basic Facilities",
        "D": "Poor Facilities",
        "E": "Frontier Base",
        "X": "No Spaceport"
    }

    def __init__(self, star):
        self.star = star
        self.number = len(star.inhabited_bodies) + 1
        self.name = "{}-{}".format(self.star.name, self.number)
        self.starport = self.star.rng.choice("AAABBCCDEEX")
        scout_chance = {
            "C": .2778,
            "B": .1667,
            "A": .0833
        }
        self.scout_base = self.star.rng.random() <= scout_chance.get(self.starport, .4167)
        self.naval_base = self.star.rng.random() <= .4167 and self.starport in "AB"
        self.radius = roll(2, -2, rng=self.star.rng)
        self.atmosphere = min(12, max(0, roll(2, -7, rng=self.star.rng) + self.radius if self.radius else 0))
        hydrographic_dm = -11 if self.atmosphere in (0, 1) or self.atmosphere > 9 else -7
        self.hydrographics = min(10, max(0, roll(2, hydrographic_dm, rng=self.star.rng) + self.atmosphere if self.radius else 0))
        pop = roll(2, -2, rng=self.star.rng)
        self.population = 10**pop
        government_type = min(0xD, max(0, roll(2, -7, rng=self.star.rng) + pop))
        self.government = self.government_types[government_type]
        self.law_level = min(10, max(0, roll(2, government_type-7, rng=self.star.rng)))
        tech_level_dm = 0
        starport_tech_level_dm = {
            "A": 6,
            "B": 4,
            "C": 2,
            "X": -4
        }
        tech_level_dm += starport_tech_level_dm.get(self.starport, 0)
        if self.radius in (0, 1):
            tech_level_dm += 2
        elif self.radius in (2, 3, 4):
            tech_level_dm += 1
        if self.atmosphere < 4 or self.atmosphere > 9:
            tech_level_dm += 1
        if self.hydrographics > 8:
            tech_level_dm += self.hydrographics - 8
        if 6 > pop > 0:
            tech_level_dm += 1
        elif pop > 8:
            tech_level_dm += 2 * (pop - 8)
        if government_type in (0, 5):
            tech_level_dm += 1
        elif government_type == 0xD:
            tech_level_dm -= 2
        self.tech_level = max(0, roll(1, tech_level_dm, rng=self.star.rng))

        self.classification = []

        if 9 >= self.atmosphere >= 4 and 8 >= self.hydrographics >= 4 and 7 >= pop >= 5:
            self.classification.append("Agricultural")
        elif self.atmosphere <= 3 and self.hydrographics <= 3 and self.population >= 6:
            self.classification.append("Non-Agricultural")
        if self.atmosphere in (0, 1, 2, 4, 7, 9) and self.population >= 9:
            self.classification.append("Industrial")
        elif self.population <= 6:
            self.classification.append("Non-Industrial")
        if self.atmosphere in (6, 8) and 8 >= self.population >= 6 and 9 >= government_type >= 4:
            self.classification.append("Rich")
        elif 5 >= self.atmosphere >= 2 and self.hydrographics <= 3:
            self.classification.append("Poor")
        if self.hydrographics == 10:
            self.classification.append("Water")
        elif not self.hydrographics and self.atmosphere >= 2:
            self.classification.append("Desert")
        if not self.radius:
            self.classification.append("Asteroid")
        elif not self.atmosphere:
            self.classification.append("Vacuum")
        if self.atmosphere in (0, 1) and self.hydrographics:
            self.classification.append("Ice-Capped")
        if not self.classification:
            self.classification.append("Standard")

    def __str__(self):
        bases = ""
        if self.scout_base or self.naval_base:
            bases += " with"
        if self.scout_base:
            bases += " Scout Base"
            if self.naval_base:
                bases += " and"
        if self.naval_base:
            bases += " Naval Base"
        return (
            "{}: {} World\n"
            "Population: ~{}\n"
            "Tech Level: {}\n"
            "Law Level: {}\n"
            "Size: {}\n"
            "Atmosphere: {}\n"
            "Hydrographics: {}% ocean\n"
            "Government: {}\n"
            "Starport: {} ({}){}"
        ).format(
            self.name(), " ".join(self.classification), self.population, hex(self.tech_level)[2:].upper(),
            hex(self.law_level)[2:].upper(), hex(self.radius)[2:].upper(), self.atmosphere_types[self.atmosphere],
            self.hydrographics * 10, self.government, self.starport, self.starport_types[self.starport], bases
        )

    def __json__(self):
        return {
            "name": self.name,
            "classification": self.classification,
            "population": self.population,
            "tech_level": self.tech_level,
            "law_level": self.law_level,
            "atmosphere": self.atmosphere,
            "hydrographics": self.hydrographics,
            "size": self.radius,
            "government": self.government,
            "starport": self.starport,
            "scout_base": self.scout_base,
            "naval_base": self.naval_base
        }

    def __repr__(self):
        return self.__str__()