# EMS Call Analysis Tool
## GroupG_CS4273Capstone

---

## Project Overview

This project supports the Norman Police Department by reviewing EMS call transcripts to ensure dispatchers ask the correct protocol questions. It can be used for quality assurance, training, and improving call consistency.

We were provided with an Excel sheet containing the grading criteria that NPD currently uses, and our non‑AI grading approach is based directly on those rules. Transcripts are parsed and checked against this grading sheet to produce consistent, repeatable scoring.

The focus for now is on a rule‑based implementation to match dispatcher questions with required prompts. Once this foundation is stable, AI‑based grading will be layered on in a later sprint. The repository now includes a dedicated parser module and aligned API endpoints to support both the non‑AI and AI graders.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Technologies Used](#technologies-used)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Key Feature](#key-feature)
- [Usage](#usage)
- [How it Works](#how-it-works)
- [Branches & Modules](#branches--modules)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Branch-Specific Demos](#branch-specific-demos)
- [Notes](#notes)
- [Team Contributions](#team-contributions)
- [Progress Plan](#progress-plan)

---

## Project Structure

Consolidated view of the current code layout. Some folders live on feature branches and merge into `main`.

```bash
/CallAnalysisTool
│
├── backend/                         # Backend API and grading logic (Python/FastAPI)
│   ├── data/
│   │   └── EMS-Calltaking-QA.csv    # EMS protocol questions (source of truth for non-AI)
│   ├── schema/
│   │   └── models.py                # API models (legacy) / shared schemas
│   ├── app/
│   │   ├── grade_rule/              # Non-AI rule-based grading module
│   │   ├── grade_llm/               # AI grading module (local LLM via Ollama + embeddings)
│   │   ├── schemas/                 # Pydantic models for CallRecord and GraderResponse
│   │   └── main.py                  # FastAPI app entry (mounts /grade/rule and /grade/llm)
│   ├── EMS_CallAnalyzer.py          # Legacy non-AI analyzer (S1 baseline)
│   ├── api.py                       # Legacy API (/analyze) — maintained for backward compatibility
│   └── requirements.txt             # Backend dependencies
│
├── parser/                          # Transcript normalization into CallRecord schema
│   ├── normalize.py
│   ├── call_record_schema.py
│   ├── speakers.py
│   └── utils.py
│
├── tests/                           # Test suites (parser, rule grader, endpoints, llm smoke)
│   ├── parser/
│   ├── rule_grader/
│   ├── endpoints/
│   └── llm_grader/
│
└── frontend/                        # React/Next (Vite-compatible) frontend UI
    ├── src/
    │   ├── components/
    │   │   ├── TranscriptUploader.jsx
    │   │   └── AnalysisResult.jsx
    │   ├── pages/                   # Next.js pages (if applicable) or Vite routes
    │   ├── App.jsx
    │   ├── index.js
    │   └── api.js                   # API helper
    └── package.json
```

---

## Setup Instructions

### Technologies Used

* `Python 3.9+` – backend services and transcript processing
* `Node.js 16+` and npm/yarn – frontend tooling
* `React` – frontend web interface
* `Vite` or `Next.js` – frontend framework for dev server/routing
* `FastAPI` – backend framework for API handling
* `CSV protocols` – EMS protocol data reference
* `EMS Protocol CSV file (Police-Fire-EMS-Calltaking-QA-Forms)` – reference material for dispatcher protocols
* Optional: `Ollama + FAISS` for local AI grading (no cloud usage)

---

### Backend Setup

```bash
cd backend
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
pip install -r requirements.txt
# New endpoints
uvicorn app.main:app --reload
# If using the legacy baseline (S1)
# uvicorn api:app --reload
```

---

### Frontend Setup

```bash
cd frontend
npm install
# or
yarn install

# Vite
npm start
# or Next.js
npm run dev
# open http://localhost:3000
```

---

## Key Feature

### Protocol Question Coverage Checker
Given a 911 call transcript and a set of required protocol questions for a selected nature code, the system checks which questions were asked, which were missed, and provides a simple coverage score. The non‑AI grader is deterministic and traceable; the AI grader expands recall for paraphrases.

**Example**
- Transcript: “911 what’s the address of the emergency? Are there any injuries?”  
- Required:  
  1. “What is the address of the emergency?”  
  2. “Is anyone injured?”  
  3. “Are you in a safe location?”  
- Output: `asked = [1,2]`, `missed = [3]`, `coverage = 0.67`

---

## Usage

1. Upload EMS call transcripts through the frontend.
2. The frontend calls the backend API.
3. The backend compares transcripts against the EMS protocol CSV (non‑AI) and/or embeddings (AI).
4. Results are returned and displayed on the frontend.

---

## How it Works

* The Excel grading sheet provided by NPD is loaded as the reference for grading criteria (non‑AI).
* Parser: transcripts from Group B’s pipeline are normalized into a CallRecord schema (speaker tags, timestamps, confidence, audio quality).
* Rule‑based grader: token/intent patterns detect whether each protocol question was asked.
* AI grader: local LLM + embeddings (FAISS) improves paraphrase/intent detection; both graders share the same output schema.
* Frontend: displays asked/missed, rationales, and basic coverage/score.

---

## Branches & Modules

- **main** — stable trunk and project README; consolidates modules as they land.
- **transcript-parsing** — parser and schema for CallRecord; tests for normalization.
- **ai-model** — AI grading via Ollama + embeddings/FAISS; tests and configs for local inference.
- **unit-testing** — shared test harness and fixtures (parser, rule grader, endpoint contract, AI smoke).

Feature branches are merged into `main` via PRs as they stabilize.

---

## API Endpoints

- Legacy (S1)  
  - `POST /analyze` → asked/missed/coverage based on CSV rules.

- Current (S2)  
  - `POST /grade/rule` → non‑AI grading (deterministic, CSV‑driven).  
  - `POST /grade/llm`  → AI grading (local model; same response shape as `/grade/rule`).

---

## Testing

```bash
# Parser tests
pytest -q tests/parser

# Rule grader tests
pytest -q tests/rule_grader

# Endpoint contract tests (FastAPI running)
pytest -q tests/endpoints

# AI grader smoke/contract (if Ollama configured)
pytest -q tests/llm_grader -k "smoke or contract"
```

Focus areas: parser normalization edge cases, synonyms/reordering tolerance in the rule‑based grader, response contract shape, and LLM smoke where configured.

---

## Branch-Specific Demos

These steps match the files that exist in each branch snapshot in this repo.

### ai-model

What it shows
- `CallAnalysisTool/backend/test_case.py` runs a single transcript through the parser → rule grader (and AI if configured).
- Group B JSON sample and text fixtures are under `tests/sample_data/`.

Run once (dependencies)
```bash
cd CallAnalysisTool/backend
python -m venv venv
# mac/linux
source venv/bin/activate
# windows
# .\venv\Scripts\activate
pip install -r requirements.txt
cd ../..
```

Quick demo (positive text)
```bash
python CallAnalysisTool/backend/test_case.py \
  --transcript tests/sample_data/transcript_positive.txt \
  --required tests/sample_data/required_questions.json \
  --nature "BREATHING_PROBLEMS" \
  --mode text
```

Demo with real JSON transcript
```bash
python CallAnalysisTool/backend/test_case.py \
  --transcript "CallAnalysisTool/backend/transcriptions/2025_00015813_Falls_Shattell_transcription.json" \
  --required tests/sample_data/required_questions.json \
  --nature "FALLS" \
  --mode json --pretty
```

---

### transcript-parsing

What it shows
- Same single‑case runner at `CallAnalysisTool/backend/test_case.py`.
- Emphasize normalization into CallRecord: run with text and with Group B JSON.

Commands
```bash
# dependencies once (if not already done)
cd CallAnalysisTool/backend
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cd ../..

# text fixture
python CallAnalysisTool/backend/test_case.py \
  --transcript tests/sample_data/transcript_positive.txt \
  --required tests/sample_data/required_questions.json \
  --nature "BREATHING_PROBLEMS" \
  --mode text

# JSON fixture
python CallAnalysisTool/backend/test_case.py \
  --transcript "CallAnalysisTool/backend/transcriptions/2025_00015813_Falls_Shattell_transcription.json" \
  --required tests/sample_data/required_questions.json \
  --nature "FALLS" \
  --mode json --pretty
```

---

### unit-testing

What it shows
- Simple non‑AI test harness for Case Entry (Q1 → 2a) over a sample transcript.

Commands
```bash
cd unitTests
python3 test_case.py transcript_call.txt --show-evidence
```

Optional (use custom config files)
```bash
cd unitTests
python3 test_case.py transcript_call.txt --labels rubric.json --synonyms synonyms.json --show-evidence
```

Expected
- Prints asked/missed codes and short evidence snippets for the provided transcript.

---

### If imports or paths fail

From the repo root:
```bash
# mac/linux
export PYTHONPATH=.
# windows powershell
$env:PYTHONPATH="."
```

---

## Notes

### Future AI Integration
- Add a basic AI grading module to test against Norman PD demo data (local only).
- Expand natural language handling while keeping outputs explainable.
- Maintain on‑premise, privacy‑aware deployment (no cloud for PHI).

### Privacy
- Treat all 911 data as sensitive. Redact as needed. Use local inference only.

---

## Team Contributions

| Name            | Role                 | Contact                     |
| --------------- | -------------------- | --------------------------- |
| Camden Laskie   | Product Owner / UI   | camdenlaskie@ou.edu         |
| Kevin Nguyen    | SM1 / Rule Grader + Tests | kevin.nguyen@ou.edu    |
| Jaiden Sizemore | SM2 / Parser + AI    | jaiden.m.sizemore-1@ou.edu  |
| Natalie Roman   | SM3 / Docs + Protocols/CSV + AI selection | casandra.n.roman-1@ou.edu |

---

## Progress Plan

* September:
  * Have all members submit the proper documents for participation in the project.
  * Acquire grading guidelines.
  * Determine what needs to be finished on the frontend.
  * Lay out project structure in GitHub.

* October:
  * Identify and develop best method of integrating AI into the grading process.
  * Develop AI grading process and connect with Group B to handle transcription and grading simultaneously.
  * Build on frontend structure from previous group.

* November:
  * Polish and verify AI grading capabilities.
  * Add finishing touches to frontend (possibly working with group B by this point).
  * Attach Group B's transcription project to our grading project.
  * Ensure there are no errors when combining the projects.

* December:
  * Test final version, and fix any issues.
  * Present final product.
