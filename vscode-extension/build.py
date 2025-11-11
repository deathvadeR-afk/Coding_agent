#!/usr/bin/env python3
"""
Build script for the VS Code extension
"""

import os
import subprocess
import sys

def build_extension():
    """Build the VS Code extension"""
    print("Building VS Code extension...")
    
    # Check if we're in the right directory
    if not os.path.exists("package.json"):
        print("Error: package.json not found. Please run this script from the vscode-extension directory.")
        return False
    
    # Install dependencies
    print("Installing dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to install npm dependencies.")
        return False
    except FileNotFoundError:
        print("Error: npm not found. Please install Node.js and npm.")
        return False
    
    # Compile TypeScript
    print("Compiling TypeScript...")
    try:
        subprocess.run(["npm", "run", "compile"], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to compile TypeScript.")
        return False
    
    print("Extension built successfully!")
    print("To package the extension, run: vsce package")
    return True

def package_extension():
    """Package the VS Code extension"""
    print("Packaging VS Code extension...")
    
    # Check if vsce is installed
    try:
        subprocess.run(["vsce", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Error: vsce not found. Please install it with: npm install -g vsce")
        return False
    except FileNotFoundError:
        print("Error: vsce not found. Please install it with: npm install -g vsce")
        return False
    
    # Package the extension
    try:
        subprocess.run(["vsce", "package"], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to package the extension.")
        return False
    
    print("Extension packaged successfully!")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "package":
        success = package_extension()
    else:
        success = build_extension()
    
    sys.exit(0 if success else 1)