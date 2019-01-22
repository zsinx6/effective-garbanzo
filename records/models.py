from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class CallRecord(models.Model):
    type = models.CharField(choices=[("start", "Call Start Record"),
                                     ("end", "Call End Record")], max_length=5)
    timestamp = models.DateTimeField(null=False, blank=False)
    call_id = models.BigIntegerField(null=False, blank=False)
    phone_regex = RegexValidator(regex=r'^\d{10,11}$',
                                 message="The phone number format is AAXXXXXXXXX, where AA is the "
                                 "area code and XXXXXXXXX is the phone number. The area code is "
                                 "always composed of two digits while the phone number can be "
                                 "composed of 8 or 9 digits.")
    source = models.CharField(max_length=11, validators=[phone_regex],
                              null=True, default=None, blank=False)
    destination = models.CharField(max_length=11, validators=[phone_regex],
                                   null=True, default=None, blank=False)

    def check_date(self, other):
        if other.type == "start" and other.timestamp < self.timestamp:
            return True
        elif other.type == "end" and other.timestamp > self.timestamp:
            return True
        return False

    def save(self, *args, **kwargs):
        if self.type == "start" and (not self.source or not self.destination):
            raise ValidationError("Call Start Record must have source and destination")
        elif self.type == "end" and (self.source or self.destination):
            raise ValidationError("Call End Record must not have source nor destination")
        if self.source == self.destination and self.source:
            raise ValidationError("Source must differ from destination.")
        other = CallRecord.objects.filter(call_id=self.call_id)
        count = other.count()
        if count == 1 and other.first().type == self.type:
            raise ValidationError("Only one 'start' and 'end' for each call_id.")
        elif count >= 2:
            raise ValidationError("This call_id is already in use.")
        elif count == 1 and not self.check_date(other.first()):
            raise ValidationError("Date interval is bad.")
        super(CallRecord, self).save(*args, **kwargs)
