# Backend API - EMS Call Analysis Tool

Flask-based REST API for grading 911 EMS call transcripts using AI.

---

## Quick Start

### 1. Prerequisites

**Install Ollama** (required for AI grading):
```bash
# Visit https://ollama.ai to install Ollama
# Or on macOS:
brew install ollama

# Download the llama3.1:8b model
ollama pull llama3.1:8b

# Start Ollama server (in a separate terminal)
# If error occurs, Ollama is already running
ollama serve
```

### 2. Install Dependencies

**Mac/Linux:**
```bash
cd CallAnalysisTool/backend
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
cd CallAnalysisTool\backend
pip install -r requirements.txt
```

### 3. Run the Server

**Mac/Linux:**
```bash
cd CallAnalysisTool/backend
export PYTHONPATH=.
python api/app.py
```

**Windows (PowerShell):**
```powershell
cd CallAnalysisTool\backend
$env:PYTHONPATH = "."
python api/app.py
```

Server will start on: **http://localhost:5001**

### 4. Test the API

**Note:** Make sure you're in the `backend` directory:
```bash
cd CallAnalysisTool/backend
```

**Mac/Linux:**
```bash
# Health check
curl http://localhost:5001/api/health

# Grade a transcript 
curl -X POST http://localhost:5001/api/grade \
  -H "Content-Type: application/json" \
  -d @tests/test_transcript.json

# Test file upload 
curl -X POST http://localhost:5001/api/upload \
  -F "file=@tests/test_transcript.json"
```

**Windows (PowerShell):**
```powershell
# Health check
curl http://localhost:5001/api/health

# Grade a transcript (AI grading - JSON body)
curl -X POST http://localhost:5001/api/grade `
  -H "Content-Type: application/json" `
  -d "@tests/test_transcript.json"

# Test file upload (what frontend uses)
curl -X POST http://localhost:5001/api/upload `
  -F "file=@tests/test_transcript.json"
```

Or run the automated test script (Mac/Linux only):
```bash
./tests/test_manual.sh
```

---

## API Endpoints

### Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "EMS Call Analysis API",
  "version": "1.0.0"
}
```

---

### Grade Transcript 

```http
POST /api/grade
POST /api/grade/ai  (alias)
```

**Uses:** AI grader with Ollama (llama3.1:8b model)

**Request Body** (JSON):
```json
{
  "language": "en",
  "segments": [
    {
      "start": 0.0,
      "end": 5.0,
      "text": "Norman 911, what is the address of the emergency?",
      "speaker": "SPEAKER_01",
      "confidence": -0.29,
      "audio_quality": 0.737
    },
    {
      "start": 5.0,
      "end": 15.0,
      "text": "28, 17, Brompton Drive, Norman, Oklahoma.",
      "speaker": "SPEAKER_00",
      "confidence": -0.29,
      "audio_quality": 0.737
    }
  ]
}
```

**Query Parameters:**
- `?show_evidence=true` - Include evidence/matching segments in response

**Response:**
```json
{
  "grader_type": "ai",
  "timestamp": "2025-10-31T12:34:56Z",
  "grades": {
    "1": {
      "code": "1",
      "label": "What's the location of the emergency?",
      "status": "Asked Correctly"
    },
    "1a": {
      "code": "1",
      "label": "Address/location confirmed/verified?",
      "status": "Asked Correctly"
    },
    "1b": {
      "code": "2",
      "label": "911 CAD Dump used to build the call?",
      "status": "Not Asked"
    },
    "2": {
      "code": "1",
      "label": "What's the phone number you're calling from?",
      "status": "Asked Correctly"
    },
    "2a": {
      "code": "1",
      "label": "Phone number documented in the entry?",
      "status": "Asked Correctly"
    }
  },
  "metadata": {
    "language": "en",
    "segment_count": 5,
    "grader_version": "1.0.0",
    "model": "llama3.1:8b"
  }
}
```

**Error Response** (if Ollama not running):
```json
{
  "error": "Ollama connection failed",
  "message": "Please ensure Ollama is installed and running (ollama serve)",
  "details": "..."
}
```

---

### Upload and Grade File

```http
POST /api/upload
```

Upload a `.json` transcript file and get grading results.

**Uses:** AI grader with Ollama (llama3.1:8b model) + nature code detection

**Request:** `multipart/form-data`
```javascript
// Frontend example (TypeScript/React)
const formData = new FormData();
formData.append('file', jsonFile); // File object from <input type="file">

const response = await fetch('http://localhost:5001/api/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
```

