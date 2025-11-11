import os
import subprocess

def git_status(working_directory, repo_path="."):
    """
    Check the git status of a repository.
    
    Args:
        working_directory (str): The base working directory
        repo_path (str): Relative path to the git repository within the working directory
        
    Returns:
        str: Git status output or error message
    """
    try:
        # Create the full path
        full_path = os.path.join(working_directory, repo_path)
        
        # Get absolute paths for comparison
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        # Check if the path is within the working directory boundaries
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot access "{repo_path}" as it is outside the permitted working directory'
        
        # Check if the path is a directory
        if not os.path.isdir(abs_full_path):
            return f'Error: "{repo_path}" is not a directory'
        
        # Check if it's a git repository
        git_dir = os.path.join(abs_full_path, '.git')
        if not os.path.exists(git_dir):
            return f'Error: "{repo_path}" is not a git repository'
        
        # Execute git status command
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=abs_full_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    return f'Git status for "{repo_path}":\n{result.stdout}'
                else:
                    return f'Git status for "{repo_path}": Working directory is clean'
            else:
                return f'Error running git status: {result.stderr}'
                
        except subprocess.TimeoutExpired:
            return "Error: Git command timed out"
        except FileNotFoundError:
            return "Error: Git is not installed or not in PATH"
        except Exception as e:
            return f"Error executing git status: {str(e)}"
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_git_status = {
    "name": "git_status",
    "description": "Check the git status of a repository to see modified, added, or deleted files.",
    "parameters": {
        "type": "object",
        "properties": {
            "repo_path": {
                "type": "string",
                "description": "The path to the git repository, relative to the working directory. Defaults to the current directory.",
            },
        },
    },
}