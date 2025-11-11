import os
import re

def extract_function(working_directory, file_path, function_name, start_line, end_line):
    """
    Extract code blocks into functions.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file within the working directory
        function_name (str): Name for the new function
        start_line (int): Starting line number (1-based)
        end_line (int): Ending line number (1-based, inclusive)
        
    Returns:
        str: Success message or error message
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
                lines = f.readlines()
        except UnicodeDecodeError:
            return f'Error: Unable to read "{file_path}" - file may be binary'
        except PermissionError:
            return f'Error: Permission denied to read "{file_path}"'
        except OSError as e:
            return f'Error: Unable to read "{file_path}": {str(e)}'
        
        # Validate line numbers
        if start_line < 1 or end_line > len(lines) or start_line > end_line:
            return f'Error: Invalid line range. File has {len(lines)} lines, requested lines {start_line}-{end_line}'
        
        # Extract the code block
        code_block = lines[start_line-1:end_line]
        
        # Remove the code block from the original file
        new_lines = lines[:start_line-1] + lines[end_line:]
        
        # Create the new function
        indent = re.match(r'^(\s*)', code_block[0]).group(1) if code_block[0].strip() else ''
        function_lines = [f'{indent}def {function_name}():\n']
        
        # Add the extracted code with proper indentation
        for line in code_block:
            if line.strip():  # Only indent non-empty lines
                function_lines.append(indent + '    ' + line.lstrip())
            else:
                function_lines.append('\n')
        
        # Add a call to the new function at the original location
        call_line = f'{indent}{function_name}()\n'
        
        # Insert the new function at the end of the file (before any trailing newlines)
        while new_lines and new_lines[-1] == '\n':
            new_lines.pop()
        
        # Add the function and call
        final_lines = new_lines + ['\n'] + function_lines + ['\n', call_line]
        
        # Write the updated content back to the file
        try:
            with open(abs_full_path, "w", encoding="utf-8") as f:
                f.writelines(final_lines)
            return f'Successfully extracted lines {start_line}-{end_line} into function "{function_name}" in "{file_path}"'
        except PermissionError:
            return f'Error: Permission denied to write to "{file_path}"'
        except OSError as e:
            return f'Error: Unable to write to "{file_path}": {str(e)}'
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_extract_function = {
    "name": "extract_function",
    "description": "Extract a code block from a file into a new function and replace it with a function call.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to modify, relative to the working directory.",
            },
            "function_name": {
                "type": "string",
                "description": "Name for the new function to create.",
            },
            "start_line": {
                "type": "integer",
                "description": "Starting line number (1-based) of the code block to extract.",
            },
            "end_line": {
                "type": "integer",
                "description": "Ending line number (1-based, inclusive) of the code block to extract.",
            },
        },
        "required": ["file_path", "function_name", "start_line", "end_line"],
    },
}