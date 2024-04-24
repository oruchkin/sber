from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field, validator


class DepositInput(BaseModel):
    date: str = Field(..., example="31.01.2021")
    periods: int = Field(..., ge=1, le=60, example=3)
    amount: float = Field(..., ge=10000, le=3000000, example=10000)
    rate: float = Field(..., ge=1, le=8, example=6)

    @validator('date')
    def validate_date(cls, value: str):
        date_format = "%d.%m.%Y"
        try:
            datetime.strptime(value, date_format)
            return value
        except ValueError:
            raise ValueError("Incorrect date format, should be dd.mm.YYYY")

    @validator('periods')
    def validate_periods(cls, value: int):
        if not (1 <= value <= 60):
            raise ValueError("Periods must be between 1 and 60.")
        return value

    @validator('amount')
    def validate_amount(cls, value: float):
        if not (10000 <= value <= 3000000):
            raise ValueError("Amount must be between 10,000 and 3,000,000.")
        return value

    @validator('rate')
    def validate_rate(cls, value: float):
        if not (1 <= value <= 8):
            raise ValueError("Rate must be between 1% and 8%.")
        return value

    def get_date_as_datetime(self) -> datetime:
        return datetime.strptime(self.date, "%d.%m.%Y")


class DepositOutput(BaseModel):
    __root__: Dict[str, float]

    @classmethod
    def from_calculation(cls, calculation: Dict[str, float]) -> 'DepositOutput':
        return cls(__root__=calculation)
