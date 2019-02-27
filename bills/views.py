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
        """The source is a required arg for the get request:
        /bills?source=9999999999

        To get a telephone bill we need two information: the subscriber
        telephone number (source) is required; the reference period (month/year)
        (optional).
        If the reference period is not informed the system will consider the
        last closed period. In other words it will get the previous month.
        It's only possible to get a telephone bill after the reference period
        has ended.

        The telephone bill itself is composed by subscriber and period
        attributes and a list of all call records of the period. A call record
        belongs to the period in which the call has ended (eg. A call that
        started on January 31st and finished in February 1st belongs to
        February period).

        Returns a json in the form:
        {
            source: source,
            period: <month>/<year>,
            bills: [
                        {
                            "destination_number": destination_number,
                            "start": start,
                            "end": end,
                            "price": price,
                            "duration": duration
                        },
                        ...
                   ]
        }
        """

        source = request.query_params.get("source")
        if not source:
            return Response("Source is required", 400)

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
            return Response("Invalid month", 400)
        if (year > now.year) or (year == now.year and month >= now.month):
            return Response("Only closed periods are permitted", 400)

        queryset = BillInformation.objects.all()
        queryset = queryset.filter(source__source=source, end__year=year, end__month=month)
        serializer = BillInformationSerializer(queryset, many=True)

        billing = {"source": source,
                   "period": str(month) + "/" + str(year),
                   "bills": serializer.data}
        return Response(billing)
