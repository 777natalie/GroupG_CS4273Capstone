# Jaiden Sizemore
# CS4273 Group G
# Last Updated 10/20/2025: Updated comments

# Still work in progress, functionality is limited and only for first 5 questions.

# Requires installation of ollama from ollama.ai
# Ensure ollama is on your PATH
# Download the model we are using: ollama pull llama3.1:8b
# Usage: python AIGrader.py <path\transcript.json>

import sys
import pandas as pd
from JSONTranscriptionParser import json_to_text
from detect_naturecode import run_detection
import ollama

def extract_all_nature_codes(text):
    nature_codes = []
    lines = text.strip().split('\n')
    
    for i, line in enumerate(lines):
        if line.strip().startswith('- '):
            nature_code = line.strip()[2:].split(' (')[0]
            
            if i + 2 < len(lines):
                confidence_line = lines[i + 2].strip()
                if confidence_line.startswith('Confidence:'):
                    try:
                        confidence = float(confidence_line.split(': ')[1])
                        nature_codes.append((nature_code, confidence))
                    except (IndexError, ValueError):
                        continue
    
    # Sort by confidence (highest first)
    nature_codes.sort(key=lambda x: x[1], reverse=True)
    return nature_codes

def load_nature_code_questions(nature_code):
    # Load questions for a specific Nature Code from EMSQA.csv
    try:
        df = pd.read_csv("data/EMSQA.csv")
        # Filter questions for the specific Nature Code
        nature_questions = df[df['NatureCode'] == nature_code]
        
        # Create questions dictionary with Question_ID as key and Question_Text as value
        questions_dict = {}
        for _, row in nature_questions.iterrows():
            qid = str(row['Question_ID'])  # Ensure string type for consistency
            question_text = row['Question_Text']
            if pd.notna(question_text):  # Only add if question text is not NaN
                questions_dict[qid] = question_text
            
        return questions_dict
    except FileNotFoundError:
        print(f"Error: EMSQA.csv file not found in data/ directory")
        return {}
    except Exception as e:
        print(f"Error loading questions for Nature Code {nature_code}: {e}")
        return {}

# Function for grading a transcript using ollama's AI

# Input: Plain text transcription for grading and list of questions to be asked
# Output AI's grade for the given transcription based on given questions
def ai_grade_transcript(transcript_text, questions_dict, nature_code):
    # Prompt for the AI
    # NOTE: asking for a JSON submission is more reliable than plain text because the model is familiar with the format
    # Therefore, we are more likely to receive coherent grades in JSON format rather than a paragraph
    prompt = f"""
    You are a 911 call quality assurance analyst. Analyze this transcript and grade it based on the questions from the given nature code below.
    
    NATURE_CODE:
    {nature_code}

    TRANSCRIPT:
    {transcript_text}
    
    GRADING QUESTIONS (use codes: 1=Asked Correctly, 2=Not Asked, 4=Not As Scripted, 5=N/A):
    {chr(10).join([f"{qid}: {question}" for qid, question in questions_dict.items()])}
    
    Return ONLY a JSON object with this format:
    {{
        "1": "1",
        "1a": "1", 
        "1b": "5",
        "2": "4",
        "2a": "2"
    }}

    Note that the left hand side is for the question ID and the right hand side is for the grade.  Add as many entries as needed to satisfy the required grading.

    Important grading guidelines:
    - Use code "1" only if the question was asked exactly as scripted
    - Use code "2" if the question was not asked at all
    - Use code "4" if the question was asked but with different wording
    - Use code "5" only for questions that are clearly not applicable to this specific call
    - Be very strict in your assessment, it is important that questions are asked exactly as stated in the guidelines.
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
        print("Usage: python AIGrader.py <transcript.json>")
        sys.exit(1)
    
    # Get transcript as text
    transcript = json_to_text(sys.argv[1])
    if not transcript:
        print(f"Error: Could not load transcript")
        sys.exit(1)

    nature_codes_path = run_detection(transcript)
    if not nature_codes_path:
        print(f"Error: Could not determine nature codes")
        sys.exit(1)

    with open(nature_codes_path, "r") as codefile:
        nature_code_txt = codefile.read()

    nature_codes = extract_all_nature_codes(nature_code_txt)

    primary_nature_code = nature_codes[0][0]

    print(primary_nature_code)

    questions = load_nature_code_questions(primary_nature_code)
    if not questions:
        print(f"Error: Could not determine questions")
        sys.exit(1)
    
    # Get grades from AI
    grades = ai_grade_transcript(transcript, questions, primary_nature_code)
    
    # Print results
    print("=== AI Grading Results ===")
    for qid, question in questions.items():
        code = grades.get(qid, "2")  # Default to "Not Asked" if qid is unrecognized
        meaning = KEY.get(code, "Unknown") # Default to unknown if code is unrecognized
        print(f"{qid}: {code} ({meaning}) - {question}")

# Driver
if __name__ == "__main__":
    main()