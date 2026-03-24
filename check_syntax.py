#!/usr/bin/env python3
"""Test compiling the process_digest file"""
import py_compile
import sys

try:
    py_compile.compile('app/services/process_digest.py', doraise=True)
    print("✓ File compiles successfully")
except py_compile.PyCompileError as e:
    print(f"✗ Compilation error: {e}")
    sys.exit(1)

# Now try to actually execute it
print("\nTrying to parse and list functions...")
import ast
with open('app/services/process_digest.py', 'r') as f:
    content = f.read()
    
try:
    tree = ast.parse(content)
    print("✓ File parses successfully")
    
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    print(f"\nFunctions found: {functions}")
    
except SyntaxError as e:
    print(f"✗ Syntax error: {e}")
    sys.exit(1)
