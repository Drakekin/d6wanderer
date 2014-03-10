from util.dice import roll
import math


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
    apparent_magnitude_comparisons = [
        (-35, "a supergiant star"),
        (-30, "the sun from mercury"),
        (-26, "the sun"),
        (-25, "the sun from mars"),
        (-23, "the sun from jupiter"),
        (-20, "the sun from uranus"),
        (-18, "the sun from pluto"),
        (-13, "the full moon"),
        (-10, "an iridium flare"),
        (-6.5, "starlight"),
        (-6, "satellites"),
        (-2.5, "jupiter"),
        (-1, "a bright star"),
        (2, "mars"),
        (5, "a weak star"),
    ]
    scout_chance = {"C": .2778, "B": .1667, "A": .0833}

    @property
    def starport(self):
        if self._starport is None:
            self._starport = self.star.rng.choice("AAABBCCDEEX")
        return self._starport

    @property
    def scout_base(self):
        if self._scout_base is None:
            self._scout_base = self.star.rng.random() <= self.scout_chance.get(self.starport, .4167)
        return self._scout_base

    @property
    def naval_base(self):
        if self._naval_base is None:
            self._naval_base = self.star.rng.random() <= .4167 and self.starport in "AB"
        return self._naval_base

    @property
    def radius(self):
        if self._radius is None:
            self._radius = roll(2, -2, rng=self.star.rng)
        return self._radius

    @property
    def atmosphere(self):
        if self._atmosphere is None:
            self._atmosphere = min(12, max(0, roll(2, -7, rng=self.star.rng) + self.radius if self.radius else 0))
        return self._atmosphere

    @property
    def hydrographics(self):
        if self._hydrographics is None:
            hydrographic_dm = -11 if self.atmosphere in (0, 1) or self.atmosphere > 9 else -7
            self._hydrographics = min(10, max(0, roll(2, hydrographic_dm, rng=self.star.rng) + self.atmosphere if self.radius else 0))
        return self._hydrographics

    @property
    def government_type(self):
        if self._government is None:
            self._government = min(0xD, max(0, roll(2, -7, rng=self.star.rng) + self.population_level))
        return self._government

    @property
    def government(self):
        return self.government_types[self.government_type]

    @property
    def population_level(self):
        if self._population is None:
            self._population = roll(2, -2, rng=self.star.rng)
        return self._population

    @property
    def population(self):
        return 10**self.population_level if self.population_level else 0

    @property
    def tech_level(self):
        if self._tech_level is None:
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
            if 6 > self.population_level > 0:
                tech_level_dm += 1
            elif self.population_level > 8:
                tech_level_dm += 2 * (self.population_level - 8)
            if self.government_type in (0, 5):
                tech_level_dm += 1
            elif self.government_type == 0xD:
                tech_level_dm -= 2
            self._tech_level = max(1, roll(1, tech_level_dm, rng=self.star.rng))
        return self._tech_level

    @property
    def law_level(self):
        if self._law_level is None:
            self._law_level = min(10, max(0, roll(2, self.government_type-7, rng=self.star.rng)))
        return self._law_level

    @property
    def moons(self):
        if self._moons is None:
            max_moons = math.floor(self.radius/4)
            self._moons = self.star.rng.randint(0, max_moons)
        return self._moons

    @property
    def classification(self):
        if self._classification is None:
            self._classification = []
            if 9 >= self.atmosphere >= 4 and 8 >= self.hydrographics >= 4 and 7 >= self.population_level >= 5:
                self._classification.append("Agricultural")
            elif self.atmosphere <= 3 and self.hydrographics <= 3 and self.population_level >= 6:
                self._classification.append("Non-Agricultural")
            if self.atmosphere in (0, 1, 2, 4, 7, 9) and self.population_level >= 9:
                self._classification.append("Industrial")
            elif self.population <= 6 and self.population_level:
                self._classification.append("Non-Industrial")
            if self.atmosphere in (6, 8) and 8 >= self.population_level >= 6 and 9 >= self.government_type >= 4:
                self._classification.append("Rich")
            elif 5 >= self.atmosphere >= 2 and self.hydrographics <= 3 and self.population_level:
                self._classification.append("Poor")
            if self.hydrographics == 10:
                self._classification.append("Water")
            elif not self.hydrographics and self.atmosphere >= 2:
                self._classification.append("Desert")
            if not self.radius:
                self._classification.append("Asteroid")
            if self.radius >= 10:
                self._classification.append("Gas Giant")
            elif not self.atmosphere and self.radius:
                self._classification.append("Vacuum")
            if self.atmosphere in (0, 1) and self.hydrographics:
                self._classification.append("Ice-Capped")
            if not self._classification:
                self._classification.append("Standard")
        return self._classification

    def __init__(self, star, orbit):
        self.star = star
        self.number = len(star.satellites) + 1
        self.name = "{}-{}".format(self.star.name, self.number)

        self._starport = None
        self._scout_base = None
        self._naval_base = None
        self._radius = None
        self._atmosphere = None
        self._hydrographics = None
        self._population = None
        self._radius = None
        self._atmosphere = None
        self._classification = None
        self._tech_level = None
        self._law_level = None
        self._government = None
        self._moons = None

        self.orbit = orbit
        self.year = orbit**3/2*365
        # visible_luminosity = 10**(-star.luminosity/2.5)
        self.apparent_luminosity = -2.72 - 2.5 * math.log10(star.luminosity / ((orbit * 1.58e-5)**2))
        self.magnitude_comparison = "nothing, invisible to the naked eye"
        for mag, comparison in self.apparent_magnitude_comparisons:
            if self.apparent_luminosity < mag:
                self.magnitude_comparison = comparison
                break

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
            self.name, " ".join(self.classification), self.population, hex(self.tech_level)[2:].upper(),
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
            "moons": self.moons,
            "size": self.radius,
            "government": self.government,
            "starport": self.starport,
            "orbit": self.orbit,
            "year": self.year,
            "apparent_luminosity": self.apparent_luminosity,
            "magnitude": self.magnitude_comparison,
            "scout_base": self.scout_base,
            "naval_base": self.naval_base
        }

    def __repr__(self):
        return self.__str__()


class AsteroidField(Planet):
    @property
    def radius(self):
        return 0

    @property
    def population_level(self):
        return 0

    @property
    def tech_level(self):
        return 0


class GasGiant(Planet):
    @property
    def radius(self):
        if self._radius is None:
            self._radius = roll(15, rng=self.star.rng)
        return self._radius

    @property
    def atmosphere(self):
        return 10
