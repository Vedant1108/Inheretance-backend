from web3 import Web3
import json
from config import (
    RPC_URL,
    MEDICAL_RECORDS_ADDRESS,
    ACCESS_CONTROL_ADDRESS,
    BACKEND_PRIVATE_KEY,
    BACKEND_WALLET
)

print("RPC_URL from config =", RPC_URL)

# -------------------------------
# Web3 connection
# -------------------------------
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise RuntimeError("❌ Failed to connect to Sepolia RPC")

print("✅ Connected to Sepolia")

# -------------------------------
# Load ABIs
# -------------------------------
with open("contracts/MedicalRecords.json") as f:
    medical_records_abi = json.load(f)["abi"]

with open("contracts/AccessControl.json") as f:
    access_control_abi = json.load(f)["abi"]

# -------------------------------
# Contract instances
# -------------------------------
medical_records_contract = w3.eth.contract(
    address=Web3.to_checksum_address(MEDICAL_RECORDS_ADDRESS),
    abi=medical_records_abi
)

access_control_contract = w3.eth.contract(
    address=Web3.to_checksum_address(ACCESS_CONTROL_ADDRESS),
    abi=access_control_abi
)

# -------------------------------
# READ FUNCTIONS (SAFE)
# -------------------------------

def get_all_records(patient_address: str):
    """
    Fetch all medical records for a patient
    """
    return medical_records_contract.functions.getAllRecords(
        Web3.to_checksum_address(patient_address)
    ).call()


def has_access(patient_address: str, doctor_address: str) -> bool:
    """
    Check if doctor has access to patient's records
    """
    return access_control_contract.functions.hasAccess(
        Web3.to_checksum_address(patient_address),
        Web3.to_checksum_address(doctor_address)
    ).call()


# -------------------------------
# WRITE FUNCTION (TX)
# -------------------------------

def add_record(patient_address: str, cid: str, record_type: str):
    """
    Store CID on blockchain
    """
    nonce = w3.eth.get_transaction_count(BACKEND_WALLET)

    tx = medical_records_contract.functions.addRecord(
        Web3.to_checksum_address(patient_address),
        cid,
        record_type
    ).build_transaction({
        "from": BACKEND_WALLET,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.eth.gas_price
    })

    signed_tx = w3.eth.account.sign_transaction(tx, BACKEND_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)


    return tx_hash.hex()

def get_all_records(patient_address: str):
    """
    Fetch all medical records (CIDs + types) for a patient
    """

    if not Web3.is_address(patient_address):
        raise ValueError("Invalid Ethereum address")

    records = medical_records_contract.functions.getAllRecords(
        patient_address
    ).call()

    # Expected Solidity return:
    # [(cid, recordType), (cid, recordType), ...]

    return [
        {
            "cid": r[0],
            "record_type": r[1],
            "ipfs_url": f"https://gateway.pinata.cloud/ipfs/{r[0]}"
        }
        for r in records
    ]


def has_access(patient_address: str, doctor_address: str) -> bool:
    """
    Check if doctor has access to patient's records
    """
    if not Web3.is_address(patient_address) or not Web3.is_address(doctor_address):
        raise ValueError("Invalid Ethereum address")

    return access_control_contract.functions.hasAccess(
        patient_address,
        doctor_address
    ).call()


def grant_access(patient_address: str, doctor_address: str) -> str:
    """
    Grant doctor access to patient's records (transaction)
    """
    if not Web3.is_address(patient_address) or not Web3.is_address(doctor_address):
        raise ValueError("Invalid Ethereum address")

    nonce = w3.eth.get_transaction_count(BACKEND_WALLET)

    tx = access_control_contract.functions.grantAccess(
        doctor_address
    ).build_transaction({
        "from": BACKEND_WALLET,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.to_wei("10", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, BACKEND_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return tx_hash.hex()
