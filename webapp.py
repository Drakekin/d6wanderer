# coding=utf-8
from flask import Flask, Response, render_template
from json import dumps
from character.generator import Character, DRAFT
from util.custom_json_encoder import ObjectJSONEncoder
from sector.generator import generate_sector
from random import choice, Random

SEED_LETTERS = "012346789ABCDEFGHJKLMNPQRSTUWXYZ"

app = Flask(__name__)


@app.route("/json/sector.json")
@app.route("/json/sector/<seed>.json")
def json_sector(seed=None):
    stars, empires, analysis = generate_sector(seed)
    return Response(
        response=dumps({"stars": stars, "empires": empires, "stats": analysis}, cls=ObjectJSONEncoder),
        status=200,
        mimetype="application/json"
    )


@app.route("/json/character.json")
@app.route("/json/character/<name>.json")
def json_character(name="Jon Smith"):
    rng = Random(name)
    character = Character(rng, name, rng.choice(DRAFT))
    return Response(
        response=dumps(character, cls=ObjectJSONEncoder),
        status=200,
        mimetype="application/json"
    )

@app.route('/sector')
@app.route('/sector/<seed>')
def show_sector(seed=None):
    if not seed:
        seed = "".join([
            choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), choice("0123456789"), choice("ABCDEFGHJKLMNPQRSTUWXYZ"), "-",
            choice(SEED_LETTERS), choice(SEED_LETTERS),
            choice(SEED_LETTERS), choice(SEED_LETTERS)
        ])
    return render_template("sector.html", seed=seed)

@app.route('/character')
@app.route('/character/<name>')
def show_character(name="John Smith"):
    rng = Random(name)
    return render_template("character.html", name=name, character=Character(rng, name, rng.choice(DRAFT)).html())


if __name__ == "__main__":
    app.run("0.0.0.0", 5555, debug=True)
