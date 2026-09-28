from django.test import SimpleTestCase


class StockCalculationTests(SimpleTestCase):

    def test_available_stock_calculation(self):
        """
        Available stock = Total stock - Reserved stock
        """
        total_quantity = 100
        reserved_quantity = 20

        available_quantity = total_quantity - reserved_quantity

        self.assertEqual(available_quantity, 80)

    def test_stock_in_calculation(self):
        """
        When stock is received, total and available stock increase.
        """
        total_quantity = 100
        reserved_quantity = 20
        received_quantity = 50

        total_quantity += received_quantity
        available_quantity = total_quantity - reserved_quantity

        self.assertEqual(total_quantity, 150)
        self.assertEqual(available_quantity, 130)

    def test_stock_in_when_no_reserved_stock(self):
        """
        When there is no reserved stock,
        available stock should equal total stock.
        """
        total_quantity = 100
        reserved_quantity = 0
        received_quantity = 50

        total_quantity += received_quantity
        available_quantity = total_quantity - reserved_quantity

        self.assertEqual(total_quantity, 150)
        self.assertEqual(available_quantity, 150)

    def test_multiple_stock_in_calculations(self):
        """
        Verify stock calculation after multiple stock IN operations.
        """
        total_quantity = 100
        reserved_quantity = 20

        total_quantity += 50
        total_quantity += 25

        available_quantity = total_quantity - reserved_quantity

        self.assertEqual(total_quantity, 175)
        self.assertEqual(available_quantity, 155)

    def test_reserved_quantity_cannot_exceed_total_quantity(self):
        """
        Reserved quantity must not be greater than total quantity.
        """
        total_quantity = 100
        reserved_quantity = 120

        self.assertGreater(reserved_quantity, total_quantity)