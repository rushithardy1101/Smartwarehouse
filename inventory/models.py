from django.db import models
class Product(models.Model):
    Product_id = models.AutoField(primary_key=True)
    Product_name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.Product_name
    
class StockBalance(models.Model):
    stock_balance_id = models.AutoField(primary_key=True)

    product = models.ForeignKey(Product,on_delete=models.PROTECT)


    warehouse = models.ForeignKey(
        'Warehouse.Warehouse',
        on_delete=models.PROTECT,
    )

    location = models.ForeignKey(
        'Warehouse.Location',
        on_delete=models.PROTECT,
    )

    total_quantity = models.PositiveBigIntegerField(default=0)
    reserved_quantity = models.PositiveBigIntegerField(default=0)
    available_quantity = models.PositiveBigIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stockbalance'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'warehouse', 'location'],
                name='unique_product_warehouse_location_stock'
            )
        ]

    def __str__(self):
        return f"{self.product} - {self.warehouse} - {self.location}"

class InventoryTransaction(models.Model):

    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('RESERVE', 'Reservation'),
        ('RELEASE', 'Reservation Release'),
        ('ADJUSTMENT', 'Stock Adjustment'),
    ]

    transaction_id = models.AutoField(primary_key=True)

    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    quantity = models.PositiveBigIntegerField()

    source_reference = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_type}"

    class Meta:
        db_table = 'inventorytransaction'

