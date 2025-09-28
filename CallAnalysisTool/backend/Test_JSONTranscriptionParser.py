import unittest
import json
import os
import tempfile
import sys
from io import StringIO

# Import your function (assuming it's in JsonTranscription.py)
from JSONTranscriptionParser import json_to_text

class TestJSONTranscriptionParser(unittest.TestCase):
    
    def setUp(self):
        # Set up test fixtures before each test method
        self.test_data = {
            "language": "en",
            "lang_confidence": 0.98,
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    "text": " Test Message 1.",
                    "confidence": -0.29,
                    "audio_quality": 0.737,
                    "speaker": "SPEAKER_01"
                },
                {
                    "start": 5.0,
                    "end": 15.0,
                    "text": " Test Message 2.",
                    "confidence": -0.29,
                    "audio_quality": 0.737,
                    "speaker": "SPEAKER_00"
                },
                {
                    "start": 15.0,
                    "end": 18.0,
                    "text": " Test Message 3.",
                    "confidence": -0.29,
                    "audio_quality": 0.737,
                    "speaker": "SPEAKER_00"
                }
            ]
        }
    
    def create_temp_json_file(self, data):
        # Helper method to create temporary JSON file for testing
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(data, temp_file)
        temp_file.close()
        return temp_file.name
    
    def tearDown(self):
        # Clean up after each test method
        pass
    
    def test_basic_functionality(self):
        # Test that the parser works with valid JSON data
        temp_file = self.create_temp_json_file(self.test_data)
        try:
            result = json_to_text(temp_file)
            
            # Check that result is not empty
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            
            # Check that all segments are present
            lines = result.strip().split('\n')
            self.assertEqual(len(lines), 3)
            
            # Check format of each line
            for line in lines:
                self.assertIn('[', line)
                self.assertIn(']', line)
                self.assertIn(':', line)
                
        finally:
            os.unlink(temp_file)
    
    def test_timestamp_formatting(self):
        # Test that timestamps are formatted correctly as MM:SS
        temp_file = self.create_temp_json_file(self.test_data)
        try:
            result = json_to_text(temp_file)
            lines = result.strip().split('\n')
            
            # Check first line timestamp (0.0 seconds → 00:00)
            self.assertIn('[00:00]', lines[0])
            
            # Check second line timestamp (5.0 seconds → 00:05)
            self.assertIn('[00:05]', lines[1])
            
            # Check third line timestamp (15.0 seconds → 00:15)
            self.assertIn('[00:15]', lines[2])
            
        finally:
            os.unlink(temp_file)
    
    def test_speaker_formatting(self):
        # Test that speaker names are included correctly
        temp_file = self.create_temp_json_file(self.test_data)
        try:
            result = json_to_text(temp_file)
            lines = result.strip().split('\n')
            
            # Check speakers are present
            self.assertIn('[SPEAKER_01]', lines[0])
            self.assertIn('[SPEAKER_00]', lines[1])
            self.assertIn('[SPEAKER_00]', lines[2])
            
        finally:
            os.unlink(temp_file)
    
    def test_text_content(self):
        # Test that transcript text is properly included and trimmed
        temp_file = self.create_temp_json_file(self.test_data)
        try:
            result = json_to_text(temp_file)
            
            # Check that text content is present and whitespace is trimmed
            self.assertIn("Test Message 1.", result)
            self.assertIn("Test Message 2.", result)
            self.assertIn("Test Message 3.", result)
            
            # Check that leading/trailing whitespace is removed from text
            lines = result.strip().split('\n')
            self.assertFalse(lines[0].startswith(' '))  # No leading space before text
            
        finally:
            os.unlink(temp_file)
    
    def test_missing_segments(self):
        # Test behavior when segments key is missing
        invalid_data = {
            "language": "en",
            "lang_confidence": 0.98
            # Missing segments key
        }
        
        temp_file = self.create_temp_json_file(invalid_data)
        try:
            result = json_to_text(temp_file)
            self.assertEqual(result, "")  # Should return empty string
            
        finally:
            os.unlink(temp_file)
    
    def test_empty_segments(self):
        # Test behavior when segments array is empty
        empty_data = {
            "language": "en",
            "segments": []
        }
        
        temp_file = self.create_temp_json_file(empty_data)
        try:
            result = json_to_text(temp_file)
            self.assertEqual(result, "")  # Should return empty string
            
        finally:
            os.unlink(temp_file)
    
    def test_missing_optional_fields(self):
        # Test behavior when optional fields are missing
        partial_data = {
            "segments": [
                {
                    "start": 10.0,
                    "text": "Test message",
                    # Missing speaker, end, confidence, audio_quality
                }
            ]
        }
        
        temp_file = self.create_temp_json_file(partial_data)
        try:
            result = json_to_text(temp_file)
            
            # Should still work with default values
            self.assertIsNotNone(result)
            self.assertIn('[00:10]', result)
            self.assertIn('[UNKNOWN]', result)
            self.assertIn('Test message', result)
            
        finally:
            os.unlink(temp_file)
    
    def test_file_not_found(self):
        # Test behavior when file doesn't exist
        result = json_to_text('nonexistent_file.json')
        self.assertEqual(result, "")
    
    def test_invalid_json(self):
        # Test behavior with invalid JSON file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        temp_file.write("This is not valid JSON { invalid syntax ")
        temp_file.close()
        
        try:
            result = json_to_text(temp_file.name)
            self.assertEqual(result, "")  # Should return empty string
            
        finally:
            os.unlink(temp_file.name)
    
    def test_large_timestamps(self):
        # Test timestamp formatting with large values (minutes > 60)
        large_time_data = {
            "segments": [
                {
                    "start": 3661.0,  # 1 hour, 1 minute, 1 second
                    "end": 3665.0,
                    "text": "Test with large timestamp",
                    "speaker": "SPEAKER_01"
                }
            ]
        }
        
        temp_file = self.create_temp_json_file(large_time_data)
        try:
            result = json_to_text(temp_file)
            self.assertIn('[61:01]', result)  # 3661 seconds = 61 minutes, 1 second
            
        finally:
            os.unlink(temp_file)
    
    def test_special_characters_in_text(self):
        # Test handling of special characters in transcript text
        special_char_data = {
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    "text": "Message with special chars: @#$%^&*() and quotes \"'",
                    "speaker": "SPEAKER_01"
                }
            ]
        }
        
        temp_file = self.create_temp_json_file(special_char_data)
        try:
            result = json_to_text(temp_file)
            self.assertIn('Message with special chars: @#$%^&*() and quotes "\'', result)
            
        finally:
            os.unlink(temp_file)


class TestMainFunction(unittest.TestCase):
    # Tests for the main function and command line interface
    
    def setUp(self):
        self.original_argv = sys.argv
        self.original_stdout = sys.stdout
    
    def tearDown(self):
        sys.argv = self.original_argv
        sys.stdout = self.original_stdout


# Additional test for edge cases
class TestEdgeCases(unittest.TestCase):
    
    def test_very_short_timestamps(self):
        """Test sub-second timestamps"""
        short_time_data = {
            "segments": [
                {
                    "start": 0.5,
                    "end": 1.2,
                    "text": "Very short segment",
                    "speaker": "SPEAKER_01"
                }
            ]
        }
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(short_time_data, temp_file)
        temp_file.close()
        
        try:
            result = json_to_text(temp_file.name)
            self.assertIn('[00:00]', result)  # Should truncate to whole seconds
            
        finally:
            os.unlink(temp_file.name)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)