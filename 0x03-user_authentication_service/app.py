#!/usr/bin/env python3
"""
Main file
"""

import flask
from flask import jsonify

app = flask.Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    GET /
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
