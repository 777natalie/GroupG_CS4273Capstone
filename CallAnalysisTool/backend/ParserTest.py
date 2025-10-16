# Test the JSON parser
from JSONTranscriptionParser import json_to_text
result = json_to_text(r"C:\Users\jaide\OneDrive\Documents\GroupG_CS4273Capstone\CallAnalysisTool\backend\transcriptions\2025_00015813_Falls_Shattell_transcription.json")
print("JSON Parser Result:")
print(result[:500] if result else "EMPTY RESULT")