(function() {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame']
                                   || window[vendors[x]+'CancelRequestAnimationFrame'];
    }

    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); },
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };

    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());

function randint(min, max) {
    return Math.floor(Math.random()*(max-min)+min);
}

var star_colours = {
    "M": "#ffbd6f",
    "K": "#ffddb4",
    "G": "#fff4e8",
    "F": "#fbf8ff",
    "A": "#cad8ff",
    "B": "#aabfff",
    "O": "#9db4ff"
}, star_sizes = {
    "M": 3,
    "K": 4,
    "G": 4,
    "F": 5,
    "A": 8,
    "B": 12,
    "O": 20
}, atmosphere_types = [
    "No",
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
], tech_levels = [
    "Frontier",
    "Basic Infrastructure",
    "Basic Industry",
    "Basic Electronics",
    "Basic Precision Engineering",
    "Solid State Electronics",
    "Nuclear Power",
    "Orbital Capability",
    "Artificial Gravity",
    "FTL Capability",
    "Holographics",
    "Handheld Quantum Computing",
    "Miniaturised Artificial Gravity",
    "Human Cloning",
    "Short-Range FTL Communication",
    "Miniaturised Forcefields",
    "Matter Transporter",
    "Self-Aware Machines",
    "Singularity"
], law_levels = [
    "No prohibitions",
    "Explosives, chemical weapons etc. prohibited",
    "Portable energy weapons prohibited",
    "Military weapons prohibited",
    "Automatic weapons prohibited",
    "Concealable firearms prohibited",
    "Small arms prohibited, open carry discouraged",
    "All longarms prohibited except for sport",
    "Long blades controlled, other weapons prohibited",
    "Weapons prohibited except on private property",
    "All weapons prohibited"
];

function fmod (a,b) {
    return Number((a - (Math.floor(a / b) * b)).toPrecision(8));
}

function buildTreemap(diagram) {
    var treemap = new QuadTree({
            x: 0,
            y: 0,
            width: sector.width,
            height: sector.height
        }),
        cells = diagram.cells,
        iCell = cells.length;
    while (iCell--) {
        var bbox = cells[iCell].getBbox();
        bbox.cellid = iCell;
        treemap.insert(bbox);
    }
    return treemap;
}

function cell_under(x, y, treemap) {
    // Get the Voronoi cells from the tree map given x,y
    var items = treemap.retrieve({x:x,y:y}),
        iItem = items.length,
        cells = diagram.cells,
        cell, cellid;
    while (iItem--) {
        cellid = items[iItem].cellid;
        cell = cells[cellid];
        if (cell.pointIntersection(x,y) > 0) {
            return cell.site;
        }
    }
    return undefined;
}

function distance(start, end) {
    return Math.sqrt(Math.pow(start[0]-end[0], 2)+Math.pow(start[1]-end[1], 2));
}

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function unselect() {
    $("#planetname").text("No System Selected");
    $('#planetname').css("color", "inherit");
    var sector_info = "Click a star to select that system.<br><br>";
    sector_info += "This sector contains " + stats.systems + " systems and " + stats.planets + " planets. ";
    sector_info += "The average tech level in this sector is " + stats.avg_tech_level + " (" + tech_levels[stats.avg_tech_level] + "). ";
    sector_info += "There are " + Object.size(stats.empires) + " empires in this sector. ";
    sector_info += "There are also " + stats.independent_systems + " independent systems with " + stats.independent_planets + " planets.<br><br>";
    for (var empire in stats.empires) {
        sector_info += "<strong style='color: " + empires[empire].colour + ";'>" + empire + "</strong><br>";
        empire = stats.empires[empire];
        sector_info += empire.systems + " systems, " + empire.planets + " planets.<br>";
        sector_info += "Average tech level: " + empire.avg_tech_level + " (" + tech_levels[empire.avg_tech_level] + ").<br><br>";
    }
    $('#planetinfo').html(sector_info);
    selected = undefined;
}

