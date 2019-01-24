from django.db import models

from records.models import CallRecord
from bills.calculate import calculate_price


class BillInformation(models.Model):
    source = models.ForeignKey(CallRecord, on_delete=models.CASCADE)
    destination = models.ForeignKey(CallRecord, on_delete=models.CASCADE)
    start = models.DateTimeField(null=False, blank=False)
    end = models.DateTimeField(null=False, blank=False)
    price = models.DecimalField(null=False, max_digits=19, decimal_places=2)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.price = calculate_price(self.start, self.end)
        super(BillInformation, self).save(*args, **kwargs)
