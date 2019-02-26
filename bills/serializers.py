from rest_framework import serializers

from bills.models import BillInformation
from bills.calculate import calculate_duration_time


class BillInformationSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    destination_number = serializers.SerializerMethodField()

    class Meta:
        model = BillInformation
        fields = ("destination_number", "start", "end", "price", "duration")

    def get_duration(self, obj):
        return calculate_duration_time(obj.start, obj.end)

    def get_destination_number(self, obj):
        return obj.source.source
