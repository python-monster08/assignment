from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.db.models import F
from vendors.models import Vendor, PurchaseOrder

class VendorModelTests(TestCase):
    
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test St",
            address="123 Test City",
            vendor_code="TV123"
        )
        self.purchase_order1 = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=now() - timedelta(days=10),
            delivery_date=now() - timedelta(days=5),
            items={"item": "Test Item"},
            quantity=10,
            status='completed',
            quality_rating=4.5
        )
        self.purchase_order2 = PurchaseOrder.objects.create(
            po_number="PO002",
            vendor=self.vendor,
            order_date=now() - timedelta(days=8),
            delivery_date=now() - timedelta(days=3),
            items={"item": "Test Item"},
            quantity=5,
            status='completed',
            quality_rating=4.0
        )
    
    def test_on_time_delivery_rate(self):
        self.purchase_order1.delivery_date = self.purchase_order1.order_date + timedelta(days=5)
        self.purchase_order1.save()
        self.purchase_order2.delivery_date = self.purchase_order2.order_date + timedelta(days=5)
        self.purchase_order2.save()
        self.vendor.update_on_time_delivery_rate()
        self.assertEqual(self.vendor.on_time_delivery_rate, 100.0)

    def test_quality_rating_avg(self):
        self.vendor.update_quality_rating_avg()
        self.assertEqual(self.vendor.quality_rating_avg, 4.25)
    
    def test_average_response_time(self):
        self.purchase_order1.acknowledgment_date = self.purchase_order1.order_date + timedelta(days=1)
        self.purchase_order1.save()
        self.purchase_order2.acknowledgment_date = self.purchase_order2.order_date + timedelta(days=2)
        self.purchase_order2.save()
        self.vendor.update_average_response_time()
        expected_avg_response_time = ((self.purchase_order1.acknowledgment_date - self.purchase_order1.issue_date).total_seconds() +
                                      (self.purchase_order2.acknowledgment_date - self.purchase_order2.issue_date).total_seconds()) / 2
        self.assertAlmostEqual(self.vendor.average_response_time, expected_avg_response_time, places=7)

    def test_fulfillment_rate(self):
        self.vendor.update_fulfillment_rate()
        self.assertEqual(self.vendor.fulfillment_rate, 100.0)
