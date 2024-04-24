from calendar import monthrange
from datetime import datetime
from typing import Dict

from dateutil.relativedelta import relativedelta

from src.models.deposit import DepositInput


async def add_months(start_date: datetime, months: int, original_day: int) -> datetime:
    new_date = start_date + relativedelta(months=months)
    days_in_new_month = monthrange(new_date.year, new_date.month)[1]

    if original_day > days_in_new_month:
        new_date = new_date.replace(day=days_in_new_month)
    else:
        new_date = new_date.replace(day=original_day)

    return new_date


async def calculate_deposit_schedule(deposit_input: DepositInput) -> Dict[str, float]:
    amount = deposit_input.amount
    schedule = {}
    date = deposit_input.get_date_as_datetime()
    original_day = date.day

    for period in range(deposit_input.periods):
        amount += amount * (deposit_input.rate / 100) / 12
        formatted_date = date.strftime("%d.%m.%Y")
        schedule[formatted_date] = round(amount, 2)
        date = await add_months(date, 1, original_day)

    return schedule
