# from django.utils.timezone import now
# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import Vendor, PurchaseOrder
# from .serializers import VendorSerializer, PurchaseOrderSerializer

# class VendorViewSet(viewsets.ModelViewSet):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer

#     @action(detail=True, methods=['get'])
#     def performance(self, request, pk=None):
#         vendor = self.get_object()
#         performance_data = {
#             'on_time_delivery_rate': vendor.on_time_delivery_rate,
#             'quality_rating_avg': vendor.quality_rating_avg,
#             'average_response_time': vendor.average_response_time,
#             'fulfillment_rate': vendor.fulfillment_rate
#         }
#         return Response(performance_data)

# class PurchaseOrderViewSet(viewsets.ModelViewSet):
#     queryset = PurchaseOrder.objects.all()
#     serializer_class = PurchaseOrderSerializer

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         vendor_id = self.request.query_params.get('vendor_id')
#         if vendor_id is not None:
#             queryset = queryset.filter(vendor_id=vendor_id)
#         return queryset

#     @action(detail=True, methods=['post'])
#     def acknowledge(self, request, pk=None):
#         purchase_order = self.get_object()
#         purchase_order.acknowledgment_date = now()
#         purchase_order.save()
#         return Response({'status': 'acknowledged'})




from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """
        Retrieve the performance metrics for a specific vendor.
        """
        vendor = self.get_object()
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate
        }
        return Response(performance_data)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchase orders,
        by filtering against a `vendor_id` query parameter in the URL.
        """
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id is not None:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """
        Acknowledge a purchase order by setting the acknowledgment date to now.
        """
        purchase_order = self.get_object()
        if purchase_order.acknowledgment_date is not None:
            return Response({'status': 'already acknowledged'}, status=status.HTTP_400_BAD_REQUEST)
        
        purchase_order.acknowledgment_date = now()
        purchase_order.save()
        purchase_order.vendor.update_average_response_time()  # Update the response time metric
        return Response({'status': 'acknowledged'}, status=status.HTTP_200_OK)