**Response:**
```json
{
  "filename": "test_transcript.json",
  "grader_type": "ai",
  "grade_percentage": 56.2,
  "detected_nature_code": "Case Entry",
  "total_questions": 17,
  "case_entry_questions": 17,
  "nature_code_questions": 0,
  "questions_asked_correctly": 4,
  "questions_missed": 13,
  "timestamp": "2025-11-05T00:38:08.231106Z",
  "grades": {
    "CE_1": {
      "code": "1",
      "label": "What's the location of the emergency?",
      "status": "Asked Correctly"
    },
    "CE_2": {
      "code": "4",
      "label": "What's the phone number you're calling from?",
      "status": "Not As Scripted"
    }
  },
  "metadata": {
    "language": "en",
    "segment_count": 5,
    "grader_version": "2.0.0",
    "model": "llama3.1:8b",
    "questions_source": "EMSQA.csv (Case Entry + Case Entry)",
    "nature_code_detection": "keyword + embedding model"
  }
}
```

**Error Responses:**

No file provided:
```json
{
  "error": "No file provided"
}
```

Invalid file type:
```json
{
  "error": "Invalid file type",
  "message": "Only .json files are supported",
  "allowed_types": [".json"]
}
```

Invalid JSON structure:
```json
{
  "error": "Invalid transcript format: missing \"segments\" field"
}
```

---

## Grading Code Reference

| Code | Meaning             |
|------|---------------------|
| 1    | Asked Correctly     |
| 2    | Not Asked           |
| 3    | Asked Incorrectly   |
| 4    | Not As Scripted     |
| 5    | N/A                 |
| 6    | Obvious             |
| RC   | Recorded Correctly  |

---

## Project Structure

```
CallAnalysisTool/backend/
├── AIGrader.py                  # AI grader (Ollama + llama3.1:8b)
├── detect_naturecode.py         # Nature code detection
├── JSONTranscriptionParser.py   # Group B JSON format parser
├── nature_keywords.json         # Keywords for nature code detection
├── requirements.txt             # Python dependencies
├── README_API.md                # This file
│
├── api/
│   ├── app.py                   # Flask application
│   ├── routes/
│   │   ├── health.py            # Health check endpoint
│   │   └── grading.py           # Grading endpoints (/grade, /upload, /grade/rule)
│   └── services/
│       ├── ai_grader.py         # AI grader wrapper for Flask
│       ├── question_loader.py   # EMSQA.csv loader
│       └── rule_grader.py       # Rule-based grading (legacy)
│
├── data/
│   └── EMSQA.csv                # 296 EMS protocol questions
│
└── tests/
    ├── test_transcript.json     # Sample transcript
    └── test_manual.sh           # Manual testing script
```

---

## Configuration

### CORS

The API allows requests from:
- `http://localhost:3000` (Next.js)
- `http://localhost:5173` (Vite)
- `http://localhost:5174` (Vite alternate)

To add more origins, edit `api/app.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://your-frontend-url.com"]
    }
})
```

---

## Testing

### Manual Testing

**Make sure you're in the `backend` directory:**
```bash
cd CallAnalysisTool/backend
```

```bash
# Start the server (in one terminal)
export PYTHONPATH=.
python api/app.py

# In another terminal (also in backend directory), run tests
cd CallAnalysisTool/backend
./tests/test_manual.sh
```

### With Postman/Insomnia

1. Import the test transcript: `CallAnalysisTool/backend/tests/test_transcript.json`
2. POST to `http://localhost:5001/api/grade`
3. Set `Content-Type: application/json`
4. Paste transcript in body

**Or test file upload endpoint:**
1. POST to `http://localhost:5001/api/upload`
2. Set `Content-Type: multipart/form-data`
3. Add file field with `tests/test_transcript.json`

### With Frontend

**For JSON body (direct grading):**
```javascript
const response = await fetch('http://localhost:5001/api/grade', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(transcriptData)
});
const result = await response.json();
```

**For file upload (recommended):**
```javascript
const formData = new FormData();
formData.append('file', jsonFile); // File object from <input type="file">

const response = await fetch('http://localhost:5001/api/upload', {
  method: 'POST',
  body: formData
});
const result = await response.json();
```

---

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:
```bash
# Make sure you're in the backend directory
cd CallAnalysisTool/backend

# Set PYTHONPATH
export PYTHONPATH=.
```

### Port Already in Use

If port 5001 is busy:
```bash
# Kill the process (Mac/Linux)
lsof -ti:5001 | xargs kill

# Or change the port in api/app.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

**Windows (PowerShell):**
```powershell
# Find process using port 5001
netstat -ano | findstr :5001
# Kill using PID from above command
taskkill /PID <PID> /F
```

### CORS Errors

If frontend can't connect:
1. Check the browser console for specific error
2. Add your frontend URL to CORS origins in `api/app.py`
3. Restart the server

---

## Features

- AI-based grading using Ollama (llama3.1:8b)
- Nature code detection (keyword + text embeddings)
- Dynamic question loading from EMSQA.csv (296 protocol questions)
- CORS-enabled for frontend integration
- Local processing (no external API calls, privacy-compliant)
- Accepts Group B's JSON transcript format

---
