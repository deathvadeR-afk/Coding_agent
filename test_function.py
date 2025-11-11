import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from functions.get_file_content import get_file_content

# Test reading main.py
print("Testing main.py:")
result = get_file_content("calculator", "main.py")
print(result[:200] + "..." if len(result) > 200 else result)
print("\n" + "="*50 + "\n")

# Test reading pkg/calculator.py
print("Testing pkg/calculator.py:")
result = get_file_content("calculator", "pkg/calculator.py")
print(result[:200] + "..." if len(result) > 200 else result)
print("\n" + "="*50 + "\n")

# Test reading lorem.txt (should be truncated)
print("Testing lorem.txt (should be truncated):")
result = get_file_content("calculator", "lorem.txt")
print(f"Length: {len(result)} characters")
print(result[-100:])  # Print the end to see if truncation message is there
print("\n" + "="*50 + "\n")

# Test reading /bin/cat (outside working directory)
print("Testing /bin/cat (outside working directory):")
result = get_file_content("calculator", "/bin/cat")
print(result)
print("\n" + "="*50 + "\n")

# Test reading a non-existent file
print("Testing pkg/does_not_exist.py (non-existent file):")
result = get_file_content("calculator", "pkg/does_not_exist.py")
print(result)