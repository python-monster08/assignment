from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.utils.timezone import now, timedelta
from vendors.models import Vendor, PurchaseOrder

class VendorViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test St",
            address="123 Test City",
            vendor_code="TV123"
        )

    def test_get_vendor_performance(self):
        url = reverse('vendor-performance', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertIn('quality_rating_avg', response.data)
        self.assertIn('average_response_time', response.data)
        self.assertIn('fulfillment_rate', response.data)

class PurchaseOrderViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test St",
            address="123 Test City",
            vendor_code="TV123"
        )
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=now(),
            delivery_date=now() + timedelta(days=5),
            items={"item": "Test Item"},
            quantity=10,
            status="pending"
        )

    def test_acknowledge_purchase_order(self):
        url = reverse('purchase-order-acknowledge', args=[self.purchase_order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)
        self.assertEqual(response.data['status'], 'acknowledged')
