"use client";
import React, { useState, useRef } from "react";
import { Dispatcher } from "@/types/dispatcher";
import { v4 as uuidv4 } from "uuid";

const UploadFileContainer = () => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Define allowed audio file types
  const allowedTypes = [".zip", ".json"];

  const handleFileSelect = (files: FileList | null) => {
    if (!files) return;

    const validFiles: File[] = [];
    const invalidFiles: string[] = [];

    Array.from(files).forEach((file) => {
      const fileExtension = "." + file.name.split(".").pop()?.toLowerCase();
      if (allowedTypes.includes(fileExtension)) {
        validFiles.push(file);
      } else {
        invalidFiles.push(file.name);
      }
    });

    if (invalidFiles.length > 0) {
      alert(
        `The following files are not supported: ${invalidFiles.join(
          ", "
        )}\n\nOnly ${allowedTypes.join(", ")} files are allowed.`
      );
    }

    setSelectedFiles((prev) => [...prev, ...validFiles]);
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files);
    }
  };

  const removeFile = (index: number) => {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const handleUpload = () => {
    if (selectedFiles.length === 0) {
      alert("Please select at least one zip and json file to upload.");
      return;
    }

    // Group files by dispatcher name
    const dispatcherMap = new Map<
      string,
      { transcriptFiles: File[]; audioFiles: File[] }
    >();

    selectedFiles.forEach((file) => {
      const filename = file.name;
      const firstUnderscoreIndex = filename.indexOf("_");
      const secondUnderscoreIndex = filename.indexOf(
        "_",
        firstUnderscoreIndex + 1
      );
      const dotIndex = filename.indexOf(".");

      if (secondUnderscoreIndex !== -1 && dotIndex !== -1) {
        const dispatcherName = filename.substring(
          secondUnderscoreIndex + 1,
          dotIndex
        );
        const fileExtension = filename.substring(dotIndex);

        // Initialize dispatcher if not exists
        if (!dispatcherMap.has(dispatcherName)) {
          dispatcherMap.set(dispatcherName, {
            transcriptFiles: [],
            audioFiles: [],
          });
        }

        const dispatcherData = dispatcherMap.get(dispatcherName)!;

        // Categorize files based on extension
        if (fileExtension === ".json") {
          dispatcherData.transcriptFiles.push(file);
        } else {
          dispatcherData.audioFiles.push(file);
        }
      }
    });

    // Get existing dispatchers from localStorage
    const storedDispatchers = localStorage.getItem("dispatchers");
    const existingDispatchers: Dispatcher[] = storedDispatchers
      ? JSON.parse(storedDispatchers)
      : [];

    dispatcherMap.forEach((files, dispatcherName) => {
      // Check if dispatcher already exists
      const existingDispatcher = existingDispatchers.find(
        (d) => d.name === dispatcherName
      );

      if (existingDispatcher) {
        // Merge new files with existing files
        existingDispatcher.files.transcriptFiles.push(
          ...files.transcriptFiles.map((f) => f.name)
        );
        existingDispatcher.files.audioFiles.push(
          ...files.audioFiles.map((f) => f.name)
        );
      } else {
        // Create new dispatcher if it doesn't exist
        const newDispatcher: Dispatcher = {
          id: uuidv4(),
          name: dispatcherName,
          files: {
            transcriptFiles: files.transcriptFiles.map((f) => f.name),
            audioFiles: files.audioFiles.map((f) => f.name),
          },
        };
        existingDispatchers.push(newDispatcher);
      }
    });

    // Store updated dispatchers array in localStorage
    localStorage.setItem("dispatchers", JSON.stringify(existingDispatchers));
    console.log("Dispatchers stored in localStorage:", existingDispatchers);

    alert("Successfully stored dispatcher(s) with files!");

    // Clear selected files after successful upload
    setSelectedFiles([]);
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <div className="mb-4">
        <h2 className="text-xl font-semibold mb-2">
          Upload Zip and JSON Files
        </h2>
      </div>

      {/* Drag and Drop Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? "border-blue-500 bg-blue-50"
            : "border-gray-300 hover:border-gray-400"
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="space-y-2">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <p className="text-lg font-medium text-gray-700">
            Drop zip and json files here, or click to browse
          </p>
          <p className="text-sm text-gray-500">Zip and JSON files only</p>
        </div>
      </div>

      {/* Hidden File Input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".zip,.json"
        onChange={(e) => handleFileSelect(e.target.files)}
        className="hidden"
      />

      {/* Selected Files List */}
      {selectedFiles.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-medium mb-3">
            Selected Files ({selectedFiles.length})
          </h3>
          <div className="space-y-2 max-h-60 overflow-y-auto">
            {selectedFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex-1">
                  <p className="font-medium text-sm">{file.name}</p>
                  <p className="text-xs text-gray-500">
                    {formatFileSize(file.size)}
                  </p>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="text-red-500 hover:text-red-700 ml-2"
                >
                  <svg
                    className="h-5 w-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Upload Button */}
      <div className="mt-6">
        <button
          onClick={handleUpload}
          disabled={selectedFiles.length === 0}
          className={`w-full py-3 px-4 rounded-lg font-medium transition-colors ${
            selectedFiles.length === 0
              ? "bg-gray-300 text-gray-500 cursor-not-allowed"
              : "bg-blue-500 text-white hover:bg-blue-600"
          }`}
        >
          Upload{" "}
          {selectedFiles.length > 0
            ? `${selectedFiles.length} file(s)`
            : "Files"}
        </button>
      </div>
    </div>
  );
};

export default UploadFileContainer;
