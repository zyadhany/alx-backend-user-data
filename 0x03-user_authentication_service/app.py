#!/usr/bin/env python3
"""
Main file
"""

import flask
from flask import jsonify, request
from auth import Auth


AUTH = Auth()
app = flask.Flask(__name__)


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> str:
    """
    POST /users
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


def login() -> str:
    """
    POST /sessions
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        reponse = jsonify({"email": email, "message": "logged in"})
        reponse.set_cookie("session_id", session_id)
        return reponse
    return jsonify({"message": "wrong password"}), 401


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    GET /
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
