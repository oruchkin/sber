from fastapi import APIRouter, HTTPException
from src.models.deposit import DepositInput, DepositOutput
from src.services.deposit_calculator import calculate_deposit_schedule

router = APIRouter()

@router.post("/calculate", response_model=DepositOutput)
def calculate_deposit(deposit_input: DepositInput):
    try:
        calculation_result = calculate_deposit_schedule(deposit_input)
        return DepositOutput.from_calculation(calculation_result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
