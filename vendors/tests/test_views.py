from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from ..models import Vendor, PurchaseOrder
from django.utils import timezone

class VendorViewSetTest(APITestCase):
    def setUp(self):
        # Create a sample vendor
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Some contact details",
            address="Some address",
            vendor_code="V1234"
        )
        self.client = APIClient()

    def test_create_vendor(self):
        # Test creating a vendor
        url = reverse('vendor-list')
        data = {
            'name': 'New Vendor',
            'contact_details': 'New contact details',
            'address': 'New address',
            'vendor_code': 'NV1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)  # Including the one from setUp

    def test_retrieve_vendor(self):
        # Test retrieving a vendor
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vendor_code'], 'V1234')

    def test_update_vendor(self):
        # Test updating a vendor
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        data = {
            'name': 'Updated Vendor',
            'contact_details': 'Updated contact details',
            'address': 'Updated address',
            'vendor_code': 'V1234'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, 'Updated Vendor')

    def test_delete_vendor(self):
        # Test deleting a vendor
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

class PurchaseOrderViewSetTest(APITestCase):
    def setUp(self):
        # Create a vendor and a purchase order
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Some contact details",
            address="Some address",
            vendor_code="V1234"
        )
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO1001",
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=2),
            items={'item1': 10, 'item2': 5},
            quantity=15,
            status='pending'
        )
        self.client = APIClient()

    def test_create_purchase_order(self):
        # Test creating a purchase order
        url = reverse('purchaseorder-list')
        data = {
            'vendor': self.vendor.id,
            'po_number': 'PO1002',
            'order_date': '2021-01-01T00:00:00Z',
            'delivery_date': '2021-01-05T00:00:00Z',
            'items': {'item3': 3, 'item4': 7},
            'quantity': 10,
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_retrieve_purchase_order(self):
        # Test retrieving a purchase order
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'PO1001')

    def test_update_purchase_order(self):
        # Test updating a purchase order
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk})
        data = {
            'status': 'completed'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.status, 'completed')

    def test_delete_purchase_order(self):
        # Test deleting a purchase order
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)
