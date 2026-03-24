#!/usr/bin/env python3
"""Check the raw content and encoding of process_digest.py"""

with open('app/services/process_digest.py', 'rb') as f:
    content = f.read()
    
print(f"File size: {len(content)} bytes")
print(f"First 50 bytes: {content[:50]!r}")
bom_marker = b'\xef\xbb\xbf'
has_bom = 'UTF-8 BOM' if content.startswith(bom_marker) else 'No BOM'
print(f"Has BOM: {has_bom}")

# Try to decode different ways
try:
    decoded = content.decode('utf-8')
    print("✓ Decodes as UTF-8")
except:
    print("✗ Cannot decode as UTF-8")
    
try:
    decoded = content.decode('utf-8-sig')
    print("✓ Decodes as UTF-8-sig")
except:
    print("✗ Cannot decode as UTF-8-sig")

# Check for the function definition
if b'def process_digests' in content:
    print("✓ File contains 'def process_digests'")
    idx = content.find(b'def process_digests')
    print(f"Found at byte: {idx}")
    print(f"Context: {content[idx-10:idx+50]!r}")
else:
    print("✗ File does NOT contain 'def process_digests'")

# List all lines
print("\n=== First 30 lines ===")
lines = content.split(b'\\n')
for i, line in enumerate(lines[:30], 1):
    print(f"{i:3}: {line!r}")
