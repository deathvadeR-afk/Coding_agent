#!/usr/bin/env python3
"""
Test suite for the Coding Assistant project
"""

import unittest
import os
import sys
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

class TestCodingAssistant(unittest.TestCase):
    
    def test_get_files_info(self):
        """Test that get_files_info returns file information"""
        # Test with current directory
        result = get_files_info(".", ".")
        self.assertIsInstance(result, str)
        # Check that it contains file information (using a more generic check)
        self.assertIn("file_size", result)
        
    def test_get_file_content(self):
        """Test that get_file_content can read a file"""
        # Test reading this test file
        result = get_file_content(".", "tests.py")
        self.assertIsInstance(result, str)
        self.assertIn("Test suite", result)

if __name__ == "__main__":
    unittest.main()