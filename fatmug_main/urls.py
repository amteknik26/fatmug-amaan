"""
URL configuration for fatmug_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import (AcknowledgePurchaseOrderView, PurchaseOrderListCreateView,
                    PurchaseOrderRetrieveUpdateDeleteView,
                    VendorListCreateView, VendorPerformanceView,
                    VendorRetrieveUpdateDeleteView)

urlpatterns = [
    path(
        'api/vendors/',
        VendorListCreateView.as_view(),
        name='vendor-list-create'),
    path(
        'api/vendors/<int:pk>/',
        VendorRetrieveUpdateDeleteView.as_view(),
        name='vendor-retrieve-update-delete'),
    path(
        'api/purchase_orders/',
        PurchaseOrderListCreateView.as_view(),
        name='purchase-order-list-create'),
    path(
        'api/purchase_orders/<int:pk>/',
        PurchaseOrderRetrieveUpdateDeleteView.as_view(),
        name='purchase-order-retrieve-update-delete'),
    path(
        'api/vendors/<int:pk>/performance/',
        VendorPerformanceView.as_view(),
        name='vendor_performance'),
    path(
        'api/purchase_orders/<int:pk>/acknowledge/',
        AcknowledgePurchaseOrderView.as_view(),
        name='acknowledge-purchase-order'),
]
