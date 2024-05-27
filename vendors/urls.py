# vendors/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseOrderViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<int:pk>/performance/', VendorViewSet.as_view({'get': 'performance'}), name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledge/', PurchaseOrderViewSet.as_view({'post': 'acknowledge'}), name='purchase-order-acknowledge'),
]
