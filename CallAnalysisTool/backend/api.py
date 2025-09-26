# Need post for sending the transcript (txt file) to our model
# Need get for retriveing results of model and sending to user
# Rate limiting (may be necessary)

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from EMS_CallAnalyzer import EMSCallAnalyzer
import json

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:5173", # port frontend is running at
    "http://localhost:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/uploadfile")
async def upload_file_and_retrieve_results(file: UploadFile):
    # Reads the JSON file for transcript parsing
    json_data = json.load(file.file)

    analyzer = EMSCallAnalyzer()
    response = analyzer.analyze_call(json_data)
    #print(json_data.get("call_transcript", {}).get("caller", {}))
    return response

    