import sys
import os

# Add the virtual environment's site-packages to the Python path
site_packages_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv', 'lib', 'python3.12', 'site-packages')
sys.path.insert(0, site_packages_path)

print("Python Path:")
for p in sys.path:
    print(p)

