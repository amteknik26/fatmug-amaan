from rest_framework import serializers

from .models import HistoricalPerformance, PurchaseOrder, Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class VendorPerformanceSerializer(serializers.Serializer):
    vendor_name = serializers.CharField()
    on_time_delivery_rate = serializers.FloatField(allow_null=True)
    quality_rating_avg = serializers.FloatField(allow_null=True)
    average_response_time = serializers.FloatField(allow_null=True)
    fulfillment_rate = serializers.FloatField(allow_null=True)


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'


class AcknowledgePurchaseOrderSerializer(serializers.Serializer):
    def validate(self, data):
        # If no data is provided, consider it as an acknowledgment
        return data
