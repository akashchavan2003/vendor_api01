from django.test import TestCase
from django.utils import timezone
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .views import change_po_status_to_completed

class VendorPerformanceTests(TestCase):
    def setUp(self):
        # Create vendor objects
        self.vendor1 = Vendor.objects.create(name='Vendor 1', on_time_delivery_rate=0.5, quality_rating=4.2, fulfilment_rate=0.8)

        # Create purchase orders for testing
        self.po1_vendor1 = PurchaseOrder.objects.create(
            vendor=self.vendor1,
            po_number='PO001',
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items=['Item1', 'Item2'],
            quantity=10,
            status='completed',
            quality_rating=4.5,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now()
        )
        self.po2_vendor1 = PurchaseOrder.objects.create(
            vendor=self.vendor1,
            po_number='PO002',
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items=['Item3', 'Item4'],
            quantity=20,
            status='completed',
            quality_rating=4.8,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now() + timezone.timedelta(days=1)
        )

        # Create HistoricalPerformance data for vendor 1
        HistoricalPerformance.objects.create(
            vendor=self.vendor1,
            date=timezone.now(),
            on_time_delivery_rate=0.7,
            quality_rating_avg=4.3,
            average_response_time=2.5,
            fulfillment_rate=0.9
        )

    def test_update_on_time_delivery_rate(self):
    # Create a purchase order with status 'pending'
        po = PurchaseOrder.objects.create(
            vendor=self.vendor1,  # Use self.vendor1 instead of self.vendor
            po_number='PO003',  # Provide a unique PO number
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items=['Item5', 'Item6'],
            quantity=30,
            status='pending',  # Set status to 'pending'
            quality_rating=4.0,  # Set quality rating as needed
            issue_date=timezone.now(),
            acknowledgment_date=None
        )

        # Initially, the vendor's on-time delivery rate should be 0
        self.assertEqual(self.vendor1.on_time_delivery_rate, 0)

        # Change the status of the purchase order to 'completed'
        response = change_po_status_to_completed(None, po.id)

        # Verify that the response indicates success
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'PO status changed to completed and vendor metrics updated')

        # Refresh the vendor instance from the database
        self.vendor1.refresh_from_db()

        # Assert that the on-time delivery rate has been updated
        self.assertAlmostEqual(self.vendor1.on_time_delivery_rate, 0.66, places=2)  # Update this value based on your expected calculation
