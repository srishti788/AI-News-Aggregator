#!/usr/bin/env python3
import sys
import importlib.util

# Load the module from file and execute it with error handling
spec = importlib.util.spec_from_file_location("test_module", "app/services/process_digest.py")
module = importlib.util.module_from_spec(spec)

try:
    print("Executing module...")
    spec.loader.exec_module(module)
    print("✓ Module executed successfully")
    print(f"\nModule attributes: {[x for x in dir(module) if not x.startswith('_')]}")
except Exception as e:
    print(f"✗ Error during module execution: {e}")
    import traceback
    traceback.print_exc()
