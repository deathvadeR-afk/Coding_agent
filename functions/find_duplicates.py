import os
import re

def find_duplicates(working_directory, file_path, min_lines=3):
    """
    Find duplicate code blocks in a file.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file within the working directory
        min_lines (int): Minimum number of lines for a block to be considered
        
    Returns:
        str: Duplicate blocks found or error message
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
        
        # Find duplicate blocks
        duplicates = []
        line_count = len(lines)
        
        # Check each possible block
        for i in range(line_count - min_lines + 1):
            for j in range(i + 1, line_count - min_lines + 1):
                # Compare blocks of min_lines or more
                block1 = lines[i:i + min_lines]
                block2 = lines[j:j + min_lines]
                
                # If initial blocks match, check if longer blocks match
                if block1 == block2:
                    # Extend the block as long as lines match
                    length = min_lines
                    while (i + length < line_count and 
                           j + length < line_count and 
                           lines[i + length] == lines[j + length]):
                        length += 1
                    
                    # Only report if the block is at least min_lines long
                    if length >= min_lines:
                        block_content = ''.join(lines[i:i + length])
                        duplicates.append({
                            'line1': i + 1,
                            'line2': j + 1,
                            'length': length,
                            'content': block_content
                        })
        
        # Prepare result
        if duplicates:
            result = f"Found {len(duplicates)} duplicate code blocks in '{file_path}':\n"
            for i, dup in enumerate(duplicates[:5], 1):  # Limit to first 5 duplicates
                result += f"\nDuplicate {i}:\n"
                result += f"  Lines {dup['line1']}-{dup['line1'] + dup['length'] - 1} and {dup['line2']}-{dup['line2'] + dup['length'] - 1}\n"
                result += f"  Length: {dup['length']} lines\n"
                result += f"  Content:\n{dup['content']}\n"
            
            if len(duplicates) > 5:
                result += f"\n... and {len(duplicates) - 5} more duplicates\n"
        else:
            result = f"No duplicate code blocks (of {min_lines}+ lines) found in '{file_path}'"
        
        return result
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_find_duplicates = {
    "name": "find_duplicates",
    "description": "Find duplicate code blocks in a file to identify potential refactoring opportunities.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to analyze for duplicates, relative to the working directory.",
            },
            "min_lines": {
                "type": "integer",
                "description": "Minimum number of lines for a block to be considered a duplicate. Defaults to 3.",
            },
        },
        "required": ["file_path"],
    },
}