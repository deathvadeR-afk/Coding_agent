import os

def get_files_info(working_directory, directory="."):
    """
    Get information about files in a directory.
    
    Args:
        working_directory (str): The base working directory
        directory (str): Relative path within the working directory (default: ".")
        
    Returns:
        str: Formatted string with file information or error message
    """
    try:
        # Create the full path
        full_path = os.path.join(working_directory, directory)
        
        # Get absolute paths for comparison
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        # Check if the path is within the working directory boundaries
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the path is a directory
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'
        
        # List directory contents
        try:
            entries = os.listdir(abs_full_path)
        except PermissionError:
            return f'Error: Permission denied to access "{directory}"'
        except OSError as e:
            return f'Error: Unable to access "{directory}": {str(e)}'
        
        # Build the result string
        result_lines = []
        for entry in entries:
            entry_path = os.path.join(abs_full_path, entry)
            try:
                file_size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                result_lines.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
            except OSError:
                # If we can't get file size, still include the entry with unknown size
                is_dir = os.path.isdir(entry_path)
                result_lines.append(f"- {entry}: file_size=unknown bytes, is_dir={is_dir}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_get_files_info = {
    "name": "get_files_info",
    "description": "Lists files in the specified directory along with their sizes, constrained to the working directory. Use this to explore the file structure of a project.",
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            },
        },
    },
}