# Jaiden Sizemore
# CS4273 Group G
# Last Updated 10/21/2025: Altered comments for clarity

# Usage: python Test_JSONTranscriptionParser.py

import unittest
import json
import os
import tempfile
import sys
from JSONTranscriptionParser import json_to_text

class TestJSONTranscriptionParser(unittest.TestCase):

    # Create an example JSON file for each test method
    def setUp(self):
        self.test_data = {
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    "speaker": "SPEAKER_01",
                    "text": "Norman 911, what is the address of the emergency?"
                },
                {
                    "start": 5.0,
                    "end": 15.0,
                    "speaker": "SPEAKER_00",
                    "text": "123 Main Street in Norman Oklahoma"
                },
                {
                    "start": 65.5,
                    "end": 70.2,
                    "speaker": "SPEAKER_01",
                    "text": "Is the patient breathing?"
                }
            ]
        }

    # Helper method for creating temp JSON files
    def create_temp_json_file(self, data):
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) # Create temp JSON file without auto-deleting
        json.dump(data, temp_file) # Write given data
        temp_file.close() # Close file
        return temp_file.name # Return temp file path

    # Test JSON parser with valid data
    def test_basic_parsing(self):
        temp_file = self.create_temp_json_file(self.test_data) # Get temp file

        # Attempt tests
        try:
            result = json_to_text(temp_file) # Parse JSON into text
            
            # Ensure result is nonempty
            self.assertIsNotNone(result)
            self.assertGreater(len(result), 0)
            
            # Check if each segment is in result
            self.assertIn("SPEAKER_01", result)
            self.assertIn("SPEAKER_00", result)
            self.assertIn("Norman 911", result)
            self.assertIn("123 Main Street", result)
            self.assertIn("Is the patient breathing?", result)
            
            # Check timestamp formatting
            self.assertIn("[00:00.0–00:05.0] SPEAKER_01:", result)
            self.assertIn("[00:05.0–00:15.0] SPEAKER_00:", result)
            self.assertIn("[01:05.5–01:10.2] SPEAKER_01:", result)
            
        finally:
            os.unlink(temp_file) # Delete temp file

    # Test handling of missing entries in JSON
    def test_missing_fields(self):
        test_data = {
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    # speaker missing
                    "text": "Test message"
                },
                {
                    "start": 5.0,
                    # end missing
                    "speaker": "SPEAKER_00",
                    "text": "Another message"
                },
                {
                    # start missing
                    "end": 10.0,
                    "speaker": "SPEAKER_01",
                    "text": "Third message"
                },
                {
                    "start": 10.0,
                    "end": 15.0,
                    "speaker": "SPEAKER_01"
                    # text missing
                }
            ]
        }
        
        temp_file = self.create_temp_json_file(test_data) # Temp file with missing entries

        # Attempt tests
        try:
            result = json_to_text(temp_file) # Parse
            
            # Expected to use default values for missing entries
            self.assertIn("UNKNOWN", result)           # Default speaker
            
            # Other default entries should be present anyway, but
            # we can test other messages to ensure errors don't compound
            self.assertIn("Test message", result)      
            self.assertIn("Another message", result)
            self.assertIn("Third message", result)
            
        finally:
            os.unlink(temp_file) # Delete temp

    # Test handling of empty segments
    def test_empty_segments(self):
        test_data = {
            "segments": []
        }
        
        temp_file = self.create_temp_json_file(test_data)

        # Attempt test
        try:
            result = json_to_text(temp_file)
            
            # Expected: empty string
            self.assertEqual(result, "")
            
        finally:
            os.unlink(temp_file)

    # Test non-existent file handling
    def test_file_not_found(self):
        result = json_to_text("fake_file.json")
        # Expected: empty string
        self.assertEqual(result, "")

    # Test invalid JSON format
    def test_invalid_json(self):
        # Create JSON with invalid format
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        temp_file.write("This is not valid JSON {")
        temp_file.close()
        
        # Attempt test
        try:
            result = json_to_text(temp_file.name)
            # Expected: empty string
            self.assertEqual(result, "")
        finally:
            os.unlink(temp_file.name)

    # Test valid JSON without segments
    def test_missing_segments_key(self):
        # Valid JSON without segments identifier
        test_data = {
            "start": 0.0,
            "end": 5.0,
            "speaker": "SPEAKER_01"
        }
        
        temp_file = self.create_temp_json_file(test_data)

        # Attempt test
        try:
            result = json_to_text(temp_file)
            # Expected: empty string
            self.assertEqual(result, "")
        finally:
            os.unlink(temp_file)

    # Test whitespace handling
    def test_whitespace_handling(self):
        """Test that whitespace in text is properly handled"""
        test_data = {
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    "speaker": "SPEAKER_01",
                    "text": "  Message with extra spaces  "
                }
            ]
        }
        
        temp_file = self.create_temp_json_file(test_data)

        # Attempt test
        try:
            result = json_to_text(temp_file)
            # Expected: whitespace removed with .strip()
            self.assertIn("Message with extra spaces", result)
            self.assertNotIn("  Message with extra spaces  ", result)
        finally:
            os.unlink(temp_file)

# Method for running all tests and displaying results
def run_tests():
    # Load tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestJSONTranscriptionParser)
    
    # Run tests, store result
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Output results
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"{'='*50}")
    
    return result.wasSuccessful()

# Driver for running tests
if __name__ == "__main__":
    print("Running JSON Transcription Parser Unit Tests...")
    success = run_tests()
    
    if success:
        print("All tests passed!")
    else:
        print("Some tests failed!")
        sys.exit(1)