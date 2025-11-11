# Coding Assist with Gemini

An AI-powered coding assistant that uses Google's Gemini API to interact with codebases, analyze files, and perform coding tasks autonomously.

## Project Overview

This project implements an AI agent that can:
- List files and directories in a codebase
- Read file contents
- Execute Python files
- Write or modify files
- Work iteratively to accomplish complex programming tasks
- Manage Git repositories
- Analyze code quality and complexity
- Run tests and linting
- Perform automated refactoring
- Manage project dependencies

The agent uses Google's Generative AI (Gemini) API to make decisions and perform actions based on user requests.

## Project Structure

```
├── calculator/                 # Sample calculator application
│   ├── pkg/                    # Calculator core modules
│   │   ├── calculator.py       # Core calculation logic with operator precedence
│   │   └── render.py           # JSON output formatting
│   ├── main.py                 # Calculator entry point
│   └── tests.py                # Calculator tests
├── functions/                  # AI agent tool implementations
│   ├── config.py               # Configuration settings
│   ├── get_files_info.py       # List directory contents
│   ├── get_file_content.py     # Read file contents
│   ├── run_python_file.py      # Execute Python scripts
│   ├── write_file.py           # Write/modify files
│   ├── search_replace.py       # Search and replace text in files
│   ├── delete_file.py          # Delete files
│   ├── create_directory.py     # Create directories
│   ├── regex_search.py         # Search for patterns using regular expressions
│   ├── git_status.py           # Check git repository status
│   ├── git_commit.py           # Commit changes to git repository
│   ├── git_diff.py             # Show differences between commits
│   ├── git_log.py              # View commit history
│   ├── code_complexity.py      # Analyze code complexity
│   ├── find_duplicates.py      # Find duplicate code blocks
│   ├── count_lines.py          # Count lines of code in files
│   ├── run_tests.py            # Execute test suites
│   ├── lint_code.py            # Run code linters
│   ├── extract_function.py     # Extract code blocks into functions
│   ├── rename_symbol.py        # Rename variables, functions, or classes
│   └── add_dependency.py       # Add packages to requirements
├── main.py                     # Main AI agent implementation
└── pyproject.toml              # Project dependencies and metadata
```

## Features

### AI Agent Capabilities
- **File System Operations**: List directories, read files, write files, search/replace, delete files, create directories, regex search
- **Code Execution**: Run Python scripts with argument passing
- **Iterative Problem Solving**: Multi-step task completion with feedback loops
- **Function Calling**: Integration with Google's Gemini function calling API
- **Git Operations**: Status, commit, diff, and log operations
- **Code Analysis**: Complexity analysis, duplicate detection, line counting
- **Testing Tools**: Run tests and linting
- **Refactoring Tools**: Extract functions, rename symbols
- **Dependency Management**: Add packages to requirements

### Calculator Application
- Mathematical expression evaluation with proper operator precedence
- JSON output formatting
- Command-line interface

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   or if using uv:
   ```bash
   uv pip install -e .
   ```

2. **Environment Variables**:
   Create a `.env` file with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

## Usage

### Running the AI Agent
```bash
python main.py "your request here"
```

Example requests:
- "List files in the calculator directory"
- "Read the contents of calculator/main.py"
- "Fix the bug: 3 + 7 * 2 shouldn't be 20"
- "Show me the git status"
- "Run tests in the calculator directory"
- "Analyze the complexity of calculator/pkg/calculator.py"

### Running the Calculator
```bash
python calculator/main.py "mathematical expression"
```

Example:
```bash
python calculator/main.py "3 + 7 * 2"
```

## AI Agent Tools

The AI agent has access to the following tools:

### File System Tools
1. **get_files_info**: Lists files in a directory with sizes
2. **get_file_content**: Reads the contents of a file
3. **run_python_file**: Executes a Python script
4. **write_file**: Writes content to a file
5. **search_replace**: Search for text in a file and replace it
6. **delete_file**: Delete a file
7. **create_directory**: Create a directory
8. **regex_search**: Search for patterns using regular expressions

### Git Tools
9. **git_status**: Check the git status of a repository
10. **git_commit**: Commit changes with a message
11. **git_diff**: Show differences between commits
12. **git_log**: View commit history

### Code Analysis Tools
13. **code_complexity**: Analyze code complexity metrics
14. **find_duplicates**: Identify duplicate code blocks
15. **count_lines**: Count lines of code in files

### Testing Tools
16. **run_tests**: Execute test suites
17. **lint_code**: Run code linters

### Refactoring Tools
18. **extract_function**: Extract code blocks into functions
19. **rename_symbol**: Rename variables, functions, or classes

### Dependency Management Tools
20. **add_dependency**: Add packages to requirements

## Implementation Details

### Agent Architecture
- Uses Google Generative AI (Gemini) API for decision making
- Implements a feedback loop for iterative task completion
- Maintains conversation history for context awareness
- Enforces security boundaries by restricting file operations to working directories
- Supports fallback to OpenRouter API when Gemini rate limits are exceeded

### Security Features
- All file operations are constrained to specific working directories
- Path validation prevents directory traversal attacks
- File size limits for content reading
- Working directory boundaries enforced for all operations

### Dual API Support
- Primary: Google's Gemini API
- Fallback: OpenRouter API with kwaipilot/kat-coder-pro:free model
- Automatic switching when rate limits are encountered

## Dependencies

- `google-generativeai==0.8.5`: Google's Generative AI SDK
- `python-dotenv==1.1.0`: Environment variable management
- `openai==1.54.0`: OpenAI SDK for OpenRouter API access

## Development

### Adding New Tools
1. Create a new function in the `functions/` directory
2. Add a function schema declaration
3. Register the function in `main.py`
4. Update the system prompt to inform the LLM about the new capability

### Testing
Run tests with:
```bash
python tests.py
```