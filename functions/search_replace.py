import os
import re

def search_replace(working_directory, file_path, search_text, replace_text):
    """
    Search for text in a file and replace it with new text.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file within the working directory
        search_text (str): Text to search for
        replace_text (str): Text to replace with
        
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
        
        # Perform search and replace
        if search_text in content:
            new_content = content.replace(search_text, replace_text)
            occurrences = content.count(search_text)
            
            # Write the updated content back to the file
            try:
                with open(abs_full_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                return f'Successfully replaced {occurrences} occurrence(s) of "{search_text}" with "{replace_text}" in "{file_path}"'
            except PermissionError:
                return f'Error: Permission denied to write to "{file_path}"'
            except OSError as e:
                return f'Error: Unable to write to "{file_path}": {str(e)}'
        else:
            return f'No occurrences of "{search_text}" found in "{file_path}"'
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_search_replace = {
    "name": "search_replace",
    "description": "Search for text in a file and replace it with new text.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to modify, relative to the working directory.",
            },
            "search_text": {
                "type": "string",
                "description": "The text to search for in the file.",
            },
            "replace_text": {
                "type": "string",
                "description": "The text to replace the search text with.",
            },
        },
        "required": ["file_path", "search_text", "replace_text"],
    },
}