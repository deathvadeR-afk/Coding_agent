import os

def add_dependency(working_directory, package_name, version=None):
    """
    Add packages to requirements or pyproject.toml.
    
    Args:
        working_directory (str): The base working directory
        package_name (str): Name of the package to add
        version (str): Version constraint (optional)
        
    Returns:
        str: Success message or error message
    """
    try:
        # Get absolute paths for comparison
        abs_working_dir = os.path.abspath(working_directory)
        
        # Check if working directory is valid
        if not os.path.isdir(abs_working_dir):
            return f'Error: Working directory not found: "{working_directory}"'
        
        # Determine which dependency file to use
        pyproject_path = os.path.join(abs_working_dir, 'pyproject.toml')
        requirements_path = os.path.join(abs_working_dir, 'requirements.txt')
        
        # Format the dependency string
        if version:
            dependency = f"{package_name}=={version}" if not version.startswith(('>', '<', '=', '~', '^')) else f"{package_name}{version}"
        else:
            dependency = package_name
        
        if os.path.exists(pyproject_path):
            # Add to pyproject.toml
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                # Find the dependencies section
                dependencies_start = -1
                for i, line in enumerate(lines):
                    if line.strip() == '[project.dependencies]' or '[project]' in line:
                        dependencies_start = i
                        break
                
                if dependencies_start == -1:
                    # Add dependencies section if it doesn't exist
                    lines.append('\n[project.dependencies]\n')
                    dependencies_start = len(lines) - 1
                
                # Find where to insert the new dependency
                insert_pos = dependencies_start + 1
                for i in range(dependencies_start + 1, len(lines)):
                    if lines[i].strip() == '' or lines[i].startswith('['):
                        break
                    insert_pos = i + 1
                
                # Insert the new dependency
                lines.insert(insert_pos, f'    "{dependency}",\n')
                
                # Write back to file
                with open(pyproject_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                
                return f'Successfully added "{dependency}" to pyproject.toml'
                
            except Exception as e:
                return f'Error updating pyproject.toml: {str(e)}'
        
        elif os.path.exists(requirements_path):
            # Add to requirements.txt
            try:
                with open(requirements_path, "a", encoding="utf-8") as f:
                    f.write(f'{dependency}\n')
                return f'Successfully added "{dependency}" to requirements.txt'
                
            except Exception as e:
                return f'Error updating requirements.txt: {str(e)}'
        
        else:
            # Create requirements.txt if neither file exists
            try:
                with open(requirements_path, "w", encoding="utf-8") as f:
                    f.write(f'{dependency}\n')
                return f'Successfully created requirements.txt with "{dependency}"'
                
            except Exception as e:
                return f'Error creating requirements.txt: {str(e)}'
            
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

# Function declaration schema for LLM
schema_add_dependency = {
    "name": "add_dependency",
    "description": "Add packages to requirements.txt or pyproject.toml dependency files.",
    "parameters": {
        "type": "object",
        "properties": {
            "package_name": {
                "type": "string",
                "description": "Name of the package to add as a dependency.",
            },
            "version": {
                "type": "string",
                "description": "Version constraint for the package (e.g., '1.2.3', '>=1.0.0', '~>2.0'). If not provided, uses the latest version.",
            },
        },
        "required": ["package_name"],
    },
}