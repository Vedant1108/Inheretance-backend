from services.blockchain import get_all_records, has_access

# replace with real addresses
PATIENT = "0x742d35Cc6bA49516c7D8E9174516bD2aF0722f"
DOCTOR  = "0xDoctorAddressHere"

print("Checking access...")
print(has_access(PATIENT, DOCTOR))

print("\nFetching records...")
records = get_all_records(PATIENT)
print(records)
