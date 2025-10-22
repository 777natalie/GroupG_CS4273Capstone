# Jaiden Sizemore
# CS4273 Group G
# Last Updated 10/21/2025: Added some basic tests

# Usage: python Test_AIGrader.py

import unittest
import sys
from unittest.mock import patch
from AIGrader import ai_grade_transcript

class TestAIGrader(unittest.TestCase):

    # Create example questions and transcript for test methods
    def setUp(self):
        self.questions = {
            "1": "What's the location of the emergency?",
            "1a": "Address/location confirmed/verified?",
            "1b": "911 CAD Dump used to build the call?", 
            "2": "What's the phone number you're calling from?",
            "2a": "Phone number documented in the entry?",
        }
        
        self.sample_transcript = """
        [00:00.0–00:05.0] SPEAKER_01: Norman 911, what is the address of the emergency?
        [00:05.0–00:15.0] SPEAKER_00: 123 Main Street in Norman Oklahoma
        [00:15.0–00:20.0] SPEAKER_01: What's the phone number you're calling from?
        [00:20.0–00:25.0] SPEAKER_00: 405-555-1234
        """

    # Test successful grading
    @patch('AIGrader.ollama.generate') # Use fake AI call for unit tests
    def test_successful_ai_grading(self, mock_ollama):
        # Create sample response
        mock_response = {
            'response': '{"1": "1", "1a": "1", "1b": "5", "2": "1", "2a": "1"}'
        }
        mock_ollama.return_value = mock_response
        
        # Call grading function from AIGrader.py
        grades = ai_grade_transcript(self.sample_transcript, self.questions)
        
        # Verify the AI was called
        mock_ollama.assert_called_once()
        
        # Verify the grades are correctly parsed
        self.assertEqual(grades["1"], "1")
        self.assertEqual(grades["1a"], "1")
        self.assertEqual(grades["1b"], "5")
        self.assertEqual(grades["2"], "1")
        self.assertEqual(grades["2a"], "1")

    # Test exception handling
    @patch('AIGrader.ollama.generate')
    def test_ai_grading_exception_handling(self, mock_ollama):
        # Make AI call trigger an exception
        mock_ollama.side_effect = Exception("AI service unavailable")
        
        grades = ai_grade_transcript(self.sample_transcript, self.questions)
        
        # Expected: empty dict
        self.assertEqual(grades, {})

# Method for running all tests and displaying results
def run_tests():
    # Load tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAIGrader)
    
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

# Driver
if __name__ == "__main__":
    print("Running AI Grader Unit Tests...")
    success = run_tests()
    
    if success:
        print("All tests passed!")
    else:
        print("Some tests failed!")
        sys.exit(1)