function click_handler(event) {
    var ratio = canvas_size / 600;
    var x = event.offsetX / ratio,
        y = event.offsetY / ratio,
        system = cell_under(x, y, treemap);
    if (system) {
        selected = system;
        var first;
        $("#planetname").text(system.name + " (" + system.empire + ")");
        $('#planetname').css("color", empires[system.empire].colour);
        var description = "<a href='javascript:unselect()'>Back to sector view</a><br><br>";
        if (system.name == empires[system.empire].seat)
            description += "<strong>Seat of the " + system.empire + "</strong><br>";
        description += "Class " + system.class + "<br>";
        description += "Coordinates (" + system.location[0] + ", " + system.location[1] + ")<br>";
        if (system.routes) {
            description += "Subsidised routes to";
            first = true;
            for (var r in system.routes) {
                r = system.routes[r];
                description += first ? " " : ", ";
                description += r;
                description += " (" + Math.ceil(distance(system.location, stars[r].location)) + " parsec)";
                first = false;
            }
            description += "<br>";
        }
        if (system.gas_giants)
            description += system.gas_giants + " gas giant" + (system.gas_giants == 1 ? "" : "s") + "<br>";
        if (system.planets) {
            description += system.planets.length + " inhabited planet" + (system.planets.length == 1 ? "" : "s") + "<br>";
            for (var p in system.planets) {
                var planet = system.planets[p];
                description += "<br>" + planet.name + " (";
                if (planet.classification) {
                    first = true;
                    for (var c in planet.classification) {
                        c = planet.classification[c];
                        description += first ? "" : " ";
                        description += c;
                        first = false;
                    }
                } else {
                    description += "Standard";
                }
                description += " World)<br><em>Size " + planet.size;
                description += ", Population ~" + planet.population + "<br>";
                description += (planet.hydrographics * 10) + "% ocean coverage, ";
                description += atmosphere_types[planet.atmosphere] + " atmosphere<br>";
                description += planet.government + ", Law Level: " + planet.law_level;
                description += " (" + law_levels[planet.law_level] + ")<br>";
                description += "Tech Level:" + planet.tech_level + " (" + tech_levels[planet.tech_level] + "), ";
                description += "Starport: " + planet.starport;
                if (planet.scout_base) description += ", Scout base";
                if (planet.naval_base) description += ", Naval base";
                description += "<br>";

                description += "</em>";
            }
        }
        $("#planetinfo").html(description);
    } else {
        unselect();
    }
}

