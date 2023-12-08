import uuid
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import HistoricalPerformance, PurchaseOrder, Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "id",
            "name",
            "contact_details",
            "address",
            "vendor_code",
        )


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    average_response_time = serializers.FloatField(default=0)
    average_response_time_in_hours = serializers.FloatField(read_only=True)
    average_response_time_in_minutes = serializers.FloatField(read_only=True)
    average_response_time_in_seconds = serializers.FloatField(read_only=True)
    on_time_delivery_rate_percent = serializers.FloatField(read_only=True)
    fulfillment_rate_percent = serializers.FloatField(read_only=True)

    class Meta:
        model = HistoricalPerformance
        fields = (
            "id",
            "date",
            "average_response_time",
            "average_response_time_in_hours",
            "average_response_time_in_minutes",
            "average_response_time_in_seconds",
            "on_time_delivery_rate",
            "on_time_delivery_rate_percent",
            "quality_rating_avg",
            "fulfillment_rate",
            "fulfillment_rate_percent",
            "vendor",
        )


class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True, many=False)
    quality_rating = serializers.FloatField()
    items = serializers.JSONField()
    quantity = serializers.IntegerField(default=1)
    acknowledgment_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = (
            "id",
            "po_number",
            "order_date",
            "delivery_date",
            "items",
            "quantity",
            "status",
            "quality_rating",
            "issue_date",
            "acknowledgment_date",
            "vendor",
        )


class CreatePurchaseOrderSerializer(serializers.ModelSerializer):
    items = serializers.JSONField(required=True)
    quantity = serializers.IntegerField(default=1)
    vendor = serializers.IntegerField(required=True)

    class Meta:
        model = PurchaseOrder
        fields = (
            "quantity",
            "vendor",
            "items",
        )

    def validate_vendor(self, vendor_id):
        vendor = Vendor.objects.filter(id=vendor_id).first()
        if not vendor:
            raise serializers.ValidationError("Invalid vendor ID")
        return vendor

    def create(self, validated_data):
        validated_data["po_number"] = str(uuid.uuid4())
        order_date = timezone.now() + timedelta(hours=5, minutes=30)
        validated_data["order_date"] = order_date
        validated_data["issue_date"] = order_date
        validated_data["delivery_date"] = order_date + timedelta(days=4)
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        return purchase_order


class UpdatePurchaseOrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=PurchaseOrder.STATUS_CHOICES, required=True
    )
    quality_rating = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=True
    )

    class Meta:
        model = PurchaseOrder
        fields = (
            "status",
            "quality_rating",
        )

    def update(self, instance, validated_data):
        if not instance.acknowledgment_date:
            raise serializers.ValidationError(
                "The purchase order you are trying to update isn't acknowledged by"
                " vendor."
            )
        if instance.status in [
            PurchaseOrder.CANCELLED.upper(),
            PurchaseOrder.COMPLETED.upper(),
        ]:
            raise serializers.ValidationError(
                "The purchase order you are trying to update is already"
                f" {instance.status}"
            )
        instance.status = validated_data.get("status")
        instance.quality_rating = validated_data.get("quality_rating")
        return super().update(instance, validated_data)
