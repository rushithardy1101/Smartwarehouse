from django.db import transaction, models
from decimal import Decimal
from rest_framework.exceptions import ValidationError
from .models import StockBalance, InventoryTransaction
from .dummy_grns import DUMMY_GRNS
from .dummy_reservations import DUMMY_SALES_ORDERS
def validate_grn_exists(grn_id):
    grn = DUMMY_GRNS.get(grn_id)
    if not grn:
        raise ValidationError("Invalid GRN . GRN does not exist")
    return grn

def stock_in(stock_balance,quantity):
    stock_balance.total_quantity += quantity
    stock_balance.available_quantity += quantity
    stock_balance.save()

def reserve_stock(stock_balance,quantity):
    stock_balance.reserved_quantity += quantity
    stock_balance.available_quantity -= quantity
    stock_balance.save()

def release_stock(stock_balance, quantity):
    stock_balance.reserved_quantity -= quantity
    stock_balance.available_quantity += quantity
    stock_balance.save()
#Inventory In Process
@transaction.atomic
def process_inventory_in(grn_id,product_id,warehouse_id,location_id,received_quantity):
    
    grn = validate_grn_exists(grn_id)
    if grn['warehouse_id'] != warehouse_id:
        raise ValidationError(
            "The selected warehouse does not belong to this GRN."
        )
    grn_item = next(
        (
            item
            for item in grn['items']
            if item['product_id'] == product_id
        ),
        None
    )

    if grn_item is None:
        raise ValidationError("The selected product is not part of this GRN.")
    grn_quantity = grn_item['grn_quantity']
    if received_quantity <= 0:
        raise ValidationError("Received quantity must be greater than 0")
    already_received = (
        InventoryTransaction.objects
        .filter(
            transaction_type='IN',
            source_reference=grn_id,
            product_id=product_id
        )
        .aggregate(
            total_received=models.Sum('quantity')
        )['total_received'] or 0
    )

    remaining_quantity = grn_quantity - already_received

    if remaining_quantity <= 0:
        raise ValidationError("This product in the GRN has already been completely processed.")

    if received_quantity > remaining_quantity:
        raise ValidationError(f"Only {remaining_quantity} quantity remains for this product in this GRN.")
    stock_balance, created = StockBalance.objects.get_or_create(
        product_id=product_id,
        warehouse_id=warehouse_id,
        location_id=location_id,
        defaults={
            'total_quantity': 0,
            'reserved_quantity': 0,
            'available_quantity': 0,
        }
    )


    stock_balance = StockBalance.objects.select_for_update().get(
        product_id=product_id,
        warehouse_id=warehouse_id,
        location_id=location_id
    )

    stock_in(stock_balance,received_quantity)
    InventoryTransaction.objects.create(
        product_id=product_id,
        transaction_type='IN',
        quantity=received_quantity,
        source_reference=grn_id
    )

    remaining_quantity -= received_quantity

    return {
        'grn_id': grn_id,
        'product_id': product_id,
        'warehouse_id': warehouse_id,
        'location_id': location_id,
        'received_quantity': received_quantity,
        'remaining_quantity': remaining_quantity,
    }
#Reserved_quantity
@transaction.atomic
def process_stock_reservation(sales_order_id,product_id,warehouse_id,location_id,quantity):
    product_id = int(product_id)
    warehouse_id = int(warehouse_id)
    location_id = int(location_id)
    quantity = Decimal(str(quantity))

    if quantity <= Decimal("0"):
        raise ValidationError("Reservation quantity must be greater than 0.")

    try:
        stock_balance = StockBalance.objects.select_for_update().get(
            product_id=product_id,
            warehouse_id=warehouse_id,
            location_id=location_id
        )
    except StockBalance.DoesNotExist:
        raise ValidationError("Stock balance does not exist for the selected product, warehouse, and location.")

    if stock_balance.available_quantity < quantity:
        raise ValidationError(f"Insufficient stock. Available: {stock_balance.available_quantity}, Requested: {quantity}")

    reserve_stock(stock_balance, quantity)

    InventoryTransaction.objects.create(
        product_id=product_id,
        transaction_type='RESERVED',
        quantity=quantity,
        source_reference=str(sales_order_id)
    )

    return {
        "sales_order_id": sales_order_id,
        "product_id": product_id,
        "warehouse_id": warehouse_id,
        "location_id": location_id,
        "reserved_quantity": quantity,
        "remaining_available_quantity": stock_balance.available_quantity
    }
#Reservation Release
@transaction.atomic
def process_reservation_release(sales_order_id,product_id,warehouse_id,location_id,quantity):
    product_id = int(product_id)
    warehouse_id = int(warehouse_id)
    location_id = int(location_id)
    quantity = Decimal(str(quantity))

    if quantity <= Decimal("0"):
        raise ValidationError("Release quantity must be greater than 0.")

    try:
        stock_balance = StockBalance.objects.select_for_update().get(
            product_id=product_id,
            warehouse_id=warehouse_id,
            location_id=location_id
        )
    except StockBalance.DoesNotExist:
        raise ValidationError(
            "Stock balance does not exist for the selected product, warehouse and location."
        )
    if stock_balance.reserved_quantity < quantity:
        raise ValidationError(
            f"Cannot release {quantity}. Currently reserved quantity is only {stock_balance.reserved_quantity}."
        )

    release_stock(stock_balance, quantity)

    InventoryTransaction.objects.create(
        product_id=product_id,
        transaction_type='RELEASED',
        quantity=quantity,
        source_reference=str(sales_order_id)
    )

    return {
        "sales_order_id": sales_order_id,
        "product_id": product_id,
        "warehouse_id": warehouse_id,
        "location_id": location_id,
        "released_quantity": quantity,
        "remaining_reserved_quantity": stock_balance.reserved_quantity,
        "available_quantity": stock_balance.available_quantity
    }