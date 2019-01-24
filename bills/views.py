from rest_framework import viewsets

from bills.models import BillInformation
from bills.serializers import BillInformationSerializer


class BillInformationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BillInformation.objects.all()
    serializer_class = BillInformationSerializer
