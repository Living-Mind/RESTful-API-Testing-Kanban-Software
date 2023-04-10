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

# POST METHOD (Creating new card)
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


# GET METHOD (Checking for new card)
def test_check_card():

    response = requests.get(f'{url}cards', headers=headers)

    #print(last_card())

    assert last_card()["title"] == "new-card"
    assert last_card()["color"] != "34a97b"


# PATCH METHOD (Changing the column of the created card)
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


# PATCH METHOD (Validate Error: Changing the card to not existing column)
def test_VE_change_false_column():

    payload = {
        "column_id": 6
    }

    response = requests.patch(f'{url}cards/{last_card()["card_id"]}', headers=headers, json=payload)
    
    assert response.status_code == 200, f"Status Code: {response.status_code}"


# PATCH METHOD (Creating a subtask to an existing card)
def test_create_subtask():

    payload = {
        "subtasks_to_add": 
        [
            {
          "description": "Subtask Creation Test"
          }
          ]
    }

    response = requests.patch(f'{url}cards/{last_card()["card_id"]}', headers=headers, json=payload)

    assert response.status_code == 200, f"Status Code: {response.status_code}"


# PATCH METHOD (Converting a subtask to a card in "Requested" column)
def test_convert_to_link_card():

    response = requests.get(f'{url}cards/{last_card()["card_id"]}', headers=headers)

    subtask_id = response.json()["data"]["subtasks"][0]["subtask_id"]

    payload = {

    "subtasks_to_convert_into_cards": [
        {
            "subtask_id": f'{subtask_id}',
            "column_id": 2,
            "links_to_existing_cards_to_add_or_update": [ 
                {

                    "linked_card_id": f'{last_card()["card_id"]}',
                    "link_type": "parent",
            }

            ]
        }
]
}

    response = requests.patch(f'{url}cards/{last_card()["card_id"]}', headers=headers, json=payload)

    assert response.status_code == 200, f"Status Code: {response.status_code}"
 

# DELETE METHOD (Deleting a card)
def test_delete_card():

    response = requests.delete(f'{url}cards/{last_card()["card_id"]}', headers=headers)

    assert response.status_code == 204, f"Status Code: {response.status_code}"

# PATCH METHOD (Validate Error: Changing the size of not existing card)
def test_VE_size_change():

    payload = {
        "size": 30
        }

    response = requests.patch(f'{url}cards/-1', headers=headers, json=payload)

    assert response.status_code == 404, f"Status Code: {response.status_code}"

# POST METHOD (Validate Error: Creating a card with deadline before 1970-01-01)
def test_VE_card_deadline():

    payload = {

    "column_id": 2,
    "lane_id": 1,
    "position": 2,
    "workflow_id": 1,
    "title": "Very old card",
    "priority": 100,
    "color": "#18f0c1",
    "deadline": "1950-01-01T11:00:26.848Z"
}

    response = requests.post(f'{url}/cards', headers=headers, json=payload)

    assert response.status_code == 400, f'Status Code: {response.status_code}'