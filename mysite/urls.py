

# mysite/urls.py
from django.contrib import admin
from django.urls import path, include

from api.views import VendorListCreateAPIView,UpdateVendorAPIView,DeleteVendorAPIView,RetrieveVendorAPIView,PurchaseOrder,purchase_order_detail,purchase_order,vendor_performance_metrics,PurchaseOrderUpdateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),  # Include the app-specific URLs
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', RetrieveVendorAPIView.as_view(), name='retrieve_vendor'),
    path('api/vendors/<int:pk>/update/', UpdateVendorAPIView.as_view(), name='update_vendor'),
    path('api/vendors/<int:pk>/delete/', DeleteVendorAPIView.as_view(), name='delete_vendor'),
    path('api/purchase_orders/', purchase_order, name='purchase_orders'),
    path('api/purchase_orders/<int:po_id>/', purchase_order_detail, name='purchase_order_detail'),
    path('api/vendors/<int:vendor_id>/performance/',vendor_performance_metrics, name='vendor_performance'),
    path('api/purchase_orders/<int:pk>/update/', PurchaseOrderUpdateAPIView.as_view(), name='purchase_order_update')
]


