from rest_framework.reverse import reverse
import decimal

from bills.models import BillInformation
from pricing_rules import standing_charge, charge_22_6, charge_6_22
import pytest

pytestmark = pytest.mark.django_db


def test_bill_calculation_21_59_to_22_01(client):
    start = {"type": "start",
             "timestamp": "2019-02-21T21:59:00-03:00",
             "call_id": 10,
             "source": "1888888888",
             "destination": "1688888888"}

    end = {"type": "end",
           "timestamp": "2019-02-21T22:01:00-03:00",
           "call_id": 10}

    response = client.post(reverse("records-list"), start)
    assert response.status_code == 201

    response = client.post(reverse("records-list"), end)
    assert response.status_code == 201

    decimal.getcontext().prec = 2
    assert BillInformation.objects.all()[0].price == decimal.Decimal(standing_charge + charge_6_22 + charge_22_6)
