import os
import re

def regex_search(working_directory, file_path, pattern):
    """
    Search for a regex pattern in a file and return matching lines.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file within the working directory
        pattern (str): Regular expression pattern to search for
        
    Returns:
        str: Matching lines or error message
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
        
        # Compile the regex pattern
        try:
            regex = re.compile(pattern)
        except re.error as e:
            return f'Error: Invalid regex pattern "{pattern}": {str(e)}'
        
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
        
        # Search for matches
        matches = []
        for i, line in enumerate(lines, 1):
            if regex.search(line):
                matches.append(f"Line {i}: {line.rstrip()}")
        
        if matches:
            return f'Found {len(matches)} match(es) for pattern "{pattern}" in "{file_path}":\n' + '\n'.join(matches)
        else:
            return f'No matches found for pattern "{pattern}" in "{file_path}"'
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_regex_search = {
    "name": "regex_search",
    "description": "Search for a regex pattern in a file and return matching lines.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to search in, relative to the working directory.",
            },
            "pattern": {
                "type": "string",
                "description": "The regular expression pattern to search for.",
            },
        },
        "required": ["file_path", "pattern"],
    },
}