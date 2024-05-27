from django.test import TestCase
from django.utils import timezone
from ..models import Vendor, PurchaseOrder

class VendorModelTest(TestCase):
    def setUp(self):
        # Create a sample vendor to use in tests
        self.vendor = Vendor.objects.create(
            name="Sample Vendor",
            contact_details="1234 Test St, Testing",
            address="1234 Test Ave, Testtown, TE",
            vendor_code="VND123"
        )

    def test_create_vendor(self):
        # Test the vendor was created correctly
        vendor = Vendor.objects.get(name="Sample Vendor")
        self.assertEqual(vendor.name, "Sample Vendor")
        self.assertEqual(vendor.vendor_code, "VND123")

    def test_update_on_time_delivery_rate(self):
        # Test on_time_delivery_rate calculations
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO1001",
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=1),
            status='completed'
        )
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO1002",
            order_date=timezone.now(),
            delivery_date=timezone.now() - timezone.timedelta(days=1),  # Delivered late
            status='completed'
        )
        self.vendor.update_on_time_delivery_rate()
        self.assertEqual(self.vendor.on_time_delivery_rate, 50.0)  # 1 on time, 1 late

    def test_update_quality_rating_avg(self):
        # Test quality_rating_avg calculations
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO1003",
            quality_rating=5.0,
            status='completed'
        )
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO1004",
            quality_rating=3.0,
            status='completed'
        )
        self.vendor.update_quality_rating_avg()
        self.assertAlmostEqual(self.vendor.quality_rating_avg, 4.0)  # Average of 5 and 3

class PurchaseOrderModelTest(TestCase):
    def setUp(self):
        # Create a vendor and purchase order for testing
        self.vendor = Vendor.objects.create(
            name="Sample Vendor",
            contact_details="1234 Test St, Testing",
            address="1234 Test Ave, Testtown, TE",
            vendor_code="VND123"
        )
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO1005",
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=2),
            items={'item1': 10},
            quantity=10,
            status='pending'
        )

    def test_purchase_order_creation(self):
        # Test the purchase order was created correctly
        po = PurchaseOrder.objects.get(po_number="PO1005")
        self.assertEqual(po.vendor, self.vendor)
        self.assertEqual(po.status, 'pending')

    def test_update_status_to_completed(self):
        # Test updating the status to 'completed' and check performance metrics update
        self.purchase_order.status = 'completed'
        self.purchase_order.quality_rating = 4.0
        self.purchase_order.save()
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.on_time_delivery_rate, 100.0)  # Assuming this is the first and only completed order

