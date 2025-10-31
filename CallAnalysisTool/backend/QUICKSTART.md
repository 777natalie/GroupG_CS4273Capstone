### DEMO ###

```bash
cd CallAnalysisTool/backend
./run.sh
```

# --------------------- #
# (In another terminal) #
# --------------------- #

# Test health
curl http://localhost:5001/api/health

# Test Grading:
curl -X POST http://localhost:5001/api/grade \
  -H "Content-Type: application/json" \
  -d @tests/test_transcript.json

# To run all manual API tests:
./tests/test_manual.sh
```

# If you need to make scripts executable:
chmod +x run.sh
chmod +x tests/test_manual.sh

# If you hit "Module not found":
export PYTHONPATH=.
python api/app.py
