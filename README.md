# EMS Call Analysis Tool
## GroupG_CS4273Capstone

--- 

## Project Overview

This project is a continuation of the Group E Capstone project, designed to assist emergency dispatchers by analyzing EMS call transcripts and verifying if protocol questions were asked correctly.

The system uses:
- A **local LLM (Ollama)** for natural language understanding and querying,
- A **semantic search vector index** (FAISS) for fast protocol question retrieval,
- A **FastAPI backend** to process transcripts,
- A **React frontend** to upload transcripts and display analysis results.

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
- [Notes](#notes)
- [Team Contributions](#team-contributions)
- [Progress Plan](#progress-plan)

---

## Project Structure
   ```bash
/project-root
│
├── backend/                       # Backend API and analysis logic (Python)
│   ├── data/                     # Data and index storage
│   │   ├── EMS-Calltaking-QA.csv  # EMS Protocol CSV file with questions and protocols
│   │   └── db_indexing/           # FAISS vector index files (persisted search index)
│   │       ├── default_vector_store.json
│   │       ├── docstore.json
│   │       ├── graph_store.json
│   │       ├── image_vector_store.json
│   │       └── index_store.json
│   │
│   ├── schema/                   # Pydantic models for structured API responses
│   │   └── models.py             # Defines the data schema for NatureCode and Questions in analysis
│   │
│   ├── EMS_CallAnalyzer.py       # Main analyzer class: Loads data, indexes it, queries FAISS, and calls LLM
│   ├── local_llm.py              # Wrapper to run Ollama local LLM model via CLI calls
│   ├── api.py                   # FastAPI app with endpoints to accept transcript and return analysis
│   └── requirements.txt          # Python dependencies list for the backend
│
└── frontend/                     # React frontend UI
    ├── public/
    │   └── index.html            # Main HTML page hosting the React app
    │
    ├── src/
    │   ├── components/           # React components for UI
    │   │   ├── TranscriptUploader.jsx  # Uploads transcript files, submits to backend
    │   │   └── AnalysisResult.jsx       # Displays the analysis results returned from backend
    │   │
    │   ├── App.jsx               # Main React app component that renders uploader and result
    │   ├── index.js              # Entry point for React app, renders App to DOM
    │   └── api.js                # API helper for calling backend /analyze endpoint
    │
    ├── package.json              # Node package config with dependencies and scripts
    ├── package-lock.json         # Dependency lockfile
    └── README.md                 # Frontend README

```


## Setup Instructions

### Technologies Used

- Python 3.9+  
- Node.js 16+ and npm/yarn  
- [Ollama](https://ollama.com) installed and configured locally  
- Access to the EMS protocol CSV file (`EMS-Calltaking-QA.csv`)

---

### Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd backend
2. (Optional) Create and activate a Python virtual environment:
   ```bash
   python -m venv venv  
   source venv/bin/activate   # Linux/macOS  
   .\venv\Scripts\activate    # Windows
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt  
4. Make sure Ollama is installed and configured, then set your model in `local_llm.py`.
5. Run the FastAPI server:
   ```bash
   uvicorn api:app --reload

### Frontend Setup

1. Navigate to the frontend folder:
   ```bash
   cd frontend  
2. Install dependencies:
   ```bash
   npm install  
   # or  
   yarn install
3. Start the React development server:
   ```bash
   npm start  
   # or  
   yarn start
   ```
4. Open your browser at `http://localhost:3000`

## Key Feature
### Protocol Question Coverage Checker
**Goal**: Given a 911 call transcript and a set of required protocol questions for a selected nature code, the system checks which questions were asked, which were missed, and a simple confidence score for each match using token-overlap

### Example 
* Transcript: "911 what's is the address of the emergency? Are there any injuries?"

* Required:
  * 1. "What is the address of the emergency?"
    2. "Is anyone injured?"
    3. "Are there you in a safe location?"
* Output: `asked = [1,2]`, `missed = [3]`, `coverage = 0.67`

## Usage

1. Use the React frontend to upload EMS call transcripts.
2. The frontend sends transcripts to the backend API /analyze.
3. Backend queries the EMS protocol vector index and runs Ollama LLM locally for analysis.
4. Analysis results are returned and displayed on the frontend UI.

## How it Works

* EMS protocol data (CSV) is loaded and indexed with FAISS for semantic search.
* Transcripts are parsed and queried against this index for relevant questions.
* A local LLM (Ollama) processes the transcript and indexed data to determine protocol adherence.
* Responses follow the structured schema defined in models.py for consistent frontend display.

## Notes 

* Ollama provides a HIPAA-friendly, local LLM inference environment, no cloud dependency.
* The semantic vector index improves retrieval performance and relevance.
* This modular approach allows easy upgrades to the backend LLM or frontend UI independently.
  
## Team Contributions

| Name            | Role            | Contact                   |
| --------------- | --------------- | ------------------------- |
| Camden Laskie   | Project Manager | camdenlaskie@ou.edu       |
| Kevin Nguyen    | Sprint Master 1 | kevin.nguyen@ou.edu       |
| Jaiden Sizemore | Sprint Master 2 | jaiden.m.sizemore-1@ou.edu|
| Natalie Roman   | Sprint Master 3 | casandra.n.roman-1@ou.edu |

## Progress Plan



