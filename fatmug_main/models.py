from django.db import models
from django.db.models import JSONField
from django.utils import timezone
from .utils.metrics_calculator import calculate_on_time_delivery_rate, calculate_quality_rating_average,calculate_average_response_time,calculate_fulfillment_rate

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField(db_comment="Preferably an email address",)
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=None)
    quality_rating_avg = models.FloatField(default=None)
    average_response_time = models.FloatField(default=None)
    fulfillment_rate = models.FloatField(default=None)

    def update_on_time_delivery_rate(self,order_instance):
        on_time_delivery_rate = calculate_on_time_delivery_rate(self,order_instance)
        self.on_time_delivery_rate = on_time_delivery_rate
        self.save()

    def update_quality_rating_avg(self,order_quality_rating):
        # Calculate the average of quality ratings for completed POs
        quality_rating_avg = calculate_quality_rating_average(self,order_quality_rating)
        self.quality_rating_avg = quality_rating_avg
        self.save()
    
    def update_average_response_time(self,order_instance):
        # Calculate the average response time for acknowledged POs
        acknowledged_pos = calculate_average_response_time(self,order_instance)
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"
    

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"

