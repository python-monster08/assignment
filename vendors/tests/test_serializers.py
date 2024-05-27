from rest_framework.test import APITestCase
from django.utils.timezone import now, timedelta
from vendors.models import Vendor, PurchaseOrder
from vendors.serializers import VendorSerializer, PurchaseOrderSerializer

class VendorSerializerTests(APITestCase):

    def setUp(self):
        self.vendor_data = {
            "name": "Test Vendor",
            "contact_details": "123 Test St",
            "address": "123 Test City",
            "vendor_code": "TV123"
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_vendor_serializer(self):
        serializer = VendorSerializer(self.vendor)
        data = serializer.data
        self.assertEqual(data['name'], self.vendor_data['name'])
        self.assertEqual(data['contact_details'], self.vendor_data['contact_details'])
        self.assertEqual(data['address'], self.vendor_data['address'])
        self.assertEqual(data['vendor_code'], self.vendor_data['vendor_code'])

class PurchaseOrderSerializerTests(APITestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test St",
            address="123 Test City",
            vendor_code="TV123"
        )
        self.po_data = {
            "po_number": "PO001",
            "vendor": self.vendor.id,
            "order_date": now(),
            "delivery_date": now() + timedelta(days=5),
            "items": {"item": "Test Item"},
            "quantity": 10,
            "status": "pending"
        }

    def test_purchase_order_serializer(self):
        serializer = PurchaseOrderSerializer(data=self.po_data)
        self.assertTrue(serializer.is_valid())
        po = serializer.save()
        self.assertEqual(po.po_number, self.po_data['po_number'])
        self.assertEqual(po.vendor, self.vendor)
