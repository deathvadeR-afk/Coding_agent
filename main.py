import os
import sys
from dotenv import load_dotenv
# pyright: reportMissingImports=false
import google.generativeai as genai
from google.generativeai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from functions.search_replace import search_replace, schema_search_replace
from functions.delete_file import delete_file, schema_delete_file
from functions.create_directory import create_directory, schema_create_directory
from functions.regex_search import regex_search, schema_regex_search
from functions.git_status import git_status, schema_git_status
from functions.code_complexity import code_complexity, schema_code_complexity
from functions.find_duplicates import find_duplicates, schema_find_duplicates
from functions.git_commit import git_commit, schema_git_commit
from functions.git_diff import git_diff, schema_git_diff
from functions.git_log import git_log, schema_git_log
from functions.count_lines import count_lines, schema_count_lines
from functions.run_tests import run_tests, schema_run_tests
from functions.lint_code import lint_code, schema_lint_code
from functions.extract_function import extract_function, schema_extract_function
from functions.rename_symbol import rename_symbol, schema_rename_symbol
from functions.add_dependency import add_dependency, schema_add_dependency

# System prompt to instruct the LLM on how to use the functions
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

File System Operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
- Search and replace text in files
- Delete files
- Create directories
- Search for patterns using regular expressions

Git Operations:
- Check git status of repositories
- Commit changes with a message
- Show differences between commits
- View commit history

Code Analysis:
- Analyze code complexity
- Find duplicate code blocks
- Count lines of code in files

Testing:
- Execute test suites
- Run code linters

Refactoring:
- Extract code blocks into functions
- Rename variables, functions, or classes across files

Dependency Management:
- Add packages to requirements

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

