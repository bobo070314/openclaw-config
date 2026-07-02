'''Main test script for IGP CLI tool

This script tests the IGP CLI tool by running the lifecycle --list command.
'''

import subprocess
import sys

if __name__ == '__main__':
    # Test the lifecycle --list command
    print("Testing 'lifecycle --list' command...")
    result = subprocess.run([sys.executable, 'igp.py', 'lifecycle', '--list'], capture_output=True, text=True)
    print("Output:")
    print(result.stdout)
    print("Errors:")
    print(result.stderr)
    print(f"Exit code: {result.returncode}")

    # Test the lifecycle --version command
    print("\nTesting 'lifecycle --version' command...")
    result = subprocess.run([sys.executable, 'igp.py', 'lifecycle', '--version', 'test_product'], capture_output=True, text=True)
    print("Output:")
    print(result.stdout)
    print("Errors:")
    print(result.stderr)
    print(f"Exit code: {result.returncode}")