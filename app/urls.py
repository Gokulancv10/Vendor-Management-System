from django.urls import path

from .views import (
    AcknowledgePurchaseOrderView,
    PurchaseOrderDetailView,
    PurchaseOrdersView,
    RetrieveVendorView,
    VendorPerformanceView,
    VendorsView,
)

urlpatterns = [
    path("vendors/", VendorsView.as_view(), name="vendors"),
    path(
        "vendors/<int:vendor_id>/", RetrieveVendorView.as_view(), name="vendor-details"
    ),
    path(
        "purchase_orders/",
        PurchaseOrdersView.as_view(),
        name="create-get-purchase-orders",
    ),
    path(
        "purchase_orders/<int:id>/",
        PurchaseOrderDetailView.as_view(),
        name="purchase_orders_detail",
    ),
    path(
        "purchase_orders/<int:id>/acknowledge/",
        AcknowledgePurchaseOrderView.as_view(),
        name="vendor_acknowledge_purchase_order",
    ),
    path(
        "vendors/<int:id>/performance/",
        VendorPerformanceView.as_view(),
        name="vendor_performance",
    ),
]
