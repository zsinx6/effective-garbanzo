"""Stores information about the calling price, to make it easier to change

Standing charge: R$ 0,36 (fixed charges that are used to pay for the cost of the connection);
Standard time call - between 6h00 and 22h00 (excluding): charge_6_22
Reduced tariff time call - between 22h00 and 6h00 (excluding): charge_22_6
"""

import decimal

standing_charge = decimal.Decimal("0.36")
charge_6_22 = decimal.Decimal("0.09")
charge_22_6 = decimal.Decimal("0.00")
