# Work at Olist

## [Heroku deploy](https://effective-garbanzo.herokuapp.com)

## Description
This is a simple project for receive call records and calcule the billing information, based on some pricing rules, 
for more information click [here](https://github.com/olist/work-at-olist).

The code base is Python 3.6 with Django REST framework and Postgresql as database.

## Install
To install:

Create a database inside the postgresql where the name of the database is 'olist'.

Then run:
```bash
$ pip install -r requirements.txt
```

To run on local
```bash
$ export DJANGO_SETTINGS_MODULE=olist.settings_test
$ export DBUSER=<DBUSER>
$ python manager.py runserver
```

#### Testing
For testing just run:

```bash
$ pytest
```

## Development Environment
* **Operating System:** Arch Linux
* **IDE:** neovim with [this](https://github.com/rafi/vim-config)
* **PEP 8 helper:** Flake8

## Libraries
#### For testing
* pytest and pytest-django for running the tests
* factory-boy for generate objects directly on django

#### Dabatase Connection
* psycopg2

## API Information

### /records
This endpoint accepts GET and POST requests

#### POST format:
There are two types of Records, the **Start** and the **End**

Here is the json format for them:

    start = {"type": "start",
             "timestamp": "2018-02-22T21:59:00Z",
             "call_id": 10,
             "source": "1888888888",
             "destination": "1688888888"}

    end = {"type": "end",
           "timestamp": "2018-02-22T22:01:00Z",
           "call_id": 10}
Only one can be sent to /records per time.

#### GET format:
Simply gets every CallRecord and show in json format.

### /bills
This endpoint only accepts GET requests

#### GET format:
There must be a source args in the request, for example:

```
https://effective-garbanzo.herokuapp.com/bills/?source=1888888888
```

The source is the subscriber telephone number for the telephone bill request.

Optionally the month and the year (period for the telephone bill request) can also be sent as args:
```
https://effective-garbanzo.herokuapp.com/bills/?source=1888888888&month=10&year=2018
```

If there is no period information, the last month is used.

The response is a json in the format:
```python
{
    "source": "1888888888",
    "period": "1/2019",
    "bills": [
        {
            "destination_number": "1788888888",
            "start": "2019-01-16T10:55:00",
            "end": "2019-01-16T10:58:00",
            "price": "0.63",
            "duration": "0h3m0s"
        }
    ]
}
```

Where the bills are a array with every occurence of billing charge.
