#!/usr/bin/env python3
import sys
try:
    print("Attempting to import process_digest module...")
    import app.services.process_digest as pd_module
    print(f"Module imported: {pd_module}")
    print(f"Module file: {pd_module.__file__}")
    print(f"\nAvailable attributes:")
    attrs = dir(pd_module)
    for attr in attrs:
        if not attr.startswith('_'):
            print(f"  - {attr}")
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
