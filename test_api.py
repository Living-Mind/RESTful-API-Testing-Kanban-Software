import requests
import json
import pytest
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

key = config.get("API", "key")
url = "https://none3m.kanbanize.com/api/v2/"
headers = {"apikey": key}

def last_card():

    response = requests.get(f'{url}cards', headers=headers)

    last_card = response.json()["data"]["data"][0]

    return last_card


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

    #print(last_card())

    assert last_card()["title"] == "new-card"
    assert last_card()["color"] != "34a97b"


#PATCH METHOD (Changing the column of the created card)
def test_change_column():

    response = requests.get(f'{url}cards', headers=headers)

    #print(last_card())

    #last_card_id = last_card()["card_id"]

    payload = {
        "column_id": 3,
        "workflow_id": 1,
        }

    response = requests.patch(f'{url}cards/{last_card()["card_id"]}', headers=headers, json=payload)

    
    response = requests.get(f'{url}cards', headers=headers)

    #print(last_card())

    assert last_card()["column_id"] == 3, "Card column ID should be 3"


# PATCH METHOD (Changing the card to not existing column)
def test_change_false_column():

    payload = {
        "column_id": 6
    }

    response = requests.patch(f'{url}cards/{last_card()["card_id"]}', headers=headers, json=payload)
    
    assert response.status_code == 200, f"Status Code: {response.status_code}"


test_new_card()
test_check_card()
test_change_column()
test_change_false_column()


