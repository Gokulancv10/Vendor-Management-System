from datetime import timedelta

from django.db import models
from django.db.models import (
    Avg,
    Case,
    Count,
    DurationField,
    ExpressionWrapper,
    F,
    FloatField,
    IntegerField,
    Q,
    When,
)
from django.db.models.signals import post_save
from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True, max_length=100)

    def save_avg_response_time(self):
        average_response_time = (
            self.purchased_orders.filter(acknowledgment_date__isnull=False)
            .annotate(
                diff=ExpressionWrapper(
                    F("acknowledgment_date") - F("issue_date"),
                    output_field=DurationField(),
                )
            )
            .aggregate(avg=Avg("diff"))["avg"]
            .total_seconds()
            / 86400
        )
        HistoricalPerformance.objects.get_or_create(
            vendor=self,
            defaults=dict(
                average_response_time=average_response_time,
                date=timezone.now() + timedelta(hours=5, minutes=30),
            ),
        )


class PurchaseOrder(models.Model):
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    STATUS_CHOICES = (
        (PENDING.upper(), PENDING),
        (COMPLETED.upper(), COMPLETED),
        (CANCELLED.upper(), CANCELLED),
    )
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="purchased_orders"
    )
    order_date = models.DateTimeField(auto_created=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=PENDING.upper()
    )
    quality_rating = models.FloatField(default=0)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="historical_performances"
    )
    date = models.DateTimeField(auto_created=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)


def update_historical_perfromance_metrics(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.status != PurchaseOrder.PENDING.upper():
        metrics = instance.vendor.purchased_orders.aggregate(
            total_orders=Count("id", distinct=True, output_field=IntegerField()),
            total_completed_orders=Count(
                "id",
                distinct=True,
                filter=Q(status=PurchaseOrder.COMPLETED.upper()),
                output_field=IntegerField(),
            ),
            completed_orders_on_time=Count(
                "id",
                distinct=True,
                filter=Q(status=PurchaseOrder.COMPLETED.upper())
                & Q(acknowledgment_date__lte=F("delivery_date")),
                output_field=IntegerField(),
            ),
            avg_quality_rating=Avg(
                "quality_rating",
                output_field=FloatField(),
                filter=(~Q(status=PurchaseOrder.PENDING.upper())),
            ),
            ontime_delivery_rate=Case(
                When(
                    Q(completed_orders_on_time__gt=0) & Q(total_completed_orders__gt=0),
                    then=F("completed_orders_on_time")
                    * 1.0
                    / F("total_completed_orders"),
                ),
                default=0,
                output_field=FloatField(),
            ),
            fulfillment_rate=Case(
                When(
                    Q(total_completed_orders__gt=0) & Q(total_orders__gt=0),
                    then=F("total_completed_orders") * 1.0 / F("total_orders"),
                ),
                default=0,
                output_field=FloatField(),
            ),
        )
        HistoricalPerformance.objects.filter(vendor=instance.vendor).update(
            quality_rating_avg=metrics["avg_quality_rating"],
            fulfillment_rate=metrics["fulfillment_rate"],
            on_time_delivery_rate=metrics["ontime_delivery_rate"],
        )


post_save.connect(
    update_historical_perfromance_metrics,
    sender=PurchaseOrder,
)
