from django.urls import path
from . import views

urlpatterns = [
    path('stock/', views.stock_balance),
    path('stock/<int:product_id>/', views.stock_balance),
    path('locations/<int:location_id>/stock/', views.stock_balance),
    path('transactions/', views.transaction_history),
    path('transactions/<int:transaction_id>/',views.transaction_history),
    path('availability/<int:product_id>/', views.availability),
    path('in/',views.inventory_in),
    path('reservations/', views.stock_reservation),
    path(
    'reservations/<str:sales_order_id>/release/',
    views.reservation_release
)

]