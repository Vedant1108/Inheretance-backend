from fastapi import APIRouter, HTTPException
from web3 import Web3

from services.blockchain import grant_access

router = APIRouter(prefix="/access", tags=["Access Control"])


@router.post("/grant")
def grant_doctor_access(patient_address: str, doctor_address: str):
    if not Web3.is_address(patient_address) or not Web3.is_address(doctor_address):
        raise HTTPException(status_code=400, detail="Invalid address")

    try:
        tx_hash = grant_access(patient_address, doctor_address)
        return {
            "status": "success",
            "transaction_hash": tx_hash
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
