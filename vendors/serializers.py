# from rest_framework import serializers
# from .models import Vendor, PurchaseOrder

# class VendorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vendor
#         fields = '__all__'

# class PurchaseOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PurchaseOrder
#         fields = '__all__'



from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    purchase_orders = PurchaseOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')

    def validate_vendor_code(self, value):
        if ' ' in value:
            raise serializers.ValidationError("Vendor code should not contain spaces.")
        return value

