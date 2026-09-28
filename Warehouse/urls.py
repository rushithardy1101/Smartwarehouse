from django.urls import path
from . import views

urlpatterns = [
    path('warehouses/', views.warehouse_list),
    path('locations/', views.location_list),
]