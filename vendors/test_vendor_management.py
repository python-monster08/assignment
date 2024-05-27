# from django.test import TestCase
# from django.utils.timezone import now, timedelta
# from rest_framework.test import APITestCase, APIClient
# from django.urls import reverse
# from .models import Vendor, PurchaseOrder
# from .serializers import VendorSerializer, PurchaseOrderSerializer

# class VendorModelTests(TestCase):
    
#     def setUp(self):
#         self.vendor = Vendor.objects.create(
#             name="Test Vendor",
#             contact_details="123 Test St",
#             address="123 Test City",
#             vendor_code="TV123"
#         )
#         self.purchase_order1 = PurchaseOrder.objects.create(
#             po_number="PO001",
#             vendor=self.vendor,
#             order_date=now() - timedelta(days=10),
#             delivery_date=now() - timedelta(days=5),
#             items={"item": "Test Item"},
#             quantity=10,
#             status='completed',
#             quality_rating=4.5
#         )
#         self.purchase_order2 = PurchaseOrder.objects.create(
#             po_number="PO002",
#             vendor=self.vendor,
#             order_date=now() - timedelta(days=8),
#             delivery_date=now() - timedelta(days=3),
#             items={"item": "Test Item"},
#             quantity=5,
#             status='completed',
#             quality_rating=4.0
#         )
    
#     def test_on_time_delivery_rate(self):
#         self.purchase_order1.delivery_date = self.purchase_order1.order_date + timedelta(days=5)
#         self.purchase_order1.save()
#         self.purchase_order2.delivery_date = self.purchase_order2.order_date + timedelta(days=5)
#         self.purchase_order2.save()
#         self.vendor.update_on_time_delivery_rate()
#         self.assertEqual(self.vendor.on_time_delivery_rate, 100.0)

#     def test_quality_rating_avg(self):
#         self.vendor.update_quality_rating_avg()
#         self.assertEqual(self.vendor.quality_rating_avg, 4.25)
    
#     def test_average_response_time(self):
#         self.purchase_order1.acknowledgment_date = self.purchase_order1.order_date + timedelta(days=1)
#         self.purchase_order1.save()
#         self.purchase_order2.acknowledgment_date = self.purchase_order2.order_date + timedelta(days=2)
#         self.purchase_order2.save()
#         self.vendor.update_average_response_time()
#         expected_avg_response_time = ((self.purchase_order1.acknowledgment_date - self.purchase_order1.issue_date).total_seconds() +
#                                       (self.purchase_order2.acknowledgment_date - self.purchase_order2.issue_date).total_seconds()) / 2
#         self.assertAlmostEqual(self.vendor.average_response_time, expected_avg_response_time, places=7)

#     def test_fulfillment_rate(self):
#         self.vendor.update_fulfillment_rate()
#         self.assertEqual(self.vendor.fulfillment_rate, 100.0)

# class VendorSerializerTests(APITestCase):

#     def setUp(self):
#         self.vendor_data = {
#             "name": "Test Vendor",
#             "contact_details": "123 Test St",
#             "address": "123 Test City",
#             "vendor_code": "TV123"
#         }
#         self.vendor = Vendor.objects.create(**self.vendor_data)

#     def test_vendor_serializer(self):
#         serializer = VendorSerializer(self.vendor)
#         data = serializer.data
#         self.assertEqual(data['name'], self.vendor_data['name'])
#         self.assertEqual(data['contact_details'], self.vendor_data['contact_details'])
#         self.assertEqual(data['address'], self.vendor_data['address'])
#         self.assertEqual(data['vendor_code'], self.vendor_data['vendor_code'])

# class PurchaseOrderSerializerTests(APITestCase):

#     def setUp(self):
#         self.vendor = Vendor.objects.create(
#             name="Test Vendor",
#             contact_details="123 Test St",
#             address="123 Test City",
#             vendor_code="TV123"
#         )
#         self.po_data = {
#             "po_number": "PO001",
#             "vendor": self.vendor.id,
#             "order_date": now(),
#             "delivery_date": now() + timedelta(days=5),
#             "items": {"item": "Test Item"},
#             "quantity": 10,
#             "status": "pending"
#         }

#     def test_purchase_order_serializer(self):
#         serializer = PurchaseOrderSerializer(data=self.po_data)
#         self.assertTrue(serializer.is_valid())
#         po = serializer.save()
#         self.assertEqual(po.po_number, self.po_data['po_number'])
#         self.assertEqual(po.vendor, self.vendor)

# class VendorViewSetTests(APITestCase):

#     def setUp(self):
#         self.client = APIClient()

#         self.vendor = Vendor.objects.create(
#             name="Test Vendor",
#             contact_details="123 Test St",
#             address="123 Test City",
#             vendor_code="TV123"
#         )

#     def test_get_vendor_performance(self):
#         url = reverse('vendor-performance', args=[self.vendor.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('on_time_delivery_rate', response.data)
#         self.assertIn('quality_rating_avg', response.data)
#         self.assertIn('average_response_time', response.data)
#         self.assertIn('fulfillment_rate', response.data)

# class PurchaseOrderViewSetTests(APITestCase):

#     def setUp(self):
#         self.client = APIClient()

#         self.vendor = Vendor.objects.create(
#             name="Test Vendor",
#             contact_details="123 Test St",
#             address="123 Test City",
#             vendor_code="TV123"
#         )
#         self.purchase_order = PurchaseOrder.objects.create(
#             po_number="PO001",
#             vendor=self.vendor,
#             order_date=now(),
#             delivery_date=now() + timedelta(days=5),
#             items={"item": "Test Item"},
#             quantity=10,
#             status="pending"
#         )

#     def test_acknowledge_purchase_order(self):
#         url = reverse('purchase-order-acknowledge', args=[self.purchase_order.id])
#         response = self.client.post(url)
#         self.assertEqual(response.status_code, 200)
#         self.purchase_order.refresh_from_db()
#         self.assertIsNotNone(self.purchase_order.acknowledgment_date)
#         self.assertEqual(response.data['status'], 'acknowledged')
