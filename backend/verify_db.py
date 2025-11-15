print("Importing database models to verify schema...")
try:
    from src.database import models
    print("Models imported successfully. Schema should be valid.")
except Exception as e:
    print(f"Error importing models: {e}")
