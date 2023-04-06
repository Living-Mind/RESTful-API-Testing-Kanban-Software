import requests
import json
import pytest
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

key = config.get("API", "key")
url = "https://none3m.kanbanize.com/api/v2/"
headers = {"apikey": key}

#POST METHOD (Creating new card)
def test_new_card():
    payload = {
        "column_id": 2,
        "lane_id": 1,
        "position": 2,
        "workflow_id": 1,
        "title": "new-card",
        "priority": 1,
        "color": "7054fe"
        }
    
    response = requests.post(f'{url}cards', headers=headers, json=payload)

    assert response.status_code == 200
    #assert response.json()["data"][0]["title"] == "new-card", "Card with title not found"
    print(response.json()["data"][0])


#GET METHOD (Checking for new card)
def test_check_card():

    response = requests.get(f'{url}cards', headers=headers)

    last_card = response.json()["data"]["data"][0]

    #print(last_card)

    assert last_card["title"] == "new-card"
    assert last_card["color"] != "34a97b"

    