from rest_framework.reverse import reverse

from bills.models import BillInformation
from pricing_rules import standing_charge, charge_22_6, charge_6_22
import pytest

pytestmark = pytest.mark.django_db


def test_bill_calculation_response_single(client):
    start = {"type": "start",
             "timestamp": "2018-02-22T21:59:00Z",
             "call_id": 10,
             "source": "1888888888",
             "destination": "1688888888"}

    end = {"type": "end",
           "timestamp": "2018-02-22T22:01:00Z",
           "call_id": 10}

    response = client.post(reverse("records-list"), start)
    assert response.status_code == 201

    response = client.post(reverse("records-list"), end)
    assert response.status_code == 201

    assert BillInformation.objects.all()[0].price == standing_charge + charge_6_22 + charge_22_6

    response = client.get(reverse("bills-list"), {"source": "1888888888", "month": "2", "year": "2018"})
    assert response.status_code == 200
    bills = response.data["bills"][0]
    assert bills["destination_number"] == "1688888888"
    assert bills["price"] == "0.45"
    assert bills["duration"] == "0h2m0s"


def test_bill_calculation_response_2(client):
    start = {"type": "start",
             "timestamp": "2018-10-10T10:15:25-03:00",
             "call_id": 10,
             "source": "1888888888",
             "destination": "1688888888"}

    end = {"type": "end",
           "timestamp": "2018-10-10T10:25:10-03:00",
           "call_id": 10}

    response = client.post(reverse("records-list"), start)
    assert response.status_code == 201
    response = client.post(reverse("records-list"), end)
    assert response.status_code == 201

    start = {"type": "start",
             "timestamp": "2018-09-30T23:55:00-03:00",
             "call_id": 11,
             "source": "1888888888",
             "destination": "1788888888"}

    end = {"type": "end",
           "timestamp": "2018-10-01T00:01:00-03:00",
           "call_id": 11}

    response = client.post(reverse("records-list"), start)
    assert response.status_code == 201
    response = client.post(reverse("records-list"), end)
    assert response.status_code == 201

    response = client.get(reverse("bills-list"), {"source": "1888888888", "month": "10", "year": "2018"})
    assert response.status_code == 200
    bills = response.data["bills"]
    assert len(bills) == 2
    assert bills[0]["price"] == str(standing_charge + 9 * (charge_6_22))
    assert bills[0]["duration"] == "0h9m45s"
    assert bills[0]["destination_number"] == "1688888888"

    assert bills[1]["price"] == str(standing_charge + 6 * (charge_22_6))
    assert bills[1]["duration"] == "0h6m0s"
    assert bills[1]["destination_number"] == "1788888888"
