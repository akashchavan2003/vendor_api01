from django.db import models
from django.core.exceptions import ValidationError

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    on_time_delivery_rate = models.FloatField(default=0, null=True, blank=True)
    quality_rating = models.FloatField(default=0, null=True, blank=True)
    response_time = models.DurationField(null=True, blank=True)
    fulfilment_rate = models.FloatField(default=0, null=True, blank=True)

    def update_performance_metrics(self):
        # Implement logic to calculate and update performance metrics
        # This method can be called whenever a relevant event occurs (e.g., new purchase order)
        pass


def validate_items(value):
    if not value:
        raise ValidationError(('Items field must be provided.'))

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField(validators=[validate_items], null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number



class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.vendor} - {self.date}"

