from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from web3 import Web3

from services.pinata_service import upload_to_ipfs
from services.blockchain import add_record, get_all_records, has_access
from services.crypto import generate_key, encrypt_file


router = APIRouter(prefix="/records", tags=["Records"])


@router.post("/upload-record")
async def upload_record(
    file: UploadFile = File(...),
    patient_address: str = Form(...),
    record_type: str = Form(...)
):
    # -------------------------------
    # Validate Ethereum address
    # -------------------------------
    if not Web3.is_address(patient_address):
        raise HTTPException(status_code=400, detail="Invalid patient address")

    # -------------------------------
    # Save file temporarily
    # -------------------------------
    temp_file_path = f"/tmp/{file.filename}"

    try:
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # -------------------------------
        # Upload to IPFS (Pinata)
        # -------------------------------
        # -------------------------------
        # Encrypt file before IPFS
        # -------------------------------
        key = generate_key()
        encrypted_path = f"{temp_file_path}.enc"

        encrypt_file(temp_file_path, encrypted_path, key)

        # -------------------------------
        # Upload encrypted file to IPFS
        # -------------------------------
        cid = upload_to_ipfs(encrypted_path)


        # -------------------------------
        # Store CID on blockchain
        # -------------------------------
        tx_hash = add_record(patient_address, cid, record_type)

        return {
            "status": "success",
            "cid": cid,
            "transaction_hash": tx_hash,
            "encryption_key": key.decode()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{patient_address}")
def fetch_records(patient_address: str, doctor_address: str):
    if not Web3.is_address(patient_address) or not Web3.is_address(doctor_address):
        raise HTTPException(status_code=400, detail="Invalid address")

    # 🔐 ACCESS CHECK
    if not has_access(patient_address, doctor_address):
        raise HTTPException(status_code=403, detail="Access denied")

    records = get_all_records(patient_address)

    return {
        "patient": patient_address,
        "records": records
    }

