# coding: utf-8
from django.db.models import Q, F
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

from composition.permissions import CompositionPermission, CompositionImagePermission
from employee.models import Operator
from composition.models import Composition
from composition.serializers import CompositionSerializer, CompositionDetailSerializer, CompositionImageSerializer


class IsApproverOrNoOneFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows to get the list which belong to approver or no owner ones.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(approver=request.user,status=Composition.APPROVING) \
            | Q(status=Composition.WAIT_APPROVAL))

class ImageUploadFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows to get the list which belong to approver or no owner ones.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(creator=request.user,status=Composition.WAIT_APPROVAL) \
            | Q(approver=request.user,status=Composition.FINISH_APPROVAL))


class CompositionList(generics.ListCreateAPIView):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer
    filter_backends = (IsApproverOrNoOneFilterBackend,)
    permission_classes = (CompositionPermission,)

    def perform_create(self, serializer):
        Operator.objects.filter(user=self.request.user).update(created_count=F('created_count') + 1)
        serializer.save(creator=self.request.user)


class CompositionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Composition.objects.all()
    serializer_class = CompositionDetailSerializer
    filter_backends = (IsApproverOrNoOneFilterBackend,)
    permission_classes = (CompositionPermission,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance and instance.status == Composition.WAIT_APPROVAL:
            instance.status = Composition.APPROVING # mark as approving status
            instance.approver = request.user # attach to the exact approver
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        Operator.objects.filter(user=self.request.user).update(approved_count=F('approved_count') + 1)
        serializer.save(status=Composition.FINISH_APPROVAL) # finish approval status


class CompositionImage(generics.UpdateAPIView):
    queryset = Composition.objects.all()
    serializer_class = CompositionImageSerializer
    filter_backends = (ImageUploadFilterBackend,)
    parser_classes = (MultiPartParser,)
    permission_classes = (CompositionImagePermission,)



