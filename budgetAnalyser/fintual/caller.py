import json
import requests

import secrets



def get_user_info(username):
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
    token = res["data"]["attributes"]["token"]

    headers = {
        'Accept': 'application/json',
    }
    params = (
        ('user_token', token),
        ('user_email', email),
    )

    response = requests.get('https://fintual.cl/api/goals', headers=headers, params=params)
    goals = json.loads(response.text)["data"]
    for goal in goals:
        print(goal["attributes"]["deposited"])
        print(goal["attributes"]["nav"])
