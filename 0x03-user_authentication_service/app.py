#!/usr/bin/env python3
"""
Main file
"""
import logging

import flask
from flask import jsonify, request, redirect, abort
from auth import Auth

logging.disable(logging.WARNING)

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
    """DELETE /sessions
    Return:
        - A redirect if successful
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST /reset_password
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    PUT /reset_password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    GET /profile
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    GET /
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
