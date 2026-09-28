from rest_framework import serializers
from .models import Product,InventoryTransaction,StockBalance
from Warehouse.models import Warehouse,Location

class StockBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockBalance

        fields = [
            'stock_balance_id',
            'product',
            'warehouse',
            'location',
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
            'product',
            'transaction_type',
            'quantity',
            'source_reference',
            'transaction_date',
        ]

        read_only_fields = [
            'transaction_id',
            'transaction_date',
        ]


class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = StockBalance

        fields = [
            'product',
            'available_quantity',
        ]


class InventoryInSerializer(serializers.Serializer):
    grn_id = serializers.CharField(max_length=100)
    product_id = serializers.IntegerField()
    warehouse_id = serializers.IntegerField()
    location_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    def validate_product_id(self, value):
        if not Product.objects.filter(Product_id=value).exists():
            raise serializers.ValidationError(
                "Invalid product. Product does not exist."
            )
        return value
    
    def validate_warehouse(self, value):
        if not Warehouse.objects.filter(
            warehouse_id=value.warehouse_id
            ).exists():
            raise serializers.ValidationError(
                "Warehouse does not exist."
            )
    
        return value
    
    def validate_location(self, value):
        if not Location.objects.filter(
            location_id=value.location_id
            ).exists():
            raise serializers.ValidationError(
                "Location does not exist."
            )
    
        return value
    
    def validate(self, data):
    
        warehouse = data.get('warehouse')
        location = data.get('location')
    
        if warehouse and location:
            if location.warehouse_id != warehouse.warehouse_id:
                raise serializers.ValidationError({
                    'location':
                        'The selected location does not belong '
                        'to the selected warehouse.'
            })
    
        return data
    

class StockReservationSerializer(serializers.Serializer):
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

class ReservationReleaseSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    warehouse_id = serializers.IntegerField()
    location_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)