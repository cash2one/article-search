# coding: utf-8
from rest_framework import generics
from rest_framework import filters

from employee.models import Operator
from employee.serializers import EmployeeDetailSerializer

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)

class EmployeeDetail(generics.RetrieveAPIView):
    queryset = Operator.objects.all()
    serializer_class = EmployeeDetailSerializer
    filter_backends = (IsOwnerFilterBackend,)
