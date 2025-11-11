import os
from .config import MAX_FILE_CHARS

def get_file_content(working_directory, file_path):
    """
    Get the content of a file within a working directory.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file within the working directory
        
    Returns:
        str: File content as string or error message
    """
    try:
        # Create the full path
        full_path = os.path.join(working_directory, file_path)
        
        # Get absolute paths for comparison
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        # Check if the path is within the working directory boundaries
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the path is a file
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file content
        try:
            with open(abs_full_path, "r", encoding="utf-8") as f:
                file_content = f.read(MAX_FILE_CHARS + 1)  # Read one extra char to check if truncation needed
                
                # If file is longer than MAX_FILE_CHARS, truncate and add message
                if len(file_content) > MAX_FILE_CHARS:
                    file_content = file_content[:MAX_FILE_CHARS] + f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
                
                return file_content
        except UnicodeDecodeError:
            # Try reading as binary and decode with error handling
            with open(abs_full_path, "rb") as f:
                file_content = f.read(MAX_FILE_CHARS + 1)
                if len(file_content) > MAX_FILE_CHARS:
                    return file_content[:MAX_FILE_CHARS].decode('utf-8', errors='ignore') + f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
                else:
                    return file_content.decode('utf-8', errors='ignore')
        except PermissionError:
            return f'Error: Permission denied to read "{file_path}"'
        except OSError as e:
            return f'Error: Unable to read "{file_path}": {str(e)}'
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_get_file_content = {
    "name": "get_file_content",
    "description": "Read the contents of a file within the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to read, relative to the working directory.",
            },
        },
        "required": ["file_path"],
    },
}