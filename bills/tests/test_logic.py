from django.utils import timezone

import datetime

from pricing_rules import standing_charge, charge_22_6, charge_6_22
from bills.calculate import calculate_duration_time, calculate_price


def test_duration_time_minutes():
    start = timezone.now()
    end = start + datetime.timedelta(minutes=10)
    duration = calculate_duration_time(start, end)

    assert duration == "0h10m0s"


def test_duration_time_seconds():
    start = timezone.now()
    end = start + datetime.timedelta(seconds=35)
    duration = calculate_duration_time(start, end)

    assert duration == "0h0m35s"


def test_duration_time_hours():
    start = timezone.now()
    end = start + datetime.timedelta(hours=2)
    duration = calculate_duration_time(start, end)

    assert duration == "2h0m0s"


def test_duration_time_various_days():
    start = timezone.now()
    end = start + datetime.timedelta(days=3, hours=5, minutes=16, seconds=55)
    duration = calculate_duration_time(start, end)

    assert duration == "77h16m55s"


def test_price_calculation_21_59_to_22_01():
    now = datetime.datetime.now()
    start = now.replace(hour=21, minute=59, second=0)
    end = start + datetime.timedelta(minutes=2)

    price = calculate_price(start, end)

    assert price == standing_charge + charge_6_22 + charge_22_6


def test_price_calculation_05_59_to_06_01():
    now = datetime.datetime.now()
    start = now.replace(hour=5, minute=59, second=0)
    end = start + datetime.timedelta(minutes=2)

    price = calculate_price(start, end)

    assert price == standing_charge + charge_22_6 + charge_6_22


def test_price_calculation_various_days():
    now = datetime.datetime.now()
    start = now.replace(hour=0, minute=0, second=0)
    end = start + datetime.timedelta(days=2, hours=10, minutes=6)

    price = calculate_price(start, end)

    assert price == standing_charge + (2 * 16 * 60 * charge_6_22) + (4 * 60 * charge_6_22) + (6 * charge_6_22)
