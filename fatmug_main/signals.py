import logging

from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_quality_rating_avg(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        with transaction.atomic():
            instance.vendor.update_quality_rating_avg(instance.quality_rating)


@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, **kwargs):
    if instance.acknowledgment_date is not None:
        with transaction.atomic():
            instance.vendor.update_average_response_time(instance)


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_fulfillment_rate(sender, instance, **kwargs):
    if instance.status in ('completed', 'pending', 'cancelled'):
        with transaction.atomic():
            instance.vendor.update_fulfillment_rate()


@receiver(pre_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.acknowledgment_date is not None:
        try:
            # Get the old instance from the database
            original_instance = PurchaseOrder.objects.get(pk=instance.pk)
        except Exception as e:
            logging.info(
                "Exception when fetching original instance to update delivery rate")

        if original_instance.status in ('cancelled', 'pending'):
            instance.vendor.update_on_time_delivery_rate(instance)
