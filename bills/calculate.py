import datetime

from pricing_rules import standing_charge, charge_22_6, charge_6_22


def calculate_price(start, end):
    cost = standing_charge
    temp_time = start

    while temp_time <= end:
        if 6 <= temp_time.hour < 22:
            cost += charge_6_22
        else:
            cost += charge_22_6
        temp_time = start + datetime.timedelta(minute=1)

    return cost


def calculate_duration_time(start, end):
    diff = end - start
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return "{hours}h{minutes}m{seconds}s".format(hours=hours, minutes=minutes, seconds=seconds)
