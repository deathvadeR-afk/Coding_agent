import os

def write_file(working_directory, file_path, content):
    """
    Write content to a file within a working directory.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file within the working directory
        content (str): Content to write to the file
        
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
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create the directory if it doesn't exist
        dir_name = os.path.dirname(abs_full_path)
        if dir_name and not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name, exist_ok=True)
            except OSError as e:
                return f'Error: Unable to create directory for "{file_path}": {str(e)}'
        
        # Write the content to the file
        try:
            with open(abs_full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except PermissionError:
            return f'Error: Permission denied to write to "{file_path}"'
        except OSError as e:
            return f'Error: Unable to write to "{file_path}": {str(e)}'
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_write_file = {
    "name": "write_file",
    "description": "Write or overwrite content to a file within the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to write, relative to the working directory.",
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file.",
            },
        },
        "required": ["file_path", "content"],
    },
}