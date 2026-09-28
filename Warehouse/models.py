
from django.db import models


class Warehouse(models.Model):

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    name = models.CharField(
        max_length=150
    )

    city = models.CharField(
        max_length=100,

    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "Warehouse"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Location(models.Model):

    LOCATION_TYPE_CHOICES = [
        ("BIN", "BIN"),
        ("RACK", "RACK"),
        ("AISLE", "AISLE"),
        ("BAY", "BAY"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    code = models.CharField(
        max_length=50,
        db_index=True,
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="locations"
    )

    type = models.CharField(
        max_length=20,
        choices=LOCATION_TYPE_CHOICES,
        default="BIN"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "locations"

        constraints = [
            models.UniqueConstraint(
                fields=["warehouse", "code"],
                name="unique_warehouse_location_code"
            )
        ]

        ordering = ["code"]

    def __str__(self):
        return f"{self.code} ({self.warehouse.name} - {self.type})"