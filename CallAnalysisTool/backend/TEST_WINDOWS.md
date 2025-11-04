# Testing on Windows (PowerShell)

## Prerequisites

1. Install Ollama from https://ollama.ai
2. Download the model:
```powershell
ollama pull llama3.1:8b
```
3. Install Python dependencies:
```powershell
cd CallAnalysisTool\backend
pip install -r requirements.txt
```

## Running the Server

### Terminal 1: Start Ollama
```powershell
ollama serve
```

### Terminal 2: Start Flask API
```powershell
cd CallAnalysisTool\backend
$env:PYTHONPATH = "."
python api/app.py
```

The server will start on http://localhost:5001

## Testing the API

### Terminal 3: Run Tests

#### Test 1: Health Check
```powershell
curl http://localhost:5001/api/health
```

#### Test 2: Grade a Transcript (AI with Nature Code Detection)
```powershell
curl -X POST http://localhost:5001/api/grade `
  -H "Content-Type: application/json" `
  -d "@tests/test_transcript.json"
```

#### Test 3: Rule-Based Grading (Backward Compatibility)
```powershell
curl -X POST http://localhost:5001/api/grade/rule `
  -H "Content-Type: application/json" `
  -d "@tests/test_transcript.json"
```

## Expected Response Format

```json
{
  "grader_type": "ai",
  "grade_percentage": 75.5,
  "detected_nature_code": "Falls",
  "total_questions": 20,
  "case_entry_questions": 5,
  "nature_code_questions": 15,
  "questions_asked_correctly": 15,
  "questions_missed": 5,
  "timestamp": "2025-11-04T20:00:00Z",
  "grades": {
    "CE_1": {
      "code": "1",
      "label": "What's the location of the emergency?",
      "status": "Asked Correctly"
    },
    "NC_3": {
      "code": "2",
      "label": "Did the patient fall from a height?",
      "status": "Not Asked"
    }
  },
  "metadata": {
    "language": "en",
    "segment_count": 10,
    "grader_version": "2.0.0",
    "model": "llama3.1:8b",
    "questions_source": "EMSQA.csv (Case Entry + Falls)",
    "nature_code_detection": "keyword + embedding model"
  }
}
```

## Troubleshooting

### Error: "Ollama connection failed"
- Make sure `ollama serve` is running in Terminal 1
- Check if model is downloaded: `ollama list`

### Error: "No module named 'api'"
- Ensure you're in the `backend/` directory
- Set PYTHONPATH: `$env:PYTHONPATH = "."`

### Error: "EMSQA.csv not found"
- Check that `CallAnalysisTool/backend/data/EMSQA.csv` exists
- Verify you're running from the correct directory

