import unittest

from fastapi.testclient import TestClient

from src.main import app
from src.models.deposit import DepositInput
from src.services.deposit_calculator import calculate_deposit_schedule

client = TestClient(app)


class TestDepositCalculator(unittest.IsolatedAsyncioTestCase):
    async def test_calculate_schedule(self):
        deposit_input = DepositInput(date="31.01.2021", periods=7, amount=10000, rate=6)
        result = await calculate_deposit_schedule(deposit_input)
        expected = {
            "31.01.2021": 10050,
            "28.02.2021": 10100.25,
            "31.03.2021": 10150.75,
            "30.04.2021": 10201.51,
            "31.05.2021": 10252.51,
            "30.06.2021": 10303.78,
            "31.07.2021": 10355.29,
        }
        self.assertEqual(result, expected)


class TestDepositInputValidation(unittest.TestCase):
    def test_invalid_date_format(self):
        self.assertRaises(
            ValueError,
            DepositInput, date="2021-01-31", periods=3, amount=10000, rate=6
        )


class TestDepositRate(unittest.TestCase):
    def test_normal_rate(self):
        response = client.post("/api/v1/calculate", json={
            "date": "31.01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": 1
        })
        self.assertEqual(response.status_code, 200)

    def test_high_rate(self):
        response = client.post("/api/v1/calculate", json={
            "date": "31.01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": 20
        })
        self.assertEqual(response.status_code, 422)


class TestDepositAmountBounds(unittest.IsolatedAsyncioTestCase):
    async def test_minimum_amount(self):
        deposit_input = DepositInput(
            date="31.01.2021", periods=3, amount=10000, rate=6
        )
        result = await calculate_deposit_schedule(deposit_input)
        self.assertIn("31.01.2021", result)

    async def test_maximum_amount(self):
        deposit_input = DepositInput(
            date="31.01.2021", periods=3, amount=3000000, rate=6
        )
        result = await calculate_deposit_schedule(deposit_input)
        self.assertIn("31.01.2021", result)


class TestDepositBoundaryConditions(unittest.TestCase):
    def test_zero_periods(self):
        response = client.post("/api/v1/calculate", json={
            "date": "31.01.2021",
            "periods": 0,
            "amount": 10000,
            "rate": 6
        })
        self.assertEqual(response.status_code, 422)

    def test_negative_amount(self):
        response = client.post("/api/v1/calculate", json={
            "date": "31.01.2021",
            "periods": 3,
            "amount": -10000,
            "rate": 6
        })
        self.assertEqual(response.status_code, 422)


class TestApiIntegration(unittest.IsolatedAsyncioTestCase):
    def test_full_integration(self):
        response = client.post("/api/v1/calculate", json={
            "date": "31.01.2021",
            "periods": 12,
            "amount": 50000,
            "rate": 5
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("31.12.2021" in data)


if __name__ == '__main__':
    unittest.main()
