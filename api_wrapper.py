#!/usr/bin/env python3
"""
API wrapper for the Coding Assistant to be used by editor extensions
"""

import os
import sys
import json
from dotenv import load_dotenv
# pyright: reportMissingImports=false
import google.generativeai as genai
from google.generativeai import types

# Add the functions directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.search_replace import search_replace
from functions.git_status import git_status
from functions.code_complexity import code_complexity
from functions.find_duplicates import find_duplicates

class CodingAssistantAPI:
    def __init__(self, working_directory="."):
        """Initialize the API wrapper"""
        self.working_directory = working_directory
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-001')
        else:
            self.model = None
    
    def list_files(self, directory="."):
        """List files in a directory"""
        return get_files_info(self.working_directory, directory)
    
    def read_file(self, file_path):
        """Read the contents of a file"""
        return get_file_content(self.working_directory, file_path)
    
    def run_python(self, file_path, args=None):
        """Run a Python file"""
        if args is None:
            args = []
        return run_python_file(self.working_directory, file_path, args)
    
    def write_file_content(self, file_path, content):
        """Write content to a file"""
        return write_file(self.working_directory, file_path, content)
    
    def search_and_replace(self, file_path, search_text, replace_text):
        """Search and replace text in a file"""
        return search_replace(self.working_directory, file_path, search_text, replace_text)
    
    def get_git_status(self, repo_path="."):
        """Get git status of a repository"""
        return git_status(self.working_directory, repo_path)
    
    def analyze_complexity(self, file_path):
        """Analyze code complexity"""
        return code_complexity(self.working_directory, file_path)
    
    def find_duplicates(self, file_path, min_lines=3):
        """Find duplicate code blocks"""
        return find_duplicates(self.working_directory, file_path, min_lines)
    
    def ask_ai(self, prompt):
        """Ask the AI a question"""
        if not self.model:
            return "Error: Gemini API key not configured"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text if hasattr(response, 'text') else "No response from AI"
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"

# For testing the API
if __name__ == "__main__":
    api = CodingAssistantAPI()
    
    # Example usage
    print("Testing API wrapper...")
    print(api.list_files())
    print(api.ask_ai("What is 2+2?"))