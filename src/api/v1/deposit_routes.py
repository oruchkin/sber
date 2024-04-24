from fastapi import APIRouter

from src.models.deposit import DepositInput, DepositOutput
from src.services.deposit_calculator import calculate_deposit_schedule

router = APIRouter()


@router.post("/calculate", response_model=DepositOutput)
async def calculate_deposit(deposit_input: DepositInput):
    return await calculate_deposit_schedule(deposit_input)