function draw_map() {
    var seedinfo = $("#seedinfo");
    var top_missing = seedinfo.height();
    top_missing += parseInt(seedinfo.css("padding-top"), 10) + parseInt(seedinfo.css("padding-bottom"), 10); //Total Padding Width
    top_missing += parseInt(seedinfo.css("margin-top"), 10) + parseInt(seedinfo.css("margin-bottom"), 10); //Total Margin Width
    top_missing += parseInt(seedinfo.css("borderTopWidth"), 10) + parseInt(seedinfo.css("borderBottomWidth"), 10); //Total Border Width

    var play_area = window.innerHeight - top_missing;

    canvas_size = play_area - 10;
    $("#infopane").css("max-height", canvas_size);


    sector.width = sector.height = canvas_size;
    ctx.fillStyle = "black";
    ctx.fillRect(0,0,canvas_size,canvas_size);

    ctx.save();
    var ratio = canvas_size / 600;
    ctx.scale(ratio, ratio);

    for (var site in diagram.cells) {
        var cell = diagram.cells[site];
        var halfedges = cell.halfedges,
                nHalfedges = halfedges.length;
        if (nHalfedges > 2) {
            var v = halfedges[0].getStartpoint();
            ctx.beginPath();
            ctx.moveTo(v.x, v.y);
            for (var iHalfedge = 0; iHalfedge < nHalfedges; iHalfedge++) {
                v = halfedges[iHalfedge].getEndpoint();
                ctx.lineTo(v.x, v.y);
            }
            ctx.fillStyle = empires[cell.site.empire].background_colour;
            ctx.fill();
            ctx.strokeStyle = empires[cell.site.empire].border_colour;
            ctx.strokeStyle = empires[cell.site.empire].border_colour;
            ctx.stroke();
        }
    }

    if (selected) {
        for (var site in diagram.cells) {
            var cell = diagram.cells[site];
            if (cell.site == selected) {
                var halfedges = cell.halfedges,
                        nHalfedges = halfedges.length;
                if (nHalfedges > 2) {
                    var v = halfedges[0].getStartpoint();
                    ctx.beginPath();
                    ctx.moveTo(v.x, v.y);
                    for (var iHalfedge = 0; iHalfedge < nHalfedges; iHalfedge++) {
                        v = halfedges[iHalfedge].getEndpoint();
                        ctx.lineTo(v.x, v.y);
                    }
                    ctx.setLineDash([2, 4]);
                    ctx.lineDashOffset = ((+new Date) / 100) % 6;
                    ctx.strokeStyle = "white";
                    ctx.stroke();
                    ctx.setLineDash([]);
                    ctx.lineDashOffset = 0;
                }
                break;
            }
        }
    }

    ctx.strokeStyle = "#404040";
    ctx.setLineDash([2, 4]);
    ctx.beginPath();
    for (star in stars) {
        var start = stars[star];
        for (var route in start.routes) {
            route = start.routes[route];
            var destination = stars[route];
            ctx.moveTo(start.x, start.y);
            ctx.lineTo(destination.x, destination.y);
        }
    }
    ctx.stroke();
    ctx.setLineDash([]);
    for (star in stars) {
        star = stars[star];
        var s = star_sizes[star.class.charAt(0)],
                s2 = s / 2;
        if (star.name == empires[star.empire].seat) {
            ctx.fillStyle = empires[star.empire].colour;
            ctx.fillRect(star.x - s2 - 4.5, star.y - s2 - 4.5, s + 9, s + 9);
        }
        ctx.fillStyle = "black";
        ctx.fillRect(star.x - s2 - 1, star.y - s2 - 1, s + 2, s + 2);
        ctx.fillStyle = star_colours[star.class.charAt(0)];
        ctx.fillRect(star.x - s2, star.y - s2, s, s);
    }

    ctx.restore();
}

var stars = {},
    empires = {},
    sector = document.getElementById("sector"),
    ctx = sector.getContext("2d"),
    voronoi = new Voronoi(),
    diagram, treemap, selected,
    stats;

if (!ctx.setLineDash) {
    ctx.setLineDash = function () {}
}

var system_data;

$.ajax({
    dataType: "json",
    url: "/json/sector/" + seed + ".json",
    success: function (data, status, xhr) {
        stats = data.stats;
        sector.width = sector.height = canvas_size;
        ctx.fillStyle = "black";
        ctx.fillRect(0,0,canvas_size,canvas_size);

        var star;

        for (var i in data.empires) {
            var empire = data.empires[i];
            empires[empire.name] = empire;
            empire.colour = "hsl(" + fmod(i * 0.618033988749895, 1.0)*360 + ", 50%, 40%)";
            empire.background_colour = "hsl(" + fmod(i * 0.618033988749895, 1.0)*360 + ", 50%, " + Math.sqrt(1.0 - fmod(i * 0.618033988749895, 0.5))*10 + "%)";
            empire.border_colour = "hsl(" + fmod(i * 0.618033988749895, 1.0)*360 + ", 50%, " + Math.sqrt(1.0 - fmod(i * 0.618033988749895, 0.5))*5 + "%)";
        }
        empires["Independent"] = {
            name: "Independent",
            colour: "black",
            background_colour: "black",
            border_colour: "#0D0D0D"
        };

        for (star in data.stars) {
            star = data.stars[star];
            star.x = star.location[0] * 27 + 300;
            star.y = star.location[1] * 27 + 300;
            stars[star.name] = star;
        }

        diagram = voronoi.compute(data.stars, {xl:0,xr:ctx.canvas.width,yt:0,yb:ctx.canvas.height});
        treemap = buildTreemap(diagram);

        var draw_loop = function () {
            draw_map();
            requestAnimationFrame(draw_loop);
        };
        draw_loop();

        $("#sector").mousedown(click_handler);
        unselect();
    }
});
