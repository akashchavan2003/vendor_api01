from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder,HistoricalPerformance
from django.db import transaction

from django.db.models import Avg, F, Count,Sum

@receiver(post_save, sender=PurchaseOrder)
def update_metrics_on_po_completion(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        print("instance changed....")
        vendor = instance.vendor

        # Get all completed purchase orders for the vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

        # Count the number of completed POs delivered on or before delivery_date
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=instance.delivery_date).count()

        # Calculate the On-Time Delivery Rate
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            on_time_delivery_rate = on_time_delivered_pos / total_completed_pos
        else:
            on_time_delivery_rate = 0

        # Calculate average quality rating
        avg_quality_rating = completed_pos.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']

        # Calculate average response time
        avg_response_time = completed_pos.aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time']

        # Calculate fulfillment rate
        total_quantity_ordered = completed_pos.aggregate(total_quantity_ordered=Sum('quantity'))['total_quantity_ordered']
        total_quantity_delivered = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).aggregate(total_quantity_delivered=Sum('quantity'))['total_quantity_delivered']
        fulfillment_rate = total_quantity_delivered / total_quantity_ordered if total_quantity_ordered else 0

        # Update metrics for the vendor
        with transaction.atomic():
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.quality_rating = avg_quality_rating
            vendor.response_time = avg_response_time
            vendor.fulfillment_rate = fulfillment_rate
            vendor.save()

            # Update HistoricalPerformance
            historical_entry, created = HistoricalPerformance.objects.get_or_create(vendor=vendor, date=instance.delivery_date.date())
            historical_entry.on_time_delivery_rate = on_time_delivery_rate
            historical_entry.quality_rating_avg = avg_quality_rating
            historical_entry.average_response_time = avg_response_time
            historical_entry.fulfillment_rate = fulfillment_rate
            historical_entry.vendor=PurchaseOrder.vendor
            historical_entry.save()
  