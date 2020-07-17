import json
import requests

import secrets


def get_goals_all_users():
    goals = []
    for username in secrets.FINTUAL_USERS:
        goals.extend(get_user_goals(username))
    for goal in goals:
        print(goal)


def get_user_goals(username):
    token = get_token(username)
    goals = get_goals(username, token)
    return format_goals(username, goals)


def get_token(username):
    email = secrets.FINTUAL_USERNAMES.get(username)
    pw = secrets.FINTUAL_PWS.get(username)

    data = '{"user":{"email":\"%s\","password":\"%s\"}}' % (email, pw)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.post(
        'https://fintual.cl/api/access_tokens',
        headers=headers,
        data=data,
    )

    res = json.loads(response.text)
    return res["data"]["attributes"]["token"]


def get_goals(username, token):
    email = secrets.FINTUAL_USERNAMES.get(username)

    headers = {
        'Accept': 'application/json',
    }
    params = (
        ('user_token', token),
        ('user_email', email),
    )

    response = requests.get('https://fintual.cl/api/goals', headers=headers, params=params)
    goals = json.loads(response.text)["data"]
    return [{
        "deposited": datum["attributes"]["deposited"],
        "value": datum["attributes"]["nav"]
    } for datum in goals]


def format_goals(username, goals):
    for goal in goals:
        goal["gain"] = goal["value"] - goal["deposited"]
        goal["user"] = username
    return goals


if "__main__" == __name__:
    get_goals_all_users()
