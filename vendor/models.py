from django.db import models
from django.core.validators import RegexValidator


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    phone_number_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    contact_details = models.CharField(max_length=255,validators=[phone_number_validator],unique=True)
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=20)
    order_date = models.DateField()
    items = models.TextField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    delivery_date = models.DateTimeField(null=True, blank=True)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.po_number} - {self.vendor.name}"
    
    def calculate_quality_rating_avg(self):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, status='completed', quality_rating__isnull=False
        )
        total_ratings = sum(order.quality_rating for order in completed_orders)
        total_orders = completed_orders.count()
        return total_ratings / total_orders if total_orders else 0.0

    def calculate_average_response_time(self):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, status='completed', acknowledgment_date__isnull=False
        )
        total_time = sum((order.acknowledgment_date - order.issue_date).total_seconds() for order in completed_orders)
        total_orders = completed_orders.count()
        return total_time / total_orders if total_orders else 0.0

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
    