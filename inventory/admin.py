from django.contrib import admin
from .models import Product, StockBalance, InventoryTransaction

admin.site.register(Product)
admin.site.register(StockBalance)
admin.site.register(InventoryTransaction)