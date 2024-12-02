# Profile matcher service
This project is a service based on Django that retrieves information from player profiles and campaigns through a REST API. Data are stored in an SQLite database and are loaded before starting the server with fixtures.

## How to execute
1. Activate virtual environment
```
source venv/bin/activate
```

2. Configure database
```
python manage.py migrate
```

3. Load data
```
python manage.py loaddata profile_matcher\data\player_profiles.json
python manage.py loaddata profile_matcher\data\campaigns.json
```

4. Start server
```
python manage.py runserver
```

5. Run endpoints:

- /api/playerprofiles/{player_id}
- /api/campaigns/{campaign_id}
- /api/get_client_config{player_id}

## Endpoint logic

### GET /playerprofiles/{player_id}

Given an existing player_id, retrieve all data of the player profile and return it on the response body.
- 200 OK
- 404 Not Found

### GET /campaigns/{campaign_id}

Given an existing campaign_id, retrieve all data of the campaign and return it on the response body.
- 200 OK
- 404 Not Found

### GET /get_client_config/{player_id}

1. Given an existing player_id
2. Retrieve player data if exists
3. Filters the campaign to get only the active campaigns according to datetimes and/or "enabled" field
4. Compare the "matchers" witht he player profile.
5. If all the "matchers" match, append the active campaign to the player profile
6. If any campaign does not match, do not assign it to the player profile.
7. Return the player profile body with the list of active campaigns.

- 200 OK
- 404 Not Found

Example of response body with the data provided under /profile_matcher/data directory:

```
{
    "player_id": "d6a92c10-2d5d-495b-9b1e-9cccada85ac4",
    "credential": "apple_credential",
    "created": "2021-01-10T13:37:17Z",
    "modified": "2021-01-23T13:37:17Z",
    "last_session": "2021-01-23T13:37:17Z",
    "total_spend": 400.0,
    "total_refund": 0.0,
    "total_transactions": 5,
    "last_purchase": "2021-01-22T13:37:17Z",
    "active_campaigns": [
        "mycampaig_2",
        "mycampaign"
    ],
    "devices": [
        {
            "id": 1,
            "model": "iphone 16",
            "carrier": "vodafone",
            "firmware": "123"
        }
    ],
    "level": 3,
    "xp": 1000,
    "total_playtime": 144.0,
    "country": "CA",
    "language": "fr",
    "birthdate": "2000-01-10T13:37:17Z",
    "gender": "male",
    "inventory": {
        "cash": 123,
        "coins": 123,
        "item_1": 1,
        "item_34": 3,
        "item_55": 2
    },
    "clan": {
        "id": 123456,
        "name": "Hello world clan"
    },
    "custom_field": "mycustom"
}
```