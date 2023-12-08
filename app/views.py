from datetime import timedelta

from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import PurchaseOrderFilter
from .models import HistoricalPerformance, PurchaseOrder, Vendor
from .serializers import (
    CreatePurchaseOrderSerializer,
    HistoricalPerformanceSerializer,
    PurchaseOrderSerializer,
    UpdatePurchaseOrderSerializer,
    VendorSerializer,
)


class VendorsView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = VendorSerializer

    def get_queryset(self):
        return Vendor.objects.all().order_by("id")

    def perform_create(self, serializer):
        return serializer.save()


class RetrieveVendorView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = VendorSerializer

    def get_object(self):
        return get_object_or_404(Vendor, id=self.kwargs["vendor_id"])

    def perform_destroy(self, instance):
        return instance.delete()


class PurchaseOrdersView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PurchaseOrderFilter

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreatePurchaseOrderSerializer
        return PurchaseOrderSerializer

    def get_queryset(self):
        return PurchaseOrder.objects.all().select_related("vendor").order_by("id")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        response_serializer = PurchaseOrderSerializer(data, many=False)
        return Response({"detail": response_serializer.data}, status=200)


class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return UpdatePurchaseOrderSerializer
        return PurchaseOrderSerializer

    def get_object(self):
        return get_object_or_404(PurchaseOrder, id=self.kwargs["id"])


class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PurchaseOrderSerializer

    def get_object(self):
        return get_object_or_404(PurchaseOrder, id=self.kwargs["id"])

    def update(self, request, *args, **kwargs):
        object = self.get_object()
        if object.acknowledgment_date:
            return Response(
                {
                    "error": (
                        "The purchase order has already been acknowledged by the"
                        " vendor."
                    )
                },
                status=400,
            )
        object.acknowledgment_date = timezone.now() + timedelta(hours=5, minutes=30)
        object.save()
        object.vendor.save_avg_response_time()
        return Response(
            {"detail": "The purchase order has been acknowledged successfully."},
            status=200,
        )


class VendorPerformanceView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = HistoricalPerformanceSerializer

    def get_object(self):
        vendor = get_object_or_404(Vendor, id=self.kwargs["id"])
        historical_performance = (
            HistoricalPerformance.objects.filter(vendor=vendor)
            .annotate(
                average_response_time_in_hours=F("average_response_time") * 24,
                average_response_time_in_minutes=F("average_response_time") * 1440,
                average_response_time_in_seconds=F("average_response_time") * 86400,
                fulfillment_rate_percent=F("fulfillment_rate") * 100,
                on_time_delivery_rate_percent=F("on_time_delivery_rate") * 100,
            )
            .first()
        )
        return historical_performance