Work iteratively using the available tools to accomplish the user's request. You can call multiple functions in sequence to gather information, analyze code, make changes, and verify your work.
"""

# Available functions for the LLM to use
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        schema_search_replace,
        schema_delete_file,
        schema_create_directory,
        schema_regex_search,
        schema_git_status,
        schema_code_complexity,
        schema_find_duplicates,
        schema_git_commit,
        schema_git_diff,
        schema_git_log,
        schema_count_lines,
        schema_run_tests,
        schema_lint_code,
        schema_extract_function,
        schema_rename_symbol,
        schema_add_dependency,
    ]
)

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
    
    # Configure the API
    genai.configure(api_key=api_key)

    if len(sys.argv) < 2:
        print("I need a prompt to generate content.")
        sys.exit(1)
    user_prompt = sys.argv[1]

    # Initialize the model with system instruction and tools
    model = genai.GenerativeModel(
        'gemini-2.0-flash-001',
        system_instruction=system_prompt,
        tools=[available_functions]
    )

    # Initialize conversation messages
    messages = [
        {
            "role": "user",
            "parts": [user_prompt]
        }
    ]

    # Loop to call the LLM repeatedly with a maximum of 5 iterations (to reduce API calls)
    max_iterations = 5
    for i in range(max_iterations):
        try:
            print(f"Iteration {i+1}")
            # Generate content with the entire conversation history
            response = model.generate_content(messages)
            
            # Add the model's response to the conversation
            if response.candidates and response.candidates[0].content:
                messages.append({
                    "role": "model",
                    "parts": [str(response.candidates[0].content)]
                })
            
            # Check if there's a text response (final answer)
            if hasattr(response, 'text') and response.text:
                print("Final response:")
                print(response.text)
                break
            
            # Check if there are function calls in the response
            function_called = False
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call = part.function_call
                        print(f"Calling function: {function_call.name}({function_call.args})")
                        function_called = True
                        
                        # Execute the function based on the call
                        result = None
                        if function_call.name == "get_files_info":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            directory = function_call.args.get("directory", ".")
                            result = get_files_info(working_directory, directory)
                            print(result)  # Print the result immediately
                        elif function_call.name == "get_file_content":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            result = get_file_content(working_directory, file_path)
                            print(result)  # Print the result immediately
                        elif function_call.name == "run_python_file":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            args = function_call.args.get("args", [])
                            result = run_python_file(working_directory, file_path, args)
                            print(result)  # Print the result immediately
                        elif function_call.name == "write_file":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            content = function_call.args.get("content")
                            result = write_file(working_directory, file_path, content)
                            print(result)  # Print the result immediately
                        elif function_call.name == "search_replace":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            search_text = function_call.args.get("search_text")
                            replace_text = function_call.args.get("replace_text")
                            result = search_replace(working_directory, file_path, search_text, replace_text)
                            print(result)  # Print the result immediately
                        elif function_call.name == "delete_file":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            result = delete_file(working_directory, file_path)
                            print(result)  # Print the result immediately
                        elif function_call.name == "create_directory":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            directory_path = function_call.args.get("directory_path")
                            result = create_directory(working_directory, directory_path)
                            print(result)  # Print the result immediately
                        elif function_call.name == "regex_search":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            pattern = function_call.args.get("pattern")
                            result = regex_search(working_directory, file_path, pattern)
                            print(result)  # Print the result immediately
                        elif function_call.name == "git_status":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            repo_path = function_call.args.get("repo_path", ".")
                            result = git_status(working_directory, repo_path)
                            print(result)  # Print the result immediately
                        elif function_call.name == "code_complexity":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            result = code_complexity(working_directory, file_path)
                            print(result)  # Print the result immediately
                        elif function_call.name == "find_duplicates":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            min_lines = function_call.args.get("min_lines", 3)
                            result = find_duplicates(working_directory, file_path, min_lines)
                            print(result)  # Print the result immediately
                        elif function_call.name == "git_commit":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            repo_path = function_call.args.get("repo_path")
                            message = function_call.args.get("message")
                            files = function_call.args.get("files")
                            result = git_commit(working_directory, repo_path, message, files)
                            print(result)  # Print the result immediately
                        elif function_call.name == "git_diff":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            repo_path = function_call.args.get("repo_path", ".")
                            commit1 = function_call.args.get("commit1")
                            commit2 = function_call.args.get("commit2")
                            result = git_diff(working_directory, repo_path, commit1, commit2)
                            print(result)  # Print the result immediately
                        elif function_call.name == "git_log":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            repo_path = function_call.args.get("repo_path", ".")
                            max_commits = function_call.args.get("max_commits", 10)
                            result = git_log(working_directory, repo_path, max_commits)
                            print(result)  # Print the result immediately
                        elif function_call.name == "count_lines":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            result = count_lines(working_directory, file_path)
                            print(result)  # Print the result immediately
                        elif function_call.name == "run_tests":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            test_path = function_call.args.get("test_path", ".")
                            test_command = function_call.args.get("test_command")
                            result = run_tests(working_directory, test_path, test_command)
                            print(result)  # Print the result immediately
                        elif function_call.name == "lint_code":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path", ".")
                            lint_command = function_call.args.get("lint_command")
                            result = lint_code(working_directory, file_path, lint_command)
                            print(result)  # Print the result immediately
                        elif function_call.name == "extract_function":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            function_name = function_call.args.get("function_name")
                            start_line = function_call.args.get("start_line")
                            end_line = function_call.args.get("end_line")
                            result = extract_function(working_directory, file_path, function_name, start_line, end_line)
                            print(result)  # Print the result immediately
                        elif function_call.name == "rename_symbol":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            file_path = function_call.args.get("file_path")
                            old_name = function_call.args.get("old_name")
                            new_name = function_call.args.get("new_name")
                            result = rename_symbol(working_directory, file_path, old_name, new_name)
                            print(result)  # Print the result immediately
                        elif function_call.name == "add_dependency":
                            # Hardcode the working directory for security
                            working_directory = "calculator"
                            package_name = function_call.args.get("package_name")
                            version = function_call.args.get("version")
                            result = add_dependency(working_directory, package_name, version)
                            print(result)  # Print the result immediately
                        
                        # Add the function result to the conversation
                        if result is not None:
                            messages.append({
                                "role": "user",
                                "parts": [f"Function result: {result}"]
                            })
            
            # If no function was called and no text response, break
            if not function_called and (not hasattr(response, 'text') or not response.text):
                print("No further actions or response generated.")
                break
                
        except Exception as e:
            # Check if this is a rate limit error and try to use OpenRouter as fallback
            if "429" in str(e) or "Resource exhausted" in str(e):
                print("Gemini API rate limit exceeded. To use OpenRouter as fallback, please implement the fallback mechanism.")
                print("Error details:", str(e))
            else:
                print(f"Error occurred: {e}")
                import traceback
                traceback.print_exc()
            break
    else:
        print("Reached maximum iterations without completing the task.")

if __name__ == "__main__":
    main()