import os

def count_lines(working_directory, file_path):
    """
    Count lines of code in a file.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file within the working directory
        
    Returns:
        str: Line count information or error message
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
        
        # Read the file and count lines
        try:
            with open(abs_full_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            total_lines = len(lines)
            
            # Count non-empty lines and comment lines (for Python files)
            non_empty_lines = 0
            comment_lines = 0
            
            for line in lines:
                stripped_line = line.strip()
                if stripped_line:  # Non-empty line
                    non_empty_lines += 1
                    if stripped_line.startswith('#'):  # Comment line
                        comment_lines += 1
            
            result = f"Line count for '{file_path}':\n"
            result += f"  Total lines: {total_lines}\n"
            result += f"  Non-empty lines: {non_empty_lines}\n"
            result += f"  Comment lines: {comment_lines}\n"
            result += f"  Code lines: {non_empty_lines - comment_lines}\n"
            
            return result
            
        except UnicodeDecodeError:
            return f'Error: Unable to read "{file_path}" - file may be binary'
        except PermissionError:
            return f'Error: Permission denied to read "{file_path}"'
        except OSError as e:
            return f'Error: Unable to read "{file_path}": {str(e)}'
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_count_lines = {
    "name": "count_lines",
    "description": "Count lines of code in a file, including total lines, non-empty lines, comment lines, and code lines.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to analyze, relative to the working directory.",
            },
        },
        "required": ["file_path"],
    },
}