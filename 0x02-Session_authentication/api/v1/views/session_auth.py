#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv

SEASSION_NAME = getenv('SESSION_NAME')


@app_views.route('/auth_session/login/', methods=['POST'],
                 strict_slashes=False)
def auth_session_login() -> str:
    """
    POST /api/v1/auth_session/login/
    """

    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})

    if not user or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(SEASSION_NAME, session_id)
    return response
