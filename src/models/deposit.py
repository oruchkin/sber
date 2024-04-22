from pydantic import validator, Field
from datetime import datetime
from pydantic import BaseModel
from typing import Dict


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

    def get_date_as_datetime(self) -> datetime:
        return datetime.strptime(self.date, "%d.%m.%Y")


class DepositOutput(BaseModel):
    __root__: Dict[str, float]

    @classmethod
    def from_calculation(cls, calculation: Dict[str, float]) -> 'DepositOutput':
        return cls(__root__=calculation)
