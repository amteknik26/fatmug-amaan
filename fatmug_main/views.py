# fatmug_main/views.py
from datetime import timezone

from django.utils import timezone
from rest_framework import filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HistoricalPerformance, PurchaseOrder, Vendor
from .serializers import (AcknowledgePurchaseOrderSerializer,
                          HistoricalPerformanceSerializer,
                          PurchaseOrderSerializer, VendorPerformanceSerializer,
                          VendorSerializer)


class VendorListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderSerializer
    filter_backends = [filters.SearchFilter]
    # Doube underscore here 'vendor__id'
    # it indicates that you want to filter or search based on the id field of
    # the related vendor model.
    search_fields = ['vendor__id']

    def get_queryset(self) -> PurchaseOrder:
        queryset = PurchaseOrder.objects.all()
        vendor_id = self.request.query_params.get('vendor_id', None)
        if vendor_id:
            queryset = queryset.filter(vendor__id=vendor_id)
        if not queryset.exists():
            raise NotFound(
                "No purchase orders found for the specified vendor.")
        return queryset


class PurchaseOrderRetrieveUpdateDeleteView(
        generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs) -> Response:
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class VendorPerformanceView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer


class VendorPerformanceView(generics.RetrieveAPIView):
    serializer_class = VendorPerformanceSerializer
    queryset = Vendor.objects.all()

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()

        performance_data = {
            'vendor_name': instance.name,
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating_avg': instance.quality_rating_avg,
            'average_response_time': instance.average_response_time,
            'fulfillment_rate': instance.fulfillment_rate
        }

        serializer = self.get_serializer(performance_data)
        return Response(serializer.data)


class AcknowledgePurchaseOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AcknowledgePurchaseOrderSerializer

    def post(self, request, *args, **kwargs) -> Response:
        po_id = kwargs.get('pk')

        try:
            instance = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response(
                {'detail': f'Purchase Order {po_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        instance.acknowledgment_date = timezone.now()
        instance.save()
        return Response(
            {'detail': f'Purchase Order {po_id} acknowledged successfully.'}, status=status.HTTP_200_OK)
