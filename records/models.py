from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class CallRecord(models.Model):
    type = models.CharField(choices=["start", "end"])
    timestamp = models.DateTimeField(null=False, blank=False)
    call_id = models.BigIntegerField(null=False, blank=False)
    phone_regex = RegexValidator(regex=r'^\d{10,11}$',
                                 message="The phone number format is AAXXXXXXXXX, where AA is the "
                                 "area code and XXXXXXXXX is the phone number. The area code is "
                                 "always composed of two digits while the phone number can be "
                                 "composed of 8 or 9 digits.")
    source = models.CharField(max_length=11, validators=[phone_regex])
    destination = models.CharField(max_length=11, validators=[phone_regex])

    def save(self, *args, **kwargs):
        if self.source == self.destination:
            raise ValidationError("Source must differ from destination.")
        other = CallRecord.objects.get(call_id=self.call_id)
        count = other.count()
        if count == 1 and other.first().type == self.type:
            raise ValidationError("Only one 'start' and 'end' for each call_id.")
        elif count >= 2:
            raise ValidationError("This call_id is already in use.")
        super(CallRecord, self).save(*args, **kwargs)
