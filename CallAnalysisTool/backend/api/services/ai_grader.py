"""
AI-based grading service
Wraps Jaiden's AIGrader.py to work with the Flask API
"""

import json
import tempfile
from typing import Dict, Any
from pathlib import Path
import sys
import os

# Add the services directory to path so Jaiden's imports work
sys.path.insert(0, str(Path(__file__).parent))

# Import Jaiden's code
import JSONTranscriptionParser
import AIGrader

class AIGraderService:
    """
    AI-based transcript grader using Ollama (llama3.1:8b model)
    Based on Jaiden's AIGrader.py
    """
    
    # Grading code meanings
    KEY = {
        "1": "Asked Correctly",
        "2": "Not Asked",
        "3": "Asked Incorrectly",
        "4": "Not As Scripted",
        "5": "N/A",
        "6": "Obvious",
        "RC": "Recorded Correctly"
    }
    
    def __init__(self, questions: Dict[str, str] = None):
        """
        Initialize AI grader with questions
        
        Args:
            questions: Dict mapping question_id to question_text
                      If None, uses default 5 questions
        """
        if questions is None:
            # Default to basic Case Entry questions for backward compatibility
            self.questions = {
                "1": "What's the location of the emergency?",
                "1a": "Address/location confirmed/verified?",
                "1b": "911 CAD Dump used to build the call?",
                "2": "What's the phone number you're calling from?",
                "2a": "Phone number documented in the entry?",
            }
        else:
            self.questions = questions
    
    def grade_transcript(self, transcript_data: Dict[str, Any], show_evidence: bool = False) -> Dict[str, Any]:
        """
        Grade a transcript using AI
        
        Args:
            transcript_data: Group B's JSON format with 'segments' array
            show_evidence: Whether to include evidence (not used by AI grader currently)
        
        Returns:
            Dict of grades with structure:
            {
                "1": {"code": "1", "label": "...", "status": "Asked Correctly"},
                ...
            }
        """
        # Jaiden's json_to_text expects a file path, so we need to create a temp file
        # This keeps their code unchanged
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump(transcript_data, tmp)
            tmp_path = tmp.name
        
        try:
            # Convert JSON to text format using Jaiden's parser
            transcript_text = JSONTranscriptionParser.json_to_text(tmp_path)
            
            if not transcript_text:
                raise ValueError("Failed to parse transcript data")
            
            # Get grades from AI using Jaiden's grader
            ai_grades = AIGrader.ai_grade_transcript(transcript_text, self.questions)
            
            if not ai_grades:
                raise RuntimeError("AI grading failed - empty response from Ollama")
            
            # Format grades to match API response structure
            formatted_grades = {}
            for q_id, question_text in self.questions.items():
                code = ai_grades.get(q_id, "2")  # Default to "Not Asked" if missing
                formatted_grades[q_id] = {
                    "code": code,
                    "label": question_text,
                    "status": self.KEY.get(code, "Unknown")
                }
            
            return formatted_grades
        
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def calculate_percentage(self, grades: Dict[str, Any]) -> float:
        """
        Calculate grade percentage based on questions asked correctly
        
        Args:
            grades: Dict of grades from grade_transcript()
        
        Returns:
            Percentage score (0.0 - 100.0)
        """
        if not grades:
            return 0.0
        
        total_questions = len(grades)
        
        # Count questions with code "1" (Asked Correctly) or "6" (Obvious)
        questions_correct = sum(
            1 for grade in grades.values() 
            if grade.get('code') in ['1', '6']
        )
        
        # Calculate percentage
        percentage = (questions_correct / total_questions) * 100
        return round(percentage, 1)

