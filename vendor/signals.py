from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver([post_save, post_delete], sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    vendor.quality_rating_avg = vendor.calculate_quality_rating_avg()
    vendor.fulfillment_rate = vendor.calculate_fulfillment_rate()
    vendor.save()