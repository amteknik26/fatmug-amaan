from django.contrib import admin

from .models import HistoricalPerformance, PurchaseOrder, Vendor

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)
