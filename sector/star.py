from sector.planet import Planet, AsteroidField, GasGiant
from math import sqrt


def bucket(l, v):
    for n, b in enumerate(l):
        if v > b:
            return n
    return n + 1


def halve(n, i=1.0):
    for _ in range(n):
        i /= 2
        yield i


def randfloat(rng, low, high):
    return low + rng.random() * (high - low)


def bound(bound, low, high):
    return low + bound * (high - low)


class Star(object):
    stellar_class_table = [
        ("A", .006),
        ("F", .03),
        ("G", .076),
    ]
    stellar_characteristic_table = {
        "O": ((16.0, 90.0), (6.60, 40.0), (30e3, 10e5)),
        "B": ((2.10, 16.0), (1.80, 6.60), (25.0, 30e3)),
        "A": ((1.40, 2.10), (1.40, 1.80), (5.00, 25.0)),
        "F": ((1.01, 1.40), (1.15, 1.40), (1.50, 5.00)),
        "G": ((0.80, 1.04), (0.96, 1.15), (0.60, 1.50)),
        "K": ((0.45, 0.80), (0.70, 0.96), (0.08, 0.60)),
        "M": ((0.08, 0.45), (0.15, 0.70), (0.01, 0.08)),
    }
    reference_habitable_zone = (0.5, 2.5)

    def __init__(self, rng, name, location):
        self.rng = rng
        self.name = name
        self.location = location
        stellar_class_value = self.rng.random()
        stellar_class = "K"
        for s_class, s_chance in self.stellar_class_table:
            if stellar_class_value <= s_chance:
                stellar_class = s_class
                break
        if stellar_class == "K":
            class_division = 0.75 + 0.25 * self.rng.random()
        else:
            class_division = self.rng.random()
        self.stellar_class = "{}{}".format(stellar_class, int(class_division * 10))
        mass_bound, radius_bound, luminosity_bound = self.stellar_characteristic_table[stellar_class]
        self.mass = bound(class_division, *mass_bound)
        self.radius = bound(class_division, *radius_bound)
        self.luminosity = bound(class_division, *luminosity_bound)
        hab_lower_bound, hab_upper_bound = self.reference_habitable_zone
        self.habitable_zone = hab_lower_bound * sqrt(self.luminosity), hab_upper_bound * sqrt(self.luminosity)
        hab_lower_bound, hab_upper_bound = self.habitable_zone

        self.satellites = []

        if rng.random() > .5:
            self.satellites.append(AsteroidField(self, hab_lower_bound / 5))

        current_radius = hab_lower_bound * 5 / 4
        current_step = (hab_upper_bound - hab_lower_bound) / 3

        for _ in range(rng.choice([0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3])):
            current_radius += current_step
            self.satellites.append(Planet(self, current_radius))

        current_step *= 4

        for _ in range(rng.choice([0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3])):
            current_radius += current_step
            self.satellites.append(GasGiant(self, current_radius))

        current_step *= 1.5

        for _ in range(rng.choice([0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2])):
            current_radius += current_step
            self.satellites.append(Planet(self, current_radius))

        self.routes = set()
        self.empire = None

    @property
    def borders(self):
        b = set()
        for route in self.routes:
            if route.empire != self.empire:
                b.add(route.empire.name if route.empire else "Independent")
        return list(b)

    @property
    def population(self):
        return sum(p.population for p in self.satellites)

    def __json__(self):
        return {
            "name": self.name,
            "location": self.location,
            "class": self.stellar_class,
            "mass": self.mass,
            "radius": self.radius,
            "luminosity": self.luminosity,
            "planets": self.satellites,
            "population": self.population,
            "empire": self.empire.name if self.empire else "Independent",
            "routes": [p.name for p in self.routes],
            "borders": self.borders
        }

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        planets = ""
        if len(self.satellites) != 1:
            planets += "s"
        if self.satellites:
            planets += " (" + ", ".join(" ".join(b.classification) for b in self.satellites) + ")"
        return (
            "{} (Class {}){}\n"
            "{} planet{}"
        ).format(
            self.name, self.stellar_class, " part of the {}".format(self.empire.name) if self.empire else "",
            len(self.satellites), planets
        )