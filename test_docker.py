#!/usr/bin/env python3
"""
Test script to verify Docker setup
"""

import os
import subprocess
import sys

def test_docker_files():
    """Test that all required Docker files exist"""
    required_files = [
        'Dockerfile',
        'docker-compose.yml',
        '.dockerignore',
        'requirements.txt'
    ]
    
    print("Checking for required Docker files...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} found")
        else:
            print(f"✗ {file} missing")
            return False
    
    print("All Docker files are present!")
    return True

def test_docker_build():
    """Test that Docker image can be built"""
    try:
        print("Testing Docker build...")
        result = subprocess.run(
            ['docker', 'build', '.', '-t', 'coding-assist-test'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print("✓ Docker build successful")
            # Clean up test image
            subprocess.run(['docker', 'rmi', 'coding-assist-test'], 
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
        print("Docker not found. Please install Docker to test.")
        return False

def main():
    print("Docker Setup Verification")
    print("=" * 30)
    
    if not test_docker_files():
        sys.exit(1)
    
    # Only test build if Docker is available
    if test_docker_build():
        print("\nDocker setup is ready!")
    else:
        print("\nDocker setup has issues. Please check the errors above.")

if __name__ == "__main__":
    main()