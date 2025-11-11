import os

def delete_file(working_directory, file_path):
    """
    Delete a file within the working directory.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file within the working directory
        
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
            return f'Error: Cannot delete "{file_path}" as it is outside the permitted working directory'
        
        # Check if the path is a file
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Delete the file
        try:
            os.remove(abs_full_path)
            return f'Successfully deleted "{file_path}"'
        except PermissionError:
            return f'Error: Permission denied to delete "{file_path}"'
        except OSError as e:
            return f'Error: Unable to delete "{file_path}": {str(e)}'
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_delete_file = {
    "name": "delete_file",
    "description": "Delete a file within the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to delete, relative to the working directory.",
            },
        },
        "required": ["file_path"],
    },
}