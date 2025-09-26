import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { UploadCloud } from "lucide-react";
import { useDropzone } from "react-dropzone";
import "./TranscriptUploadPage.css";
import api from "../../api.js";

export default function TranscriptUpload() {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [errorMessage, setErrorMessage] = useState("");
  const [file, setFile] = useState(null);
  const navigate = useNavigate(); // Hook for navigation
  const [isUploadingToApi, setIsUploadingToApi] = useState(false); // To disable button during API call

  // Function to handle file upload of only allowed types and simulate upload progress
  const handleFileUpload = (selectedFile) => {
    if (!selectedFile) return;

    const allowedTypes = ["application/json"];
    if (!allowedTypes.includes(selectedFile.type)) {
      setErrorMessage("Unsupported file type. Please upload a .json file.");
      return;
    }
    //console.log(selectedFile.type)
    setErrorMessage("");
    setFile(selectedFile);
    setUploadProgress(0);

    // Simulating upload progress
    let progress = 0;
    const interval = setInterval(() => {
      progress += 20;
      setUploadProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
        fetchQAResults(selectedFile); // Call API for JSON files
      }
    }, 500);
  };

  const fetchQAResults = async (fileToSend) => {
    setIsUploadingToApi(true);
    try {
      const formData = new FormData();
      formData.append("file", fileToSend); // 'file' should match the parameter name in your FastAPI endpoint

      const response = await api.post("http://localhost:8000/uploadfile", formData, {
        headers: {
          "Content-Type": "multipart/form-data", 
        },
      });

      //console.log("API Response:", response.data);
      setIsUploadingToApi(false);
              
      // Navigate to results page after completion
      navigate("/results", { state: response.data });
    } catch (error) {
      console.error("API Error:", error);
      setIsUploadingToApi(false);
      setErrorMessage("Failed to upload and process the file.");
    }
  };

  // Hook for handling file drop
  const { getRootProps, getInputProps } = useDropzone({
    accept: { "application/json": [".json"] },
    onDrop: (acceptedFiles) => handleFileUpload(acceptedFiles[0]),
  });

  return (
    <div className="transcript-upload-container">
      <div className="upload-box">
        <h1 className="upload-title">Upload Call Transcript</h1>
        <div {...getRootProps()} className="upload-area">
          <input {...getInputProps()} />
          <UploadCloud className="upload-icon" size={40} />
          <p className="upload-text">Drag and drop a transcript file here, or click to select a file</p>
        </div>
        <p className="upload-formats">Supported formats: .json</p>
        {file && !isUploadingToApi && <p className="upload-success">Selected: {file.name}</p>}
        {file && isUploadingToApi && <p className="upload-progress">Uploading: {file.name}...</p>}
        {errorMessage && <p className="upload-error">{errorMessage}</p>}
        <button className="upload-button" onClick={() => document.querySelector('input[type=file]').click()}
          disabled={isUploadingToApi}>
          Select File
        </button>
      </div>
    </div>
  );
}
