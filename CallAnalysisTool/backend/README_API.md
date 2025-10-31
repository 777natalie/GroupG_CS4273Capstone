# Backend API - EMS Call Analysis Tool

Flask-based REST API for grading 911 EMS call transcripts.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd CallAnalysisTool/backend
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python api/app.py
```

Server will start on: **http://localhost:5001**

### 3. Test the API

```bash
# Health check
curl http://localhost:5001/api/health

# Grade a transcript
curl -X POST http://localhost:5001/api/grade \
  -H "Content-Type: application/json" \
  -d @tests/test_transcript.json
```

Or run the automated test script:
```bash
./tests/test_manual.sh
```

---

## 📡 API Endpoints

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

### Grade Transcript (Rule-Based)

```http
POST /api/grade
POST /api/grade/rule  (alias)
```

**Request Body** (Group B's JSON format):
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
  "grader_type": "rule_based",
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
    "grader_version": "1.0.0"
  }
}
```

---

### Grade Transcript (AI) - Coming Soon

```http
POST /api/grade/ai
```

**Status:** `501 Not Implemented`

This endpoint will integrate Jaiden's AI grader. Currently returns:
```json
{
  "error": "AI grading not yet implemented",
  "status": "coming_soon"
}
```

---

### Grade Transcript (All Graders) - Coming Soon

```http
POST /api/grade/all
```

**Status:** `501 Not Implemented`

This endpoint will run both rule-based and AI grading, returning comparison. Currently returns:
```json
{
  "error": "Combined grading not yet implemented",
  "status": "coming_soon"
}
```

---

## 📊 Grading Code Reference

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

## 🏗️ Project Structure

```
CallAnalysisTool/backend/
├── api/
│   ├── app.py                    # Flask application
│   ├── routes/
│   │   ├── health.py            # Health check endpoint
│   │   └── grading.py           # Grading endpoints
│   ├── services/
│   │   └── rule_grader.py       # Rule-based grading logic
│   └── models/
│       └── schemas.py           # Request/response models (future)
│
├── tests/
│   ├── test_transcript.json     # Sample transcript
│   └── test_manual.sh           # Manual testing script
│
├── requirements.txt             # Python dependencies
└── README_API.md               # This file
```

---

## 🔧 Configuration

### Rubric & Synonyms

The grader uses configuration files from `unitTests/`:
- `rubric.json` - Question labels
- `synonyms.json` - Phrase matching patterns

These files are automatically loaded when the server starts.

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

## 🧪 Testing

### Manual Testing

```bash
# Start the server
python api/app.py

# In another terminal, run tests
./tests/test_manual.sh
```

### With Postman/Insomnia

1. Import the test transcript: `tests/test_transcript.json`
2. POST to `http://localhost:5001/api/grade`
3. Set `Content-Type: application/json`
4. Paste transcript in body

### With Frontend

Update your frontend to call:
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

---

## 🚧 Future Integration

### Adding Jaiden's AI Grader

1. Import his `AIGrader.py` module
2. Update `api/services/` to include AI grader wrapper
3. Implement `/api/grade/ai` endpoint in `api/routes/grading.py`

### Adding Natalie's Nature Code Detector

1. Import her nature code detection module
2. Call it before grading to determine which questions to check
3. Update grading logic to use detected nature code

### Adding Database Storage

1. Add SQLAlchemy to `requirements.txt`
2. Create models in `api/models/`
3. Store grading results for history page

---

## 🐛 Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:
```bash
# Make sure you're in the backend directory
cd CallAnalysisTool/backend

# Set PYTHONPATH
export PYTHONPATH=.
```

### Port Already in Use

If port 5000 is busy:
```bash
# Kill the process
lsof -ti:5000 | xargs kill

# Or change the port in api/app.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

### CORS Errors

If frontend can't connect:
1. Check the browser console for specific error
2. Add your frontend URL to CORS origins in `api/app.py`
3. Restart the server

---

## 📝 Notes

- **Privacy:** All grading is done locally (no external API calls)
- **Group B Integration:** This API accepts their JSON transcript format
- **Extensible:** Easy to add AI graders, nature code detection, etc.

---

## 👥 Team

- **Kevin Nguyen** - Backend API, Rule-Based Grader
- **Jaiden Sizemore** - AI Grader (integration pending)
- **Natalie Roman** - Nature Code Detection (integration pending)
- **Camden Laskie** - Frontend Integration

---

## 📅 Next Steps

1. ✅ Test API locally
2. ⏳ Share with Camden for frontend integration
3. ⏳ Get Jaiden's AI grader format
4. ⏳ Get Natalie's nature code detector format
5. ⏳ Integrate AI + nature code detection
6. ⏳ Merge with Group B (Nov 7)

