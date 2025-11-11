import os
import subprocess

def git_commit(working_directory, repo_path, message, files=None):
    """
    Commit changes to a git repository.
    
    Args:
        working_directory (str): The base working directory
        repo_path (str): Relative path to the git repository within the working directory
        message (str): Commit message
        files (list): List of files to commit (optional, defaults to all staged files)
        
    Returns:
        str: Commit result or error message
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
        
        # If specific files are provided, add them
        if files:
            try:
                for file in files:
                    subprocess.run(
                        ['git', 'add', file],
                        cwd=abs_full_path,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        timeout=30
                    )
            except subprocess.TimeoutExpired:
                return "Error: Git add command timed out"
            except Exception as e:
                return f"Error adding files: {str(e)}"
        
        # Execute git commit command
        try:
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=abs_full_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return f'Git commit successful:\n{result.stdout}'
            else:
                return f'Error running git commit: {result.stderr}'
                
        except subprocess.TimeoutExpired:
            return "Error: Git commit command timed out"
        except FileNotFoundError:
            return "Error: Git is not installed or not in PATH"
        except Exception as e:
            return f"Error executing git commit: {str(e)}"
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_git_commit = {
    "name": "git_commit",
    "description": "Commit changes to a git repository with a specified message.",
    "parameters": {
        "type": "object",
        "properties": {
            "repo_path": {
                "type": "string",
                "description": "The path to the git repository, relative to the working directory.",
            },
            "message": {
                "type": "string",
                "description": "The commit message.",
            },
            "files": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of files to commit. If not provided, commits all staged files.",
            },
        },
        "required": ["repo_path", "message"],
    },
}