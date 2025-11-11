import os
import re

def rename_symbol(working_directory, file_path, old_name, new_name):
    """
    Rename variables, functions, or classes across files.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file within the working directory
        old_name (str): Current name of the symbol
        new_name (str): New name for the symbol
        
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
                content = f.read()
        except UnicodeDecodeError:
            return f'Error: Unable to read "{file_path}" - file may be binary'
        except PermissionError:
            return f'Error: Permission denied to read "{file_path}"'
        except OSError as e:
            return f'Error: Unable to read "{file_path}": {str(e)}'
        
        # Create a regex pattern that matches the symbol as a whole word
        # This prevents partial matches (e.g., renaming "test" shouldn't affect "testing")
        pattern = r'\b' + re.escape(old_name) + r'\b'
        
        # Count occurrences
        occurrences = len(re.findall(pattern, content))
        
        if occurrences == 0:
            return f'No occurrences of "{old_name}" found in "{file_path}"'
        
        # Replace all occurrences
        new_content = re.sub(pattern, new_name, content)
        
        # Write the updated content back to the file
        try:
            with open(abs_full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return f'Successfully renamed "{old_name}" to "{new_name}" ({occurrences} occurrences) in "{file_path}"'
        except PermissionError:
            return f'Error: Permission denied to write to "{file_path}"'
        except OSError as e:
            return f'Error: Unable to write to "{file_path}": {str(e)}'
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_rename_symbol = {
    "name": "rename_symbol",
    "description": "Rename variables, functions, or classes across files, replacing all occurrences of a symbol name.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to modify, relative to the working directory.",
            },
            "old_name": {
                "type": "string",
                "description": "Current name of the symbol to rename.",
            },
            "new_name": {
                "type": "string",
                "description": "New name for the symbol.",
            },
        },
        "required": ["file_path", "old_name", "new_name"],
    },
}