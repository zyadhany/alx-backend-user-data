#!/usr/bin/env python3
"""
Main file
"""
import requests
import sys
import os
from typing import List, Dict, Any, Union

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Register a user
    """
    url = "http://localhost:5000/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    if response.status_code == 400:
        print("User already registered")
        return
    if response.status_code != 200:
        raise Exception("Invalid response")
    print("User registered")


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with wrong password
    """
    url = "http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    if response.status_code != 401:
        raise Exception("Invalid response")
    print("Log in failed")


def profile_unlogged() -> None:
    """Profile unlogged
    """
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    if response.status_code != 403:
        raise Exception("Invalid response")
    print("Profile unlogged")


def log_in(email: str, password: str) -> str:
    """Log in
    """
    url = "http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception("Invalid response")
    print("Logged in")
    return response.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """Profile logged
    """
    url = "http://localhost:5000/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    if response.status_code != 200:
        raise Exception("Invalid response")
    print("Profile logged")


def log_out(session_id: str) -> None:
    """Log out
    """
    url = "http://localhost:5000/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    if response.status_code != 302:
        raise Exception("Invalid response")
    print("Logged out")


def reset_password_token(email: str) -> str:
    """Reset password token
    """
    url = "http://localhost:5000/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception("Invalid response")
    print("Reset password token")
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password
    """
    url = "http://localhost:5000/\
           reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)
    if response.status_code != 200:
        raise Exception("Invalid response")
    print("Password updated")


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
