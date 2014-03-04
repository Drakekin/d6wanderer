from math import sqrt


def route_length((x1, y1), (x2, y2)):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


class Empire(object):
    empire_names = [
        "{} Confederacy",
        "{} Union",
        "{} Empire",
        "Dominion of {}",
        "{} Federation",
        "{} Axis",
        "{} Aegis",
        "United Systems of {}",
        "Parliament of {}",
        "Kingdom of {}",
        "Duchy of {}",
        "County of {}",
        "Barony of {}",
    ]

    def __init__(self, rng, seat):
        self.rng = rng
        self.name = self.rng.choice(self.empire_names).format(seat.name)
        self.seat = seat
        self.seat.empire = self
        self.stars = {seat}

    def expand(self):
        expansion_options = set()
        for star in self.stars:
            expansion_options = expansion_options | star.routes
        expansion_options = expansion_options - self.stars
        options = []
        for option in expansion_options:
            if option.empire:
                continue
            options.append(option)
        if options:
            options = sorted(options, key=lambda s: route_length(s.location, self.seat.location), reverse=True)
            new_star = options.pop()
            new_star.empire = self
            self.stars.add(new_star)
            return True
        return False

    def __json__(self):
        return {
            "name": self.name,
            "seat": self.seat.name,
            "stars": [s.name for s in self.stars]
        }