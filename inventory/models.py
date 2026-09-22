from django.db import models

class StockBalance(models.Model):
    stock_balance_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    warehouse_id = models.IntegerField()
    location_id = models.IntegerField()
    total_quantity = models.PositiveBigIntegerField(default=0)
    reserved_quantity = models.PositiveBigIntegerField(default=0)
    available_quantity = models.PositiveBigIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'stock_balance'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'product_id',
                    'warehouse_id',
                    'location_id'
                ],
                name='unique_product_warehouse_location_stock'
            )
        ]

    def __str__(self):
        return (
            f"Product {self.product_id} - "
            f"Warehouse {self.warehouse_id} - "
            f"Location {self.location_id}"
        )
    

class InventoryTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    TRANSACTION_TYPES = [
        ('IN', 'Stock IN'),
        ('OUT', 'Stock OUT'),
        ('RESERVED', 'Reserved'),
        ('RELEASED', 'Released'),
        ('ADJUSTMENT', 'Adjustment'),
    ]

    transaction_type = models.CharField(max_length=20,choices=TRANSACTION_TYPES)
    ADJUSTMENT_TYPES = [
        ('INCREASE', 'Increase'),
        ('DECREASE', 'Decrease'),
    ]

    adjustment_type = models.CharField(
        max_length=20,
        choices=ADJUSTMENT_TYPES,
        null=True,
        blank=True
    )

    adjustment_reason = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    quantity = models.PositiveBigIntegerField()

    reference_type = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    reference_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'inventory_transaction'
        ordering = ['-created_at']

    def __str__(self):
        return (
            f"{self.transaction_type} - "
            f"Product {self.product_id} - "
            f"{self.quantity}"
        )