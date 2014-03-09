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


def range2d(start, end):
    sx, sy = start
    ex, ey = end
    dx = ex - sx + 1
    dy = ey - sy + 1

    for y in range(dy):
        for x in range(dx):
            yield (sx + x, sy + y)


def generate_systems(rng):
    stars = {}
    with open("starnames.csv") as star_name_file:
        star_names = list(set([l.strip() for l in star_name_file]))
        rng.shuffle(star_names)
    # for _ in range(rng.randint(100, 150)):
    #     location = None
    #     while location is None or location in stars:
    #         location = (rng.randint(-10, 10), rng.randint(-10, 10))
    for location in range2d((-10, -10), (10, 10)):
        if rng.random() > (1.0/3.0):
            continue  # One third chance of a notable star
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

        sorted_routes = sorted(list(plausible_routes), key=lambda (s, e): route_length(s, e), reverse=True)

        routes.add(sorted_routes.pop())

        for _ in range(rng.randint(min(1, len(sorted_routes)), max(min(1, len(sorted_routes)), len(sorted_routes) / 3))):
            routes.add(sorted_routes.pop())
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


def analyse(stars, empires):
    independent_stars = [s for s in stars if s.empire is None]
    stats = {"population": sum(sum(p.population for p in s.inhabited_bodies) for s in stars), "systems": len(stars),
             "planets": sum(len(s.inhabited_bodies) for s in stars), "independent_systems": len(independent_stars),
             "independent_planets": sum(len(s.inhabited_bodies) for s in independent_stars)}

    tech_levels = []
    for star in stars:
        tech_levels += [p.tech_level for p in star.inhabited_bodies]
    tech_levels = sorted(tech_levels)
    if len(tech_levels) % 2:
        stats["avg_tech_level"] = (tech_levels[len(tech_levels)/2] + tech_levels[len(tech_levels)/2 - 1])/2
    else:
        stats["avg_tech_level"] = tech_levels[len(tech_levels)/2]

    empire_stats = {}
    for empire in empires:
        e_stats = {"population": sum(sum(p.population for p in s.inhabited_bodies) for s in empire.stars),
                   "systems": len(empire.stars), "planets": sum(len(s.inhabited_bodies) for s in empire.stars)}

        tech_levels = []
        for star in empire.stars:
            tech_levels += [p.tech_level for p in star.inhabited_bodies]
        tech_levels = sorted(tech_levels)
        if len(tech_levels) % 2:
            e_stats["avg_tech_level"] = (tech_levels[len(tech_levels)/2] + tech_levels[len(tech_levels)/2 - 1])/2
        else:
            e_stats["avg_tech_level"] = tech_levels[len(tech_levels)/2]

        empire_stats[empire.name] = e_stats

    stats["empires"] = empire_stats

    return stats


def generate_sector(gen_seed):
    rng = Random(gen_seed.lower())
    stars = generate_systems(rng)
    connect_systems(rng, stars)
    empires = generate_empires(rng, stars)
    analysis = analyse(stars.values(), empires)

    return stars.values(), empires, analysis


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



