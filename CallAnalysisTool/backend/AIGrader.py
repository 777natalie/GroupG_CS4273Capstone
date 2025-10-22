# Jaiden Sizemore
# CS4273 Group G
# Last Updated 10/20/2025: Updated comments

# Still work in progress, functionality is limited and only for first 5 questions.

# Requires installation of ollama from ollama.ai
# Ensure ollama is on your PATH
# Download the model we are using: ollama pull llama3.1:8b
# Run the model as follows: python AIGrader.py <path\transcript.json>

import sys
from JSONTranscriptionParser import json_to_text
import ollama

# Function for grading a transcript using ollama's AI

# Input: Plain text transcription for grading and list of questions to be asked
# Output AI's grade for the given transcription based on given questions
def ai_grade_transcript(transcript_text, questions_dict):
    # Prompt for the AI
    # NOTE: asking for a JSON submission is more reliable than plain text because the model is familiar with the format
    # Therefore, we are more likely to receive coherent grades in JSON format rather than a paragraph
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
            # If unable to access grades in json, send error message
            print("Could not parse AI response as JSON")
            return {}
            
    except Exception as e:
        print(f"AI grading failed: {e}")
        return {}

def main():
    # List of questions that need to be asked
    questions = {
        "1": "What's the location of the emergency?",
        "1a": "Address/location confirmed/verified?",
        "1b": "911 CAD Dump used to build the call?",
        "2": "What's the phone number you're calling from?",
        "2a": "Phone number documented in the entry?",
    }
    
    # Key for grading the transcription
    KEY = {
        "1": "Asked Correctly",
        "2": "Not Asked",
        "3": "Asked Incorrectly",
        "4": "Not As Scripted", 
        "5": "N/A"
    }
    
    # Check if file was provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python SimpleAIGrader.py <transcript.json>")
        sys.exit(1)
    
    # Get transcript as text
    transcript = json_to_text(sys.argv[1])
    
    # Get grades from AI
    grades = ai_grade_transcript(transcript, questions)
    
    # Print results
    print("=== AI Grading Results ===")
    for qid, question in questions.items():
        code = grades.get(qid, "2")  # Default to "Not Asked" if qid is unrecognized
        meaning = KEY.get(code, "Unknown") # Default to unknown if code is unrecognized
        print(f"{qid}: {code} ({meaning}) - {question}")

# Driver
if __name__ == "__main__":
    main()