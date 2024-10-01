#!/usr/bin/env python3
"""
Main file
"""

import flask
from flask import jsonify, request, redirect, abort
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


@app.route("/sessions", methods=["POST"])
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


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    DELETE /sessions
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    GET /
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
