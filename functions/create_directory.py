import os

def create_directory(working_directory, directory_path):
    """
    Create a directory within the working directory.
    
    Args:
        working_directory (str): The base working directory
        directory_path (str): Relative path to the directory to create within the working directory
        
    Returns:
        str: Success message or error message
    """
    try:
        # Create the full path
        full_path = os.path.join(working_directory, directory_path)
        
        # Get absolute paths for comparison
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        # Check if the path is within the working directory boundaries
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot create "{directory_path}" as it is outside the permitted working directory'
        
        # Check if the path already exists
        if os.path.exists(abs_full_path):
            if os.path.isdir(abs_full_path):
                return f'Warning: Directory "{directory_path}" already exists'
            else:
                return f'Error: A file with the name "{directory_path}" already exists'
        
        # Create the directory
        try:
            os.makedirs(abs_full_path, exist_ok=True)
            return f'Successfully created directory "{directory_path}"'
        except PermissionError:
            return f'Error: Permission denied to create directory "{directory_path}"'
        except OSError as e:
            return f'Error: Unable to create directory "{directory_path}": {str(e)}'
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_create_directory = {
    "name": "create_directory",
    "description": "Create a directory within the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "directory_path": {
                "type": "string",
                "description": "The path to the directory to create, relative to the working directory.",
            },
        },
        "required": ["directory_path"],
    },
}