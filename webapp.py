from flask import Flask, Response, render_template
from json import dumps
from util.custom_json_encoder import ObjectJSONEncoder
from sector.generator import generate_sector
from random import choice

SEED_LETTERS = "012346789ABCDEFGHJKLMNPQRSTUWXYZ"

app = Flask(__name__)


@app.route("/json/sector.json")
@app.route("/json/sector/<seed>.json")
def json_sector(seed=None):
    stars, empires = generate_sector(seed)
    return Response(
        response=dumps({"stars": stars, "empires": empires}, cls=ObjectJSONEncoder),
        status=200,
        mimetype="application/json"
    )

@app.route('/sector')
@app.route('/sector/<seed>')
def show_sector(seed=None):
    if not seed:
        seed = "".join([
            choice("SRCG"), choice("0123456789"), choice("ABCDEFGHJKLMNPQRSTUWXYZ"), "-",
            choice(SEED_LETTERS), choice(SEED_LETTERS),
            choice(SEED_LETTERS), choice(SEED_LETTERS)
        ])
    return render_template("sector.html", seed=seed)


if __name__ == "__main__":
    app.run("0.0.0.0", 5555, debug=True)
