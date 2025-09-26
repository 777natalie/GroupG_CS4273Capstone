# EMS Call Analysis Tool
## GroupG_CS4273Capstone

--- 

## Project Overview

This project supports the Norman Police Department by reviewing EMS call transcripts to ensure dispatchers ask the correct protocol questions. It can be used for quality assurance, training, and improving call consistency.

We were provided with an Excel sheet containing the grading criteria that NPD currently uses, and our non-AI grading approach is based directly on those rules. Transcripts are parsed and checked against this grading sheet to produce consistent, repeatable scoring.

The focus for now is on a rule-based implementation to match dispatcher questions with required prompts. Once this foundation is stable, AI-based grading will be layered on in a later sprint.

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
/CallAnalysisTool
│
├── backend/                       # Backend API and grading logic (Python)
│   ├── data/                     
│   │   └── EMS-Calltaking-QA.csv  # EMS protocol questions
│   │
│   ├── schema/                   # Models for API responses
│   │   └── models.py
│   │
│   ├── EMS_CallAnalyzer.py       # Rule-based transcript analyzer
│   ├── api.py                    # FastAPI app with /analyze endpoint
│   └── requirements.txt          # Backend dependencies
│
└── frontend/                     # React frontend UI
    ├── src/
    │   ├── components/
    │   │   ├── TranscriptUploader.jsx  # Upload transcripts
    │   │   └── AnalysisResult.jsx      # Display grading results
    │   ├── App.jsx
    │   ├── index.js
    │   └── api.js                # API helper
    └── package.json


```


## Setup Instructions

### Technologies Used

* `Python 3.9+` – backend services and transcript processing
* `Node.js 16+` and npm/yarn – frontend tooling
* `React` – frontend web interface
* `Vite` – React framework for routing
* `FastAPI` – backend framework for API handling
* `CSV protocols` – EMS protocol data reference
* `EMS Protocol CSV file (Police-Fire-EMS-Calltaking-QA-Forms)` – reference material for dispatcher protocols

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

1. Upload EMS call transcripts through the React frontend.
2. Transcripts are sent to the backend API.
3. The backend compares transcripts against the EMS protocol CSV.
4. Results are returned and displayed on the frontend.

## How it Works

* The Excel grading sheet provided by NPD is loaded as the reference for grading criteria.
* Each transcript is parsed line by line and compared against the required questions from the sheet.
* A matching algorithm (keyword/token overlap) determines which protocol questions were asked, which were missed, and assigns points based on the NPD rubric.
* Results are packaged into a structured API response (via models.py) and returned to the frontend for display.

## Notes 
### Future AI Integration
- Once the non-AI version is stable, the team plans to add:
    - A basic AI grading module to test against Norman PD demo data.
    - More advanced natural language techniques for transcript understanding.
    - Secure, on-premise deployment to maintain data privacy.
  
## Team Contributions

| Name            | Role            | Contact                   |
| --------------- | --------------- | ------------------------- |
| Camden Laskie   | Project Manager | camdenlaskie@ou.edu       |
| Kevin Nguyen    | Sprint Master 1 | kevin.nguyen@ou.edu       |
| Jaiden Sizemore | Sprint Master 2 | jaiden.m.sizemore-1@ou.edu|
| Natalie Roman   | Sprint Master 3 | casandra.n.roman-1@ou.edu |

## Progress Plan

* September:
  * Have all members submit the proper documents for participation in the project.
  * Acquire grading guidelines.
  * Determine what needs to finished on frontend
  * Layout project structure in GitHub.

* October:
  * Identify and develop best method of integrating AI into the grading process.
  * Develop AI grading process and connect with group B to handle transcription and grading simoultaneously
  * Build on frontend structure from previous group.

* November:
  * Polish and verify AI grading capabilities.
  * Add finishing touches to frontend (possibly working with group B by this point).
  * Attach group B's transcription project to our grading project.
  * Ensure there are no errors when combining the projects.

* December:
  * Test final version, and fix any issues.
  * Present final product.
