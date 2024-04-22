from datetime import datetime
from typing import Dict
from src.models.deposit import DepositInput
from dateutil.relativedelta import relativedelta


def add_months(start_date: datetime, months: int) -> datetime:
    return start_date + relativedelta(months=months)

def calculate_deposit_schedule(deposit_input: DepositInput) -> Dict[str, float]:
    amount = deposit_input.amount
    schedule = {}
    date = deposit_input.get_date_as_datetime()

    for i in range(deposit_input.periods):
        amount += amount * (deposit_input.rate / 100) / 12
        date = add_months(date, 1)
        schedule[date.strftime("%d.%m.%Y")] = round(amount, 2)

    return schedule
