# run_tests.py
# author: nsarathy

import subprocess
import sys
import os

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Install in editable mode
    print("Installing package in editable mode...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", project_root])

    # Step 2: Run tests using unittest
    print("\nRunning tests...")
    subprocess.check_call([sys.executable, "-m", "unittest", "discover", "tests"])

if __name__ == "__main__":
    main()
