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

        month = request.query_params.get("month")
        year = request.query_params.get("year")
        now = timezone.now()
        first = now.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        if not year or not month:
            month, year = lastMonth.month, lastMonth.year
        else:
            month, year = int(month), int(year)

        if not 1 <= month <= 12:
            return Response("invalid month", 400)
        if (year > now.year) or (year == now.year and month >= now.month):
            return Response("only closed periods are permitted", 400)

        queryset = BillInformation.objects.all()
        queryset = queryset.filter(source__source=source, end__year=year, end__month=month)
        serializer = BillInformationSerializer(queryset, many=True)
        billing = {"source": source,
                   "period": str(month) + "/" + str(year),
                   "bills": serializer.data}
        return Response(billing)
