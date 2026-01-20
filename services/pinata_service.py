import requests
from config import PINATA_API_KEY, PINATA_SECRET_KEY

PINATA_PIN_FILE_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"


def upload_to_ipfs(file_path: str) -> str:
    """
    Upload a file to Pinata IPFS and return CID (IpfsHash)
    """

    if not PINATA_API_KEY or not PINATA_SECRET_KEY:
        raise RuntimeError("Pinata API keys are missing")

    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_KEY
    }

    with open(file_path, "rb") as f:
        files = {
            "file": f
        }

        response = requests.post(
            PINATA_PIN_FILE_URL,
            files=files,
            headers=headers,
            timeout=60
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"Pinata upload failed: {response.status_code} {response.text}"
        )

    data = response.json()
    return data["IpfsHash"]
