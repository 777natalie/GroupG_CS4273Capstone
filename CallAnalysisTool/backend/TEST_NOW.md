# 🧪 Quick Testing Guide

## Step 1: Start Server (Terminal 1)

```bash
cd CallAnalysisTool/backend
./run.sh
```

**Keep this terminal running!** You should see:
```
✅ Starting Flask server...
* Running on http://127.0.0.1:5001
```

---

## Step 2: Test (Terminal 2 - NEW TERMINAL)

Open a **new terminal window** and run:

### Test 1: Health Check
```bash
curl http://localhost:5001/api/health
```

**Expected output:**
```json
{"status":"healthy","service":"EMS Call Analysis API","version":"1.0.0"}
```

---

### Test 2: Grade a Transcript
```bash
cd /Users/exfi8/Capstone/GroupG_CS4273Capstone/CallAnalysisTool/backend
curl -X POST http://localhost:5001/api/grade \
  -H "Content-Type: application/json" \
  -d @tests/test_transcript.json
```

**Expected output:** JSON with grading results for questions 1, 1a, 1b, 2, 2a

---

### Test 3: Grade with Evidence
```bash
curl -X POST "http://localhost:5001/api/grade?show_evidence=true" \
  -H "Content-Type: application/json" \
  -d @tests/test_transcript.json
```

**Expected output:** Same as Test 2, but includes `evidence` field showing which segments matched

---

### Or Run All Tests Automatically:

```bash
cd /Users/exfi8/Capstone/GroupG_CS4273Capstone/CallAnalysisTool/backend
./tests/test_manual.sh
```

This runs all tests and shows formatted JSON output.

---

## ✅ Success Looks Like:

```json
{
  "grader_type": "rule_based",
  "timestamp": "2025-10-31T...",
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
  }
}
```

---

## 🐛 Troubleshooting

**"Connection refused"**
→ Make sure server is running in Terminal 1

**"No such file or directory"**
→ Make sure you're in `CallAnalysisTool/backend` directory

**Empty response**
→ Check if server is actually running (look at Terminal 1)

