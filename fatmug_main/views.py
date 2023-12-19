# fatmug_main/views.py
from datetime import timezone
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.utils import timezone
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import AcknowledgePurchaseOrderSerializer, VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = PurchaseOrderSerializer
    filter_backends = [filters.SearchFilter]
    #Doube underscore here 'vendor__id'
    # it indicates that you want to filter or search based on the id field of the related vendor model.
    search_fields = ['vendor__id']

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        vendor_id = self.request.query_params.get('vendor_id', None)
        if vendor_id:
            queryset = queryset.filter(vendor__id=vendor_id)
        if not queryset.exists():
            raise NotFound("No purchase orders found for the specified vendor.")
        return queryset

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    serializer_class = AcknowledgePurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
            # Extract po_id from URL parameters
            po_id = kwargs.get('pk')
            
            # Get the PurchaseOrder instance
            try:
                instance = PurchaseOrder.objects.get(pk=po_id)
            except PurchaseOrder.DoesNotExist:
                return Response({'detail': 'Purchase Order not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Create an instance of the serializer
            serializer = AcknowledgePurchaseOrderSerializer(instance)

            # Validate the serializer
            serializer.is_valid(raise_exception=True)

            # Update acknowledgment_date and trigger recalculation
            instance.acknowledgment_date = timezone.now()
            instance.save()
            instance.vendor.update_average_response_time()

            return Response({'detail': 'Purchase Order acknowledged successfully.'})

