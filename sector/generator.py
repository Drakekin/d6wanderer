from collections import defaultdict
from math import sqrt
from random import Random
from json import dump
from sector.empire import Empire
from sector.star import Star
from util.custom_json_encoder import ObjectJSONEncoder
from util.point import Point
from util.voronoi import computeDelaunayTriangulation


def systems_visited(routes):
    visited = set()
    for start, end in routes:
        visited.add(start)
        visited.add(end)
    return visited


def is_important_planet(planet):
    return planet.population >= 1e6 and planet.tech_level >= 11 and planet.starport == "A"


def count_affiliated(stars):
    return len([s for s in stars if s.empire is None])


def generate_systems(rng):
    stars = {}
    with open("starnames.csv") as star_name_file:
        star_names = list(set([l.strip() for l in star_name_file]))
        rng.shuffle(star_names)
    for _ in range(rng.randint(100, 150)):
        location = None
        while location is None or location in stars:
            location = (rng.randint(-10, 10), rng.randint(-10, 10))
        name = star_names.pop()
        stars[location] = Star(rng, name, location)
    return stars


def route_length((x1, y1), (x2, y2)):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def connect_systems(rng, stars):
    routes = set()
    destinations = stars.keys()
    possible_routes = defaultdict(set)

    for _a, _b, _c in computeDelaunayTriangulation([Point(*point) for point in destinations]):
        a = destinations[_a]
        b = destinations[_b]
        c = destinations[_c]

        possible_routes[a].add(b)
        possible_routes[a].add(c)
        possible_routes[b].add(c)
        possible_routes[b].add(a)
        possible_routes[c].add(a)
        possible_routes[c].add(b)

    visited_systems = {rng.choice(destinations)}
    destinations = set(destinations)

    while visited_systems != destinations:
        plausible_routes = set()

        for system in visited_systems:
            for destination in possible_routes[system]:
                if destination not in visited_systems:
                    plausible_routes.add((system, destination))

        routes.add(sorted(list(plausible_routes), key=lambda (s, e): route_length(s, e), reverse=True).pop())
        visited_systems = systems_visited(routes)

    for start, end in routes:
        stars[start].routes.add(stars[end])
        stars[end].routes.add(stars[start])


def generate_empires(rng, stars):
    planets = []

    for system in stars.itervalues():
        planets += system.inhabited_bodies

    important_planets = sorted((p for p in planets if is_important_planet(p)),
                               key=lambda p: (p.tech_level, p.population))
    seed_systems = set()
    seed_planets = []

    for planet in important_planets:
        if planet.star in seed_systems:
            continue

        seed_systems.add(planet.star)
        seed_planets.append(planet)

    empires = []
    rng.shuffle(seed_planets)

    for _ in range(rng.randint(3 if len(seed_planets) > 3 else len(seed_planets), len(seed_planets))):
        seat = seed_planets.pop()
        empire = Empire(rng, seat.star)
        seat.name = "{}, Capital of the {}".format(seat.name, empire.name)
        empires.append(empire)

    expanding_empires = empires

    while float(count_affiliated(stars.values())) / len(stars.values()) > .3:
        to_expand = expanding_empires
        expanding_empires = []

        for empire in to_expand:
            expanded = empire.expand()
            if expanded:
                expanding_empires.append(empire)

        if not expanding_empires:
            break

    return empires


def generate_sector(gen_seed):
    rng = Random(gen_seed.lower())
    stars = generate_systems(rng)
    connect_systems(rng, stars)
    empires = generate_empires(rng, stars)

    return stars.values(), empires


if __name__ == "__main__":
    stars, empires = generate_sector("Atik Navy Cruiser Gorobchev")

    with open("../sector.json", "w") as sector:
        dump(
            {"stars": stars, "empires": empires}, sector, sort_keys=True,
            indent=4, separators=(',', ': '), cls=ObjectJSONEncoder
        )

    print len(stars), "Stars"
    print sum(1 for s in stars if not s.inhabited_bodies or not s.gas_giants), "Stars With Planets"
    print sum(1 for s in stars if not s.inhabited_bodies), "Stars With Inhabited Planets"
    print sum(len(s.inhabited_bodies) + s.gas_giants for s in stars), "Planets"
    print sum(len(s.inhabited_bodies) for s in stars), "Inhabited Planets"
    print len(empires), "Empires"
    for empire in empires:
        print "\t{} ({} stars, {} planets, {} inhabited)".format(
            empire.name,
            len(empire.stars),
            sum(len(s.inhabited_bodies) + s.gas_giants for s in empire.stars),
            sum(len(s.inhabited_bodies) for s in empire.stars),
        )
    print count_affiliated(stars), "independent systems"



