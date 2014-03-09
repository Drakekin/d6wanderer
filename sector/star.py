from sector.planet import Planet


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
        ("O", .0000003),
        ("B", .0013),
        ("A", .006),
        ("F", .03),
        ("G", .076),
        ("K", .121),
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
        class_division = self.rng.random()
        self.stellar_class = "{}{}".format(stellar_class, int(class_division * 10))
        mass_bound, radius_bound, luminosity_bound = self.stellar_characteristic_table[stellar_class]
        self.mass = bound(class_division, *mass_bound)
        self.radius = bound(class_division, *radius_bound)
        self.luminosity = bound(class_division, *luminosity_bound)
        self.gas_giants = self.rng.randint(0, 5)

        self.inhabited_bodies = []

        chance = list(halve(10))
        planets = bucket(chance, rng.random()) + 1

        for _ in range(planets):
            self.inhabited_bodies.append(Planet(self))
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
        return sum(p.population for p in self.inhabited_bodies)

    def __json__(self):
        return {
            "name": self.name,
            "location": self.location,
            "class": self.stellar_class,
            "mass": self.mass,
            "radius": self.radius,
            "luminosity": self.luminosity,
            "gas_giants": self.gas_giants,
            "planets": self.inhabited_bodies,
            "population": self.population,
            "empire": self.empire.name if self.empire else "Independent",
            "routes": [p.name for p in self.routes],
            "borders": self.borders
        }

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        planets = ""
        if len(self.inhabited_bodies) != 1:
            planets += "s"
        if self.inhabited_bodies:
            planets += " (" + ", ".join(" ".join(b.classification) for b in self.inhabited_bodies) + ")"
        return (
            "{} (Class {}){}\n"
            "{} planet{} plus {} gas giant{}"
        ).format(
            self.name, self.stellar_class, " part of the {}".format(self.empire.name) if self.empire else "",
            len(self.inhabited_bodies), planets, self.gas_giants, "" if self.gas_giants == 1 else "s"
        )