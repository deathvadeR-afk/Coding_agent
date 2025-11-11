import os
import subprocess

def git_log(working_directory, repo_path=".", max_commits=10):
    """
    View commit history of a git repository.
    
    Args:
        working_directory (str): The base working directory
        repo_path (str): Relative path to the git repository within the working directory
        max_commits (int): Maximum number of commits to show (default: 10)
        
    Returns:
        str: Git log output or error message
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
        
        # Execute git log command
        try:
            result = subprocess.run(
                ['git', 'log', f'--oneline', f'-n', str(max_commits)],
                cwd=abs_full_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    return f'Git log for "{repo_path}" (last {max_commits} commits):\n{result.stdout}'
                else:
                    return f'Git log for "{repo_path}": No commits found'
            else:
                return f'Error running git log: {result.stderr}'
                
        except subprocess.TimeoutExpired:
            return "Error: Git log command timed out"
        except FileNotFoundError:
            return "Error: Git is not installed or not in PATH"
        except Exception as e:
            return f"Error executing git log: {str(e)}"
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_git_log = {
    "name": "git_log",
    "description": "View commit history of a git repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "repo_path": {
                "type": "string",
                "description": "The path to the git repository, relative to the working directory. Defaults to the current directory.",
            },
            "max_commits": {
                "type": "integer",
                "description": "Maximum number of commits to show. Defaults to 10.",
            },
        },
    },
}