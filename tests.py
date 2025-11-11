from functions.run_python_file import run_python_file

def test_run_python_file():
    """Test the run_python_file function with various inputs."""
    
    # Test running main.py without arguments
    print("Result for 'main.py' (no arguments):")
    result = run_python_file("calculator", "main.py")
    print(result)
    print()
    
    # Test running main.py with arguments
    print("Result for 'main.py' with '3 + 5':")
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    print()
    
    # Test running tests.py
    print("Result for 'tests.py':")
    result = run_python_file("calculator", "tests.py")
    print(result)
    print()
    
    # Test running a file outside the working directory
    print("Result for '../main.py' (outside working directory):")
    result = run_python_file("calculator", "../main.py")
    print(result)
    print()
    
    # Test running a non-existent file
    print("Result for 'nonexistent.py' (non-existent file):")
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print()
    
    # Test running a non-Python file
    print("Result for 'lorem.txt' (non-Python file):")
    result = run_python_file("calculator", "lorem.txt")
    print(result)
    print()

if __name__ == "__main__":
    test_run_python_file()