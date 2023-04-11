# RESTful API Testing for Kanbanize Software

This repository contains automated tests for the [Kanbanize] (https://kanbanize.com) RESTful API. The tests are implemented using Python and pytest testing framework.

## Sources

* [Kanbanize] (https://kanbanize.com)
* [API documentation] (https://test.kanbanize.com/openapi/) (Swagger UI)

## Requirements

* Python 3.6 or later
* Requests library (can be installed using pip install requests)
* Pytest (can be installed using pip install pytest)

## Getting Started

1. Clone this repository
2. Install the requirements using pip
3. Create and update the config.ini file with your Kanbanize API key
4. Run the tests using pytest

## Configuration

The config.ini file contains the following settings:

* key: The Kanbanize API key

## Tests

The following tests are implemented:

 * test_new_card: POST (Creating new card)
 * test_check_card: GET (Checking for new card)
 * test_change_column: PATCH (Changing the column of the created card)
 * test_VE_change_false_column: PATCH (Validate Error: Changing the card to not existing column)
 * test_create_subtask: PATCH (Creating a subtask to an existing card)
 * test_convert_to_link_card: PATCH (Converting a subtask to a card in "Requested" column)
 * test_delete_card: DELETE (Deleting a card)
 * test_VE_size_change: PATCH (Validate Error: Changing the size of not existing card)
 * test_VE_card_deadline: POST (Validate Error: Creating a card with deadline before 1970-01-01)
