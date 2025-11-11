import os
import subprocess

def run_tests(working_directory, test_path=".", test_command=None):
    """
    Execute test suites in a directory.
    
    Args:
        working_directory (str): The base working directory
        test_path (str): Relative path to the test directory or file within the working directory
        test_command (str): Specific test command to run (optional)
        
    Returns:
        str: Test results or error message
    """
    try:
        # Create the full path
        full_path = os.path.join(working_directory, test_path)
        
        # Get absolute paths for comparison
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        # Check if the path is within the working directory boundaries
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot access "{test_path}" as it is outside the permitted working directory'
        
        # Check if the path exists
        if not os.path.exists(abs_full_path):
            return f'Error: Path not found: "{test_path}"'
        
        # Determine the test command to use
        if test_command:
            # Use the provided test command
            cmd = test_command.split()
        else:
            # Auto-detect test framework
            if os.path.isfile(abs_full_path) and abs_full_path.endswith('.py'):
                # Single test file
                cmd = ['python', os.path.basename(abs_full_path)]
                cwd = os.path.dirname(abs_full_path)
            elif os.path.isdir(abs_full_path):
                # Test directory - look for common test patterns
                cwd = abs_full_path
                if os.path.exists(os.path.join(abs_full_path, 'pytest.ini')) or \
                   os.path.exists(os.path.join(abs_full_path, 'pyproject.toml')):
                    cmd = ['pytest']
                elif os.path.exists(os.path.join(abs_full_path, 'tests.py')) or \
                     os.path.exists(os.path.join(abs_full_path, 'test')):
                    cmd = ['python', '-m', 'unittest', 'discover']
                else:
                    cmd = ['python', '-m', 'unittest', 'discover']
            else:
                return f'Error: Unsupported test path: "{test_path}"'
        
        # Execute the test command
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd if 'cwd' in locals() else abs_full_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60  # Longer timeout for tests
            )
            
            output = f"Test execution results for '{test_path}':\n"
            output += f"Command: {' '.join(cmd)}\n"
            output += f"Exit code: {result.returncode}\n"
            
            if result.stdout.strip():
                output += f"STDOUT:\n{result.stdout}\n"
            if result.stderr.strip():
                output += f"STDERR:\n{result.stderr}\n"
            
            return output
                
        except subprocess.TimeoutExpired:
            return "Error: Test execution timed out (exceeded 60 seconds)"
        except FileNotFoundError:
            return f"Error: Test command not found: {' '.join(cmd)}"
        except Exception as e:
            return f"Error executing tests: {str(e)}"
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_run_tests = {
    "name": "run_tests",
    "description": "Execute test suites in a directory or run a specific test file.",
    "parameters": {
        "type": "object",
        "properties": {
            "test_path": {
                "type": "string",
                "description": "The path to the test directory or file, relative to the working directory. Defaults to the current directory.",
            },
            "test_command": {
                "type": "string",
                "description": "Specific test command to run (e.g., 'pytest -v'). If not provided, auto-detects the test framework.",
            },
        },
    },
}