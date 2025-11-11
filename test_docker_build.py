#!/usr/bin/env python3
"""
Test Docker build process
"""

import subprocess
import sys

def test_docker_build():
    """Test that Docker image can be built successfully"""
    try:
        print("Testing Docker build...")
        result = subprocess.run(
            ["docker", "build", ".", "-t", "coding-assist-test"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print("✓ Docker build successful")
            # Clean up test image
            subprocess.run(["docker", "rmi", "coding-assist-test"], 
                         capture_output=True)
            return True
        else:
            print("✗ Docker build failed")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Docker build timed out")
        return False
    except FileNotFoundError:
        print("Docker not found. Skipping Docker build test.")
        return True  # Not a failure if Docker isn't installed

if __name__ == "__main__":
    success = test_docker_build()
    sys.exit(0 if success else 1)