# EMS Call Analysis API - Quick Start

## Prerequisites

**1. Install Ollama (required for AI grading):**
```bash
# Visit https://ollama.ai or install via Homebrew (macOS)
brew install ollama

# Download the llama3.1:8b model
ollama pull llama3.1:8b

# Start Ollama server (keep running in a terminal)
ollama serve
```

## Run the API

**Terminal 1 - Start Ollama:**
```bash
ollama serve
```

**Terminal 2 - Start API Server:**
```bash
cd CallAnalysisTool/backend
./run.sh
# Or manually:
# pip install -r requirements.txt
# python api/app.py
```

## Test the API

**Terminal 3 - Run tests:**
```bash
cd CallAnalysisTool/backend

# Test health 
# Verifies: Server is running, routes are registered, basic HTTP response works
curl http://localhost:5001/api/health 

# Test AI Grading 
# Verifies: POST requests accepted, JSON parsing works, AI grader calls Ollama,
# transcript converted to text format, AI returns structured grades
curl -X POST http://localhost:5001/api/grade \
  -H "Content-Type: application/json" \
  -d @tests/test_transcript.json

# Test Rule-Based Grading (legacy)
curl -X POST http://localhost:5001/api/grade/rule \
  -H "Content-Type: application/json" \
  -d @tests/test_transcript.json

# To run all manual API tests:
./tests/test_manual.sh
```

## Troubleshooting

**"Ollama connection failed":**
- Make sure Ollama is running: `ollama serve`
- Check if model is downloaded: `ollama list` (should show llama3.1:8b)
- If not downloaded: `ollama pull llama3.1:8b`

**"Module not found":**
```bash
export PYTHONPATH=.
python api/app.py
```

**Scripts not executable:**
```bash
chmod +x run.sh
chmod +x tests/test_manual.sh
```
