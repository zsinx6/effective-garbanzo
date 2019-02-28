import datetime
import decimal

from pricing_rules import standing_charge, charge_22_6, charge_6_22


def calculate_price(start, end):
    """Receives the start and end times as timestamp, and calculates the price using the
    information in pricing_rules.
    """

    decimal.getcontext().prec = 19
    cost = standing_charge
    temp_time = start

    while temp_time + datetime.timedelta(minutes=1) <= end:
        if 6 <= temp_time.hour < 22:
            cost += charge_6_22
        else:
            cost += charge_22_6
        temp_time += datetime.timedelta(minutes=1)

    return cost


def calculate_duration_time(start, end):
    """Calculates the duration in the format of <hours>h<minutes>m<seconds>s
    given start and end timestamps.
    """

    diff = end - start
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return "{hours}h{minutes}m{seconds}s".format(hours=hours, minutes=minutes, seconds=seconds)
