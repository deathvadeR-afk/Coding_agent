import os
import subprocess

def git_diff(working_directory, repo_path=".", commit1=None, commit2=None):
    """
    Show differences between commits or between working directory and index.
    
    Args:
        working_directory (str): The base working directory
        repo_path (str): Relative path to the git repository within the working directory
        commit1 (str): First commit hash (optional)
        commit2 (str): Second commit hash (optional)
        
    Returns:
        str: Git diff output or error message
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
        
        # Build git diff command
        cmd = ['git', 'diff']
        if commit1 and commit2:
            cmd.extend([commit1, commit2])
        elif commit1:
            cmd.append(commit1)
        # If no commits specified, diff shows changes in working directory
        
        # Execute git diff command
        try:
            result = subprocess.run(
                cmd,
                cwd=abs_full_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    return f'Git diff for "{repo_path}":\n{result.stdout}'
                else:
                    return f'Git diff for "{repo_path}": No differences found'
            else:
                return f'Error running git diff: {result.stderr}'
                
        except subprocess.TimeoutExpired:
            return "Error: Git diff command timed out"
        except FileNotFoundError:
            return "Error: Git is not installed or not in PATH"
        except Exception as e:
            return f"Error executing git diff: {str(e)}"
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_git_diff = {
    "name": "git_diff",
    "description": "Show differences between commits or between working directory and index in a git repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "repo_path": {
                "type": "string",
                "description": "The path to the git repository, relative to the working directory. Defaults to the current directory.",
            },
            "commit1": {
                "type": "string",
                "description": "First commit hash. If provided alone, shows changes since that commit.",
            },
            "commit2": {
                "type": "string",
                "description": "Second commit hash. Used with commit1 to show differences between two commits.",
            },
        },
    },
}