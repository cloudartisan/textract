#!/usr/bin/env python

"""
Unit tests for the textract module.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

import pytesseract
from PIL import Image

# Add parent directory to path to allow importing textract
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import textract


class TestTextract(unittest.TestCase):
    
    def setUp(self):
        # Get the absolute path to the test directory
        self.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')
    
    def test_find_tesseract(self):
        """Test that tesseract binary can be found."""
        tesseract_path = textract.find_tesseract()
        self.assertIsNotNone(tesseract_path, "Tesseract binary not found")
        self.assertTrue(os.path.isfile(tesseract_path), "Tesseract binary path is not a file")
    
    def test_extract_terraform_text(self):
        """Test extracting text from terraform_text.png"""
        # Set up test arguments
        test_args = MagicMock()
        test_args.source = textract.IMAGE
        test_args.infile = open(os.path.join(self.test_dir, 'terraform_text.png'), 'rb')
        test_args.enlarge = 1
        test_args.save = None
        test_args.outfile = MagicMock()
        
        # Mock the parse_args function to return our test args
        with patch('textract.parse_args', return_value=test_args):
            # Run the main function
            textract.main()
            
            # Check that outfile.write was called
            test_args.outfile.write.assert_called_once()
            
            # Get the text that was written
            text = test_args.outfile.write.call_args[0][0]
            
            # Verify text contains expected terraform output
            self.assertIn("execution plan", text.lower())
            self.assertIn("terraform", text.lower())
    
    def test_extract_percentage(self):
        """Test extracting text from 11_percent.png"""
        # Set up test arguments
        test_args = MagicMock()
        test_args.source = textract.IMAGE
        test_args.infile = open(os.path.join(self.test_dir, '11_percent.png'), 'rb')
        test_args.enlarge = 1
        test_args.save = None
        test_args.outfile = MagicMock()
        
        # Mock the parse_args function to return our test args
        with patch('textract.parse_args', return_value=test_args):
            # Run the main function
            textract.main()
            
            # Check that outfile.write was called
            test_args.outfile.write.assert_called_once()
            
            # Get the text that was written
            text = test_args.outfile.write.call_args[0][0]
            
            # Verify text contains expected percentage (allow for OCR variations)
            self.assertTrue("1%" in text or "11%" in text, 
                           f"Expected percentage not found in extracted text: '{text}'")


if __name__ == '__main__':
    unittest.main()