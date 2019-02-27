from rest_framework.reverse import reverse

from bills.models import BillInformation
import pytest

pytestmark = pytest.mark.django_db


def test_bill_creation_single(client):
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

    assert len(BillInformation.objects.all()) == 1


def test_bill_creation_2(client):
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

    assert len(BillInformation.objects.all()) == 2
