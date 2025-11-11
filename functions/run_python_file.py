import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    """
    Run a Python file within a working directory.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the Python file within the working directory
        args (list): Additional arguments to pass to the Python file
        
    Returns:
        str: Execution result or error message
    """
    if args is None:
        args = []
    
    try:
        # Create the full path
        full_path = os.path.join(working_directory, file_path)
        
        # Get absolute paths for comparison
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        # Check if the path is within the working directory boundaries
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Check if the file exists
        if not os.path.exists(abs_full_path):
            return f'Error: File "{file_path}" not found.'
        
        # Check if the file ends with ".py"
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Execute the Python file
        try:
            # Combine the file path and arguments
            cmd = ["python", abs_full_path] + args
            
            # Run the subprocess with a 30-second timeout
            completed_process = subprocess.run(
                cmd,
                cwd=abs_working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                text=True
            )
            
            # Format the output
            result_lines = []
            
            # Add stdout if present
            if completed_process.stdout:
                result_lines.append(f"STDOUT: {completed_process.stdout}")
            else:
                result_lines.append("STDOUT: No output produced.")
            
            # Add stderr if present
            if completed_process.stderr:
                result_lines.append(f"STDERR: {completed_process.stderr}")
            
            # Add exit code if non-zero
            if completed_process.returncode != 0:
                result_lines.append(f"Process exited with code {completed_process.returncode}")
            
            return "\n".join(result_lines)
            
        except subprocess.TimeoutExpired:
            return "Error: Python execution timed out after 30 seconds"
        except Exception as e:
            return f"Error: executing Python file: {e}"
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_run_python_file = {
    "name": "run_python_file",
    "description": "Execute a Python file within the working directory with optional arguments.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the Python file to execute, relative to the working directory.",
            },
            "args": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Optional arguments to pass to the Python file.",
            },
        },
        "required": ["file_path"],
    },
}