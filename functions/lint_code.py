import os
import subprocess

def lint_code(working_directory, file_path=".", lint_command=None):
    """
    Run code linters on files.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Relative path to the file or directory within the working directory
        lint_command (str): Specific lint command to run (optional)
        
    Returns:
        str: Lint results or error message
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
        
        # Check if the path exists
        if not os.path.exists(abs_full_path):
            return f'Error: Path not found: "{file_path}"'
        
        # Determine the lint command to use
        if lint_command:
            # Use the provided lint command
            cmd = lint_command.split()
        else:
            # Auto-detect linting tool based on file type
            if os.path.isfile(abs_full_path) and abs_full_path.endswith('.py'):
                # Single Python file
                if os.path.exists(os.path.join(abs_working_dir, 'pyproject.toml')):
                    cmd = ['flake8', os.path.basename(abs_full_path)]
                    cwd = os.path.dirname(abs_full_path)
                else:
                    cmd = ['python', '-m', 'pylint', os.path.basename(abs_full_path)]
                    cwd = os.path.dirname(abs_full_path)
            elif os.path.isdir(abs_full_path):
                # Directory - use flake8 or pylint
                cwd = abs_full_path
                if os.path.exists(os.path.join(abs_full_path, 'pyproject.toml')):
                    cmd = ['flake8', '.']
                else:
                    cmd = ['python', '-m', 'pylint', '.']
            else:
                # Default to flake8 for general linting
                cmd = ['flake8', os.path.basename(abs_full_path) if os.path.isfile(abs_full_path) else '.']
                cwd = os.path.dirname(abs_full_path) if os.path.isfile(abs_full_path) else abs_full_path
        
        # Execute the lint command
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd if 'cwd' in locals() else abs_full_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60  # Longer timeout for linting
            )
            
            output = f"Lint results for '{file_path}':\n"
            output += f"Command: {' '.join(cmd)}\n"
            output += f"Exit code: {result.returncode}\n"
            
            if result.stdout.strip():
                output += f"STDOUT:\n{result.stdout}\n"
            if result.stderr.strip():
                output += f"STDERR:\n{result.stderr}\n"
            
            # If exit code is 0 and no output, code is clean
            if result.returncode == 0 and not result.stdout.strip() and not result.stderr.strip():
                output += "No linting issues found.\n"
            
            return output
                
        except subprocess.TimeoutExpired:
            return "Error: Linting timed out (exceeded 60 seconds)"
        except FileNotFoundError:
            return f"Error: Lint command not found: {' '.join(cmd)}. You may need to install flake8 or pylint."
        except Exception as e:
            return f"Error executing linting: {str(e)}"
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_lint_code = {
    "name": "lint_code",
    "description": "Run code linters on files or directories to check for code quality issues.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file or directory to lint, relative to the working directory. Defaults to the current directory.",
            },
            "lint_command": {
                "type": "string",
                "description": "Specific lint command to run (e.g., 'flake8 --max-line-length=100'). If not provided, auto-detects the appropriate linter.",
            },
        },
    },
}