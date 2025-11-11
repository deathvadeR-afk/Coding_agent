import os
import re

def code_complexity(working_directory, file_path):
    """
    Analyze the complexity of a Python file by counting lines, functions, and cyclomatic complexity.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file within the working directory
        
    Returns:
        str: Complexity analysis or error message
    """
    try:
        # Create the full path
        full_path = os.path.join(working_directory, file_path)
        
        # Get absolute paths for comparison
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        # Check if the path is within the working directory boundaries
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
        
        # Check if the path is a file
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file content
        try:
            with open(abs_full_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            return f'Error: Unable to read "{file_path}" - file may be binary'
        except PermissionError:
            return f'Error: Permission denied to read "{file_path}"'
        except OSError as e:
            return f'Error: Unable to read "{file_path}": {str(e)}'
        
        # Analyze complexity metrics
        lines = content.split('\n')
        line_count = len(lines)
        
        # Count functions
        function_pattern = r'^\s*def\s+\w+\s*\('
        function_count = len(re.findall(function_pattern, content, re.MULTILINE))
        
        # Count classes
        class_pattern = r'^\s*class\s+\w+'
        class_count = len(re.findall(class_pattern, content, re.MULTILINE))
        
        # Count control structures for cyclomatic complexity approximation
        control_patterns = [
            r'\bif\b',
            r'\bfor\b',
            r'\bwhile\b',
            r'\belif\b',
            r'\bexcept\b',
            r'\band\b',
            r'\bor\b'
        ]
        
        control_count = 0
        for pattern in control_patterns:
            control_count += len(re.findall(pattern, content))
        
        # Estimate cyclomatic complexity (simplified)
        cyclomatic_complexity = control_count + 1
        
        # Count comments
        comment_pattern = r'^\s*#'
        comment_count = len(re.findall(comment_pattern, content, re.MULTILINE))
        
        # Prepare result
        result = f"Code Complexity Analysis for '{file_path}':\n"
        result += f"  Lines of code: {line_count}\n"
        result += f"  Functions: {function_count}\n"
        result += f"  Classes: {class_count}\n"
        result += f"  Estimated cyclomatic complexity: {cyclomatic_complexity}\n"
        result += f"  Comments: {comment_count}\n"
        
        # Provide complexity rating
        if cyclomatic_complexity > 20:
            result += "  Complexity rating: HIGH - Consider refactoring\n"
        elif cyclomatic_complexity > 10:
            result += "  Complexity rating: MEDIUM - May need refactoring\n"
        else:
            result += "  Complexity rating: LOW - Code is relatively simple\n"
        
        return result
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_code_complexity = {
    "name": "code_complexity",
    "description": "Analyze the complexity of a Python file by counting lines, functions, classes, and estimating cyclomatic complexity.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the Python file to analyze, relative to the working directory.",
            },
        },
        "required": ["file_path"],
    },
}