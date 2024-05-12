# yourapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import VendorListCreateAPIView,RetrieveVendorAPIView,UpdateVendorAPIView,DeleteVendorAPIView,purchase_order,purchase_order_detail,vendor_performance_metrics,PurchaseOrderUpdateAPIView



urlpatterns = [
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', RetrieveVendorAPIView.as_view(), name='retrieve_vendor'),
    path('vendors/<int:pk>/update/', UpdateVendorAPIView.as_view(), name='update_vendor'),
    path('vendors/<int:pk>/delete/', DeleteVendorAPIView.as_view(), name='delete_vendor'),
    
    # Define URLs for purchase order-related views
    path('purchase_orders/', purchase_order, name='purchase_orders'),
    path('purchase_orders/<int:po_id>/', purchase_order_detail, name='purchase_order_detail'),

    path('api/vendors/<int:vendor_id>/performance/',vendor_performance_metrics, name='vendor_performance'),
    path('api/purchase_orders/<int:pk>/update/', PurchaseOrderUpdateAPIView.as_view(), name='purchase_order_update')
]




# Optionally, you can define additional URL patterns for token-based authentication if needed.