
DUMMY_SALES_ORDERS = {
    "SO-0001": {
        "sales_order_id": "SO-0001",
        "customer_name": "Retailer Alpha",
        "warehouse_id": 1,
        "status": "PENDING",
        "items": [
            {
                "product_id": 1,
                "order_quantity": 40
            },
            {
                "product_id": 2,
                "order_quantity": 25
            }
        ]
    },
    "SO-0002": {
        "sales_order_id": "SO-0002",
        "customer_name": "Beta Electronics",
        "warehouse_id": 1,
        "status": "PENDING",
        "items": [
            {
                "product_id": 2,
                "order_quantity": 50
            }
        ]
    },
    "SO-0003": {
        "sales_order_id": "SO-0003",
        "customer_name": "Gamma Distributors",
        "warehouse_id": 2,  # Different warehouse for cross-warehouse testing
        "status": "PENDING",
        "items": [
            {
                "product_id": 1,
                "order_quantity": 10
            }
        ]
    }
}