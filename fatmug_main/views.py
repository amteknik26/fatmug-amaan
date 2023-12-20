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
    """
    API endpoint for listing and creating vendors.

    - GET: Retrieve a list of all vendors.
    - POST: Create a new vendor.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Serializer:
    - VendorSerializer: Used for both serialization and deserialization of Vendor objects.

    Fields:
    - name (str): The name of the vendor.
    - contact_details (str): Contact details of the vendor, preferably an email address.
    - address (str): The address of the vendor.
    - vendor_code (str): A unique code assigned to the vendor.
    - on_time_delivery_rate (float, optional): Rate of on-time deliveries.
    - quality_rating_avg (float, optional): Average quality rating.
    - average_response_time (float, optional): Average response time in minutes.
    - fulfillment_rate (float, optional): Fulfillment rate.

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific vendor.

    - GET: Retrieve details of a specific vendor.
    - PUT/PATCH: Update details of a specific vendor.
    - DELETE: Delete a specific vendor.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Serializer:
    - VendorSerializer: Used for both serialization and deserialization of Vendor objects.

    Fields:
    - name (str): The name of the vendor.
    - contact_details (str): Contact details of the vendor, preferably an email address.
    - address (str): The address of the vendor.
    - vendor_code (str): A unique code assigned to the vendor.
    - on_time_delivery_rate (float, optional): Rate of on-time deliveries.
    - quality_rating_avg (float, optional): Average quality rating.
    - average_response_time (float, optional): Average response time in minutes.
    - fulfillment_rate (float, optional): Fulfillment rate.

    Note: The fields marked as optional may have a value of None or the default value if not specified.

    Raises:
    - NotFound: If the specified vendor does not exist.

    Note: Additional fields may be included based on your specific requirements.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorPerformanceView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving performance data of a specific vendor.

    - GET: Retrieve performance data of a specific vendor.

    Serializer:
    - VendorPerformanceSerializer: Used for serialization of performance data.

    Performance Data Fields:
    - vendor_name (str): The name of the vendor.
    - on_time_delivery_rate (float, optional): Rate of on-time deliveries.
    - quality_rating_avg (float, optional): Average quality rating.
    - average_response_time (float, optional): Average response time in minutes.
    - fulfillment_rate (float, optional): Fulfillment rate.

    Note: The fields marked as optional may have a value of None or the default value if not specified.

    Raises:
    - NotFound: If the specified vendor does not exist.

    Note: This endpoint does not support updating or deleting vendor performance data.

    """
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


class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating purchase orders.

    - GET: Retrieve a list of all purchase orders or filter by a specific vendor.
    - POST: Create a new purchase order.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Serializer:
    - PurchaseOrderSerializer: Used for both serialization and deserialization of PurchaseOrder objects.

    Fields:
    - po_number (str): The purchase order number (unique).
    - vendor (Vendor): The vendor associated with the purchase order.
    - order_date (datetime): The date of the purchase order.
    - delivery_date (datetime): The delivery date of the purchase order.
    - items (JSONField): A JSON field representing the items in the purchase order.
    - quantity (int): The quantity of items in the purchase order.
    - status (str): The status of the purchase order (pending, completed, canceled).
    - quality_rating (float, optional): The quality rating of the purchase order.
    - issue_date (datetime): The date of the purchase order issuance.
    - acknowledgment_date (datetime, optional): The date of acknowledgment.

    Filtering:
    - The purchase orders can be filtered based on the 'vendor_id' query parameter.
      For example, '/purchase-orders/?vendor_id=1' will retrieve purchase orders for the vendor with ID 1.

    Raises:
    - NotFound: If no purchase orders are found for the specified vendor.

    """
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
    """
    API endpoint for retrieving, updating, and deleting a specific purchase order.

    - GET: Retrieve details of a specific purchase order.
    - PUT/PATCH: Update details of a specific purchase order.
    - DELETE: Delete a specific purchase order.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Serializer:
    - PurchaseOrderSerializer: Used for both serialization and deserialization of PurchaseOrder objects.

    Fields:
    - po_number (str): The purchase order number (unique).
    - vendor (Vendor): The vendor associated with the purchase order.
    - order_date (datetime): The date of the purchase order.
    - delivery_date (datetime): The delivery date of the purchase order.
    - items (JSONField): A JSON field representing the items in the purchase order.
    - quantity (int): The quantity of items in the purchase order.
    - status (str): The status of the purchase order (pending, completed, canceled).
    - quality_rating (float, optional): The quality rating of the purchase order.
    - issue_date (datetime): The date of the purchase order issuance.
    - acknowledgment_date (datetime, optional): The date of acknowledgment.

    Updating:
    - Supports partial updates (PATCH) by setting 'partial' to True.

    Raises:
    - NotFound: If the specified purchase order does not exist.

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs) -> Response:
        """
        Update details of a specific purchase order.

        Parameters:
        - request (Request): The HTTP request.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: The updated purchase order details.

        Raises:
        - NotFound: If the specified purchase order does not exist.

        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class AcknowledgePurchaseOrderView(APIView):
    """
    API endpoint for acknowledging a specific purchase order.

    - POST: Acknowledge a specific purchase order by updating its acknowledgment date.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Serializer:
    - AcknowledgePurchaseOrderSerializer: Used for validation (no specific data requirements).

    Parameters:
    - pk (int): The primary key of the purchase order to be acknowledged.

    Returns:
    - Response: A success or error message indicating the result of the acknowledgment.

    Raises:
    - NotFound: If the specified purchase order does not exist.

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AcknowledgePurchaseOrderSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """
        Acknowledge a specific purchase order by updating its acknowledgment date.

        Parameters:
        - request (Request): The HTTP request.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: A success or error message indicating the result of the acknowledgment.

        Raises:
        - NotFound: If the specified purchase order does not exist.

        """
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
