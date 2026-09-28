from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import StockBalance, InventoryTransaction
from .serializers import (
    InventoryTransactionSerializer,
    StockBalanceSerializer,InventoryInSerializer,StockReservationSerializer,ReservationReleaseSerializer
)
from .service import process_inventory_in,process_stock_reservation,process_reservation_release

@api_view(['GET'])
def stock_balance(request, product_id=None, location_id=None):

    stock = StockBalance.objects.all()

    if product_id is not None:
        stock = stock.filter(product_id=product_id)

        if not stock.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if location_id is not None:
        stock = stock.filter(location_id=location_id)

        if not stock.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = StockBalanceSerializer(stock, many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def transaction_history(request, transaction_id=None):
    if transaction_id is not None:

        transaction = get_object_or_404(InventoryTransaction,transaction_id=transaction_id)

        serializer = InventoryTransactionSerializer(transaction)
        return Response(serializer.data)

    transactions = InventoryTransaction.objects.all()

    serializer = InventoryTransactionSerializer(transactions, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def availability(request, product_id):

    stock = StockBalance.objects.filter(product_id=product_id)
    if not stock.exists():
        return Response(
            {
                "message": "Product stock not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    total_available = sum(
        item.available_quantity
        for item in stock
    )

    return Response(
        {
            "product_id": product_id,
            "available_quantity": total_available
        },
        status=status.HTTP_200_OK
    )



@api_view(['POST'])
def inventory_in(request):
    serializer = InventoryInSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "message": "Invalid inventory IN request.",
                "errors": serializer.errors  
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = process_inventory_in(
            grn_id=serializer.validated_data['grn_id'],
            product_id=serializer.validated_data['product_id'],
            warehouse_id=serializer.validated_data['warehouse_id'],
            location_id=serializer.validated_data['location_id'],
            received_quantity=serializer.validated_data['quantity']
        )

        return Response(
            {
                "success": True,
                "message": "Inventory received successfully.",
                "data": result
            },
            status=status.HTTP_200_OK
        )

    except ValidationError as e:
        return Response(
            {
                "success": False,
                "message": e.detail if hasattr(e, 'detail') else str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
@api_view(['POST'])
def stock_reservation(request):

    serializer = StockReservationSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "message": "Invalid stock reservation request.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = process_stock_reservation(
            sales_order_id=serializer.validated_data['sales_order_id'],
            product_id=serializer.validated_data['product_id'],
            warehouse_id=serializer.validated_data['warehouse_id'],
            location_id=serializer.validated_data['location_id'],
            quantity=serializer.validated_data['quantity']
        )

        return Response(
            {
                "success": True,
                "message": "Stock reserved successfully.",
                "data": result
            },
            status=status.HTTP_200_OK
        )

    except ValidationError as e:
        return Response(
            {
                "success": False,
                "message": (
                    e.detail[0]
                    if isinstance(e.detail, list)
                    else e.detail
                )
            },
            status=status.HTTP_400_BAD_REQUEST
        )
@api_view(['POST'])
def reservation_release(request, sales_order_id):

    serializer = ReservationReleaseSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "message": "Invalid reservation release request.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = process_reservation_release(
            sales_order_id=sales_order_id,
            product_id=serializer.validated_data['product_id'],
            warehouse_id=serializer.validated_data['warehouse_id'],
            location_id=serializer.validated_data['location_id'],
            quantity=serializer.validated_data['quantity']
        )

        return Response(
            {
                "success": True,
                "message": "Reservation released successfully.",
                "data": result
            },
            status=status.HTTP_200_OK
        )

    except ValidationError as e:
        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )