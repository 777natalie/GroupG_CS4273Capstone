# Jaiden Sizemore
# CS4273 Group G
# Last Updated 10/16/2025

# Still very work in progress, functionality is limited and only for first 5 questions.

import sys
from JSONTranscriptionParser import json_to_text
import ollama

def ai_grade_transcript(transcript_text, questions_dict):
    """Let the AI handle all the grading logic automatically"""
    
    prompt = f"""
    You are a 911 call quality assurance analyst. Analyze this transcript and grade it based on the questions below.
    
    TRANSCRIPT:
    {transcript_text}
    
    GRADING QUESTIONS (use codes: 1=Asked Correctly, 2=Not Asked, 4=Not As Scripted, 5=N/A):
    {chr(10).join([f"{qid}: {question}" for qid, question in questions_dict.items()])}
    
    Return ONLY a JSON object with this exact format:
    {{
        "1": "1",
        "1a": "1", 
        "1b": "5",
        "2": "4",
        "2a": "2"
    }}
    """
    
    try:
        response = ollama.generate(model='llama3.1:8b', prompt=prompt)
        # Extract JSON from response
        import json
        import re
        
        # Find JSON in the response
        json_match = re.search(r'\{.*\}', response['response'], re.DOTALL)
        if json_match:
            grades = json.loads(json_match.group())
            return grades
        else:
            print("Could not parse AI response as JSON")
            return {}
            
    except Exception as e:
        print(f"AI grading failed: {e}")
        return {}

def main():
    # Your questions and grading scale
    questions = {
        "1": "What's the location of the emergency?",
        "1a": "Address/location confirmed/verified?",
        "1b": "911 CAD Dump used to build the call?",
        "2": "What's the phone number you're calling from?",
        "2a": "Phone number documented in the entry?",
    }
    
    KEY = {
        "1": "Asked Correctly",
        "2": "Not Asked",
        "4": "Not As Scripted", 
        "5": "N/A"
    }
    
    if len(sys.argv) < 2:
        print("Usage: python SimpleAIGrader.py <transcript.json>")
        sys.exit(1)
    
    # Get transcript
    transcript = json_to_text(sys.argv[1])
    
    # Let AI do all the work
    grades = ai_grade_transcript(transcript, questions)
    
    # Print results
    print("=== AI Grading Results ===")
    for qid, question in questions.items():
        code = grades.get(qid, "2")  # Default to "Not Asked"
        meaning = KEY.get(code, "Unknown")
        print(f"{qid}: {code} ({meaning}) - {question}")

if __name__ == "__main__":
    main()