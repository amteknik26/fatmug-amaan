from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField
from django.dispatch import Signal
from django.utils import timezone

from .utils.metrics_calculator import (calculate_average_response_time,
                                       calculate_fulfillment_rate,
                                       calculate_on_time_delivery_rate,
                                       calculate_quality_rating_average)


class Vendor(models.Model):
    name = models.CharField(max_length=30)
    contact_details = models.TextField(
        db_comment="Preferably an email address",)
    address = models.TextField(max_length=100)
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(null=True, default=None)
    quality_rating_avg = models.FloatField(null=True, default=None)
    average_response_time = models.FloatField(
        null=True, default=None, db_comment="in Minutes")
    fulfillment_rate = models.FloatField(null=True, default=None)

    def update_on_time_delivery_rate(self, order_instance):
        on_time_delivery_rate = calculate_on_time_delivery_rate(
            self, order_instance)
        self.on_time_delivery_rate = on_time_delivery_rate
        self.save()

    def update_quality_rating_avg(self, order_quality_rating):
        # Calculate the average of quality ratings for completed POs
        quality_rating_avg = calculate_quality_rating_average(
            self, order_quality_rating)
        self.quality_rating_avg = quality_rating_avg
        self.save()

    def update_average_response_time(self, order_instance):
        # Calculate the average response time for acknowledged POs
        acknowledged_pos = calculate_average_response_time(
            self, order_instance)
        self.average_response_time = acknowledged_pos
        self.save()

    def update_fulfillment_rate(self):
        # Calculate the fulfillment rate for all POs
        fulfillment_rate = calculate_fulfillment_rate(self)
        self.fulfillment_rate = fulfillment_rate
        self.save()


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = JSONField()
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"

    def clean(self):
        super().clean()

        if (self.delivery_date < self.acknowledgment_date) or (
                self.delivery_date < self.issue_date):
            raise ValidationError(
                "Delivery date must be >= the issue date and acknowledgement date.")

        if self.acknowledgment_date and self.issue_date:
            if self.acknowledgment_date < self.issue_date:
                raise ValidationError(
                    "Acknowledgment date must be equal to or after the issue date.")

        if self.quality_rating is not None and (
                self.quality_rating < 0 or self.quality_rating > 100):
            raise ValidationError("Quality rating must be between 0 and 100.")


class HistoricalPerformance(models.Model):
    # In our case, I would ideally run a CRON JOB once a day to update the
    # historical performance of each day
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
