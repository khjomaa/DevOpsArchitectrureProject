import json
import requests

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


def search_user(url, username, password):
    payload = {}
    res = requests.get(url, auth=(username, password), headers=headers, data=payload)
    return res.status_code, res.json()


def create_user(url, username, password, payload):
    payload = json.dumps(payload)
    res = requests.post(url, auth=(username, password), headers=headers, data=payload)
    return res.status_code, res.json()


def change_user_permission(url, username, password, payload):
    payload = json.dumps(payload)
    res = requests.put(url, auth=(username, password), headers=headers, data=payload)
    return res.status_code, res.json()


def delete_user_from_grafana(url, username, password):
    payload = {}
    res = requests.delete(url, auth=(username, password), headers=headers, data=payload)
    return res.status_code, res.json()
