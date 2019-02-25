from rest_framework import viewsets
from django.utils import timezone
import datetime

from bills.models import BillInformation
from bills.serializers import BillInformationSerializer
from rest_framework.response import Response


class BillInformationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BillInformation.objects.all()
    serializer_class = BillInformationSerializer

    def list(self, request):
        source = request.query_params.get("source")
        if not source:
            return Response("source is required", 400)
        month = int(request.query_params.get("month"))
        year = int(request.query_params.get("year"))
        now = timezone.now()
        first = now.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        if not 1 <= month <= 12:
            return Response("invalid month", 400)
        if (year > now.year) or (year == now.year and month >= now.month):
            return Response("only closed periods are permitted", 400)
        if not year or not month:
            month, year = lastMonth.month, lastMonth.year
        queryset = BillInformation.objects.all()
        queryset = queryset.filter(source=source, end__year=year, end__month=month)
        serializer = BillInformationSerializer(queryset, many=True)
        return Response(serializer.data)
