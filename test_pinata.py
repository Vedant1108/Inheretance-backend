from services.pinata_service import upload_to_ipfs

try:
    cid = upload_to_ipfs("test_upload.txt")
    print("✅ Upload successful")
    print("CID:", cid)
    print("Gateway URL:")
    print(f"https://gateway.pinata.cloud/ipfs/{cid}")
except Exception as e:
    print("❌ Upload failed")
    print(e)
