from rest_framework import serializers
from .dummy_products import DUMMY_PRODUCT_IDS
from .dummy_locations import DUMMY_LOCATIONS
from .dumy_warehouse import DUMMY_WAREHOUSES
from .models import InventoryTransaction,StockBalance


class StockBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockBalance

        fields = [
            'stock_balance_id',
            'product_id',
            'warehouse_id',
            'location_id',
            'total_quantity',
            'reserved_quantity',
            'available_quantity',
            'updated_at',
        ]

        read_only_fields = [
            'stock_balance_id',
            'updated_at',
        ]

class InventoryTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryTransaction

        fields = [
            'transaction_id',
            'product_id',
            'transaction_type',
            'adjustment_type',
            'adjustment_reason',
            'quantity',
            'reference_type',
            'reference_id',
            'created_at',
        ]

        read_only_fields = [
            'transaction_id',
            'created_at',
        ]
class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = StockBalance
        fields = [
            'product_id',
            'available_quantity',
        ]
        

class InventoryInSerializer(serializers.Serializer):
    grn_id = serializers.CharField(max_length=100)
    product_id = serializers.IntegerField()
    warehouse_id = serializers.IntegerField()
    location_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )

        return value

    def validate_product_id(self, value):

        if value not in DUMMY_PRODUCT_IDS:
            raise serializers.ValidationError(
            "Invalid product. Product does not exist."
        )

        return value


def validate_warehouse_id(self, value):

    try:
        warehouse = DUMMY_WAREHOUSES.objects.get(warehouse_id=value)
    except DUMMY_WAREHOUSES.DoesNotExist:
        raise serializers.ValidationError("Warehouse does noe exist")

    if not warehouse.is_active:
        raise serializers.ValidationError(
            "Warehouse is inactive."
        )

    return value

def validate_location_id(self, value):
    try:
        location = DUMMY_LOCATIONS.objects.get(
            location_id=value
        )
    except DUMMY_LOCATIONS.DoesNotExist:
        raise serializers.ValidationError(
            "Location does not exist."
        )

    if not location.is_active:
        raise serializers.ValidationError(
            "Location is inactive."
        )

    return value
def validate(self, data):

    warehouse_id = data.get("warehouse_id")
    location_id = data.get("location_id")


    location = DUMMY_LOCATIONS.objects.get(
        location_id=location_id
    )

    if location.warehouse_id != warehouse_id:
        raise serializers.ValidationError({
            "location_id":
            "The selected location does not belong "
            "to the selected warehouse."
        })

    return data
        

class ReservationSerializer(serializers.Serializer):
    sales_order_id = serializers.CharField(max_length=100)
    product_id = serializers.IntegerField()
    warehouse_id = serializers.IntegerField()
    location_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Reservation quantity must be greater than zero."
            )

        return value


class ReleaseSerializer(serializers.Serializer):
    sales_order_id = serializers.CharField(max_length=100)
    product_id = serializers.IntegerField()
    warehouse_id = serializers.IntegerField()
    location_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Release quantity must be greater than zero."
            )

        return value