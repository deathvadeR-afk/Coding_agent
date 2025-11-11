# Coding Assist with Gemini - VS Code Extension

An AI-powered coding assistant extension for Visual Studio Code that uses Google's Gemini API to help you analyze code, find duplicates, and get AI-powered insights.

## Features

- **List Files**: View all files in your workspace with size information
- **Read File**: View the content of any file in your workspace
- **Ask AI**: Ask questions to the Gemini AI about your code or general programming questions
- **Analyze Code**: Get complexity analysis for your code files
- **Find Duplicates**: Identify duplicate code blocks in your files

## Requirements

- Visual Studio Code v1.74.0 or higher
- Python 3.12 or higher
- Google Gemini API key

## Installation

1. Clone this repository
2. Navigate to the `vscode-extension` directory
3. Run `npm install` to install dependencies
4. Press `F5` to compile and run the extension in a new Extension Development Host window

## Extension Settings

This extension contributes the following commands:

- `coding-assist-gemini.listFiles`: List all files in the workspace
- `coding-assist-gemini.readFile`: Read the content of a file (right-click on file in explorer)
- `coding-assist-gemini.askAI`: Ask a question to the AI
- `coding-assist-gemini.analyzeCode`: Analyze code complexity (right-click on file in explorer)
- `coding-assist-gemini.findDuplicates`: Find duplicate code blocks (right-click on file in explorer)

## Configuration

To use this extension, you need to set up your Google Gemini API key:

1. Create a `.env` file in your workspace root
2. Add your API key: `GEMINI_API_KEY=your_api_key_here`

## Known Issues

- The extension requires Python to be installed and accessible from the command line
- Large files may take longer to process

## Release Notes

### 0.1.0

Initial release of Coding Assist with Gemini extension