import os
from dotenv import load_dotenv

load_dotenv()

# Ethereum / Sepolia
RPC_URL = os.getenv("RPC_URL")

BACKEND_PRIVATE_KEY = os.getenv("BACKEND_PRIVATE_KEY")
BACKEND_WALLET = os.getenv("BACKEND_WALLET")

MEDICAL_RECORDS_ADDRESS = os.getenv("MEDICAL_RECORDS_ADDRESS")
ACCESS_CONTROL_ADDRESS = os.getenv("ACCESS_CONTROL_ADDRESS")

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY")

# ---- FAIL FAST (IMPORTANT) ----
if not RPC_URL:
    raise RuntimeError("RPC_URL is missing. Check your .env file")
