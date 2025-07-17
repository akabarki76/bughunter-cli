import sys
import os

print("Python Path:")
for p in sys.path:
    print(p)

try:
    import restrictedpython
    print("restrictedpython imported successfully!")
except ImportError as e:
    print(f"Error importing restrictedpython: {e}")
