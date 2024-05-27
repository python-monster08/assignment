from django.test import TestCase
from ..models import Vendor, PurchaseOrder
from ..serializers import VendorSerializer, PurchaseOrderSerializer
from django.utils import timezone

class VendorSerializerTest(TestCase):
    def setUp(self):
        # Create a sample vendor to use in tests
        self.vendor_attributes = {
            'name': 'Test Vendor',
            'contact_details': 'Some contact details',
            'address': 'Some address',
            'vendor_code': 'V1234',
            'on_time_delivery_rate': 95.5,
            'quality_rating_avg': 4.2,
            'average_response_time': 24,
            'fulfillment_rate': 99.9
        }

        self.vendor = Vendor.objects.create(**self.vendor_attributes)
        self.serializer = VendorSerializer(instance=self.vendor)

    def test_contains_expected_fields(self):
        # Test that serializer has the correct fields
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']))

    def test_field_content(self):
        # Test the content of the serializer fields
        data = self.serializer.data
        for key in self.vendor_attributes:
            self.assertEqual(data[key], self.vendor_attributes[key])

class PurchaseOrderSerializerTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Details', address='Some address', vendor_code='V12345')
        self.purchase_order_attributes = {
            'po_number': 'PO10001',
            'vendor': self.vendor,
            'order_date': timezone.now(),
            'delivery_date': timezone.now() + timezone.timedelta(days=1),
            'items': {'item1': 10, 'item2': 5},
            'quantity': 15,
            'status': 'completed',
            'quality_rating': 4.5
        }

        self.purchase_order = PurchaseOrder.objects.create(**self.purchase_order_attributes)
        self.serializer = PurchaseOrderSerializer(instance=self.purchase_order)

    def test_contains_expected_fields(self):
        # Test that serializer includes the correct fields
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']))

    def test_field_content(self):
        # Test the content of the serializer fields
        data = self.serializer.data
        self.assertEqual(data['po_number'], self.purchase_order_attributes['po_number'])
        self.assertEqual(data['vendor'], self.purchase_order.vendor.id)
        self.assertEqual(data['quantity'], self.purchase_order_attributes['quantity'])
        self.assertEqual(data['status'], self.purchase_order_attributes['status'])

    def test_invalid_data(self):
        # Ensure that serializer rejects invalid data
        invalid_data = {**self.purchase_order_attributes, 'quantity': -10}  # Invalid quantity
        serializer = PurchaseOrderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

