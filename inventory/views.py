from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import StockBalance, InventoryTransaction
from .serializers import (
    InventoryTransactionSerializer,
    StockBalanceSerializer,
    InventoryInSerializer,ReleaseSerializer,ReservationSerializer
)
from .service import process_inventory_in,process_reservation,process_release


@api_view(['GET'])
def stock_balance(request, product_id=None, location_id=None):
    try:
        stock = StockBalance.objects.all()

        if product_id is not None:
            stock = stock.filter(product_id=product_id)
        if location_id is not None:
            stock = stock.filter(location_id=location_id)
        serializer = StockBalanceSerializer(stock,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def transaction_history(request, transaction_id=None):
    try:
        if transaction_id is not None:

            transaction = get_object_or_404(InventoryTransaction,transaction_id=transaction_id)

            serializer = InventoryTransactionSerializer(transaction)
            return Response(serializer.data)

        transactions = InventoryTransaction.objects.all()

        serializer = InventoryTransactionSerializer(transactions, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def inventory_in(request):

    serializer = InventoryInSerializer(
        data=request.data
    )

    if serializer.is_valid():

        result = process_inventory_in(
            grn_id=serializer.validated_data['grn_id'],
            received_quantity=serializer.validated_data['quantity']
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
def availability(request, product_id):

    stock = StockBalance.objects.filter(
        product_id=product_id
    )

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
def reservation(request):

    serializer = ReservationSerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    try:

        result = process_reservation(
            sales_order_id=serializer.validated_data['sales_order_id'],
            product_id=serializer.validated_data['product_id'],
            warehouse_id=serializer.validated_data['warehouse_id'],
            location_id=serializer.validated_data['location_id'],
            quantity=serializer.validated_data['quantity']
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )

    except ValidationError as error:

        return Response(
            {
                "error": error.detail
            },
            status=status.HTTP_400_BAD_REQUEST
        )
@api_view(['POST'])
def release(request,sales_order_id):

    serializer = ReleaseSerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    try:

        result = process_release(
            sales_order_id=serializer.validated_data['sales_order_id'],
            product_id=serializer.validated_data['product_id'],
            warehouse_id=serializer.validated_data['warehouse_id'],
            location_id=serializer.validated_data['location_id'],
            quantity=serializer.validated_data['quantity']
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )

    except ValidationError as error:

        return Response(
            {
                "error": error.detail
            },
            status=status.HTTP_400_BAD_REQUEST
        )

