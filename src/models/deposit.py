from pydantic import BaseModel, validator, Field
from datetime import datetime
from pydantic import BaseModel, create_model
from typing import Dict, List


DATE_FORMAT = "%d.%m.%Y"

class DepositInput(BaseModel):
    date: str = Field(..., example="31.01.2021")
    periods: int = Field(..., ge=1, le=60, example=3)
    amount: float = Field(..., ge=10000, le=3000000, example=10000)
    rate: float = Field(..., ge=1, le=8, example=6)

    @validator('date')
    def validate_date(cls, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return value
        except ValueError:
            raise ValueError("Incorrect date format, should be dd.mm.YYYY")

    def get_date_as_datetime(self) -> datetime:
        return datetime.strptime(self.date, "%d.%m.%Y")



class DepositOutput(BaseModel):
    calculation: Dict[str, float]

    @classmethod
    def from_calculation(cls, calculation: Dict[str, float]) -> 'DepositOutput':
        return cls(calculation=calculation)
