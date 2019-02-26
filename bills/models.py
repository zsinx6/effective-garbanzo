from django.db import models
import decimal

from records.models import CallRecord
from bills.calculate import calculate_price


class BillInformation(models.Model):
    source = models.ForeignKey(CallRecord, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_source")
    start = models.DateTimeField(null=False, blank=False)
    end = models.DateTimeField(null=False, blank=False)
    price = models.DecimalField(null=False, max_digits=19, decimal_places=2)

    def save(self, *args, **kwargs):
        decimal.getcontext().prec = 19
        self.price = calculate_price(self.start, self.end)
        self.full_clean()
        super(BillInformation, self).save(*args, **kwargs)
