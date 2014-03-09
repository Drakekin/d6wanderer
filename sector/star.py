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
        "O": (16.0, 6.6, 30000.0),
        "B": (9.0, 4.7, 15000.0),
        "A": (1.75, 1.6, 15),
        "F": (1.21, 1.275, 3.25),
        "G": (0.92, 1.05, 1.05),
        "K": (0.625, 0.83, 0.3),
        "M": (0.25, 0.7, 0.08),
    }

    def __init__(self, rng, name, location):
        self.rng = rng
        self.name = name
        self.location = location
        stellar_class_value = self.rng.random()
        stellar_class = "M"
        for s_class, s_chance in self.stellar_class_table:
            if stellar_class_value <= s_chance:
                stellar_class = s_class
                break
        self.stellar_class = "{}{}".format(stellar_class, self.rng.randint(0, 9))
        self.mass, self.radius, self.luminosity = self.stellar_characteristic_table[stellar_class]
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