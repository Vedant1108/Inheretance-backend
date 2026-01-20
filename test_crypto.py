from services.crypto import generate_key, encrypt_file, decrypt_file

key = generate_key()

encrypt_file("test_upload.txt", "encrypted.enc", key)
decrypt_file("encrypted.enc", "decrypted.txt", key)

print("Encryption + Decryption successful")
