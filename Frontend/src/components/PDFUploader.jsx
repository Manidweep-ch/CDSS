import { useState, useRef } from "react";
import axiosClient from "../api/axiosClient";
import "./PDFUploader.css";

function PDFUploader({ onExtractionComplete }) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileUpload = async (file) => {
    if (!file) return;
    
    if (!file.name.endsWith('.pdf')) {
      setError("Please upload a PDF file");
      return;
    }

    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      setError("File size must be less than 10MB");
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axiosClient.post("/pdf/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      onExtractionComplete(response.data);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || "PDF upload failed. Please try again.";
      setError(errorMsg);
      console.error("PDF upload error:", err);
    } finally {
      setUploading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="pdf-uploader">
      <div className="uploader-header">
        <h3>Upload Lab Report</h3>
        <p>Upload a PDF file containing your medical test results</p>
      </div>

      <div 
        className={`upload-zone ${dragActive ? 'drag-active' : ''} ${uploading ? 'uploading' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => !uploading && fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={(e) => handleFileUpload(e.target.files[0])}
          disabled={uploading}
          style={{ display: 'none' }}
        />

        {uploading ? (
          <div className="upload-status">
            <div className="spinner-large"></div>
            <h4>Processing PDF...</h4>
            <p>Extracting medical data from your report</p>
          </div>
        ) : (
          <div className="upload-prompt">
            <div className="upload-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
            </div>
            <h4>Drop your PDF here or click to browse</h4>
            <p>Maximum file size: 10MB</p>
            <button type="button" className="btn-upload">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              Choose File
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="upload-error slide-in">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
          {error}
        </div>
      )}

      <div className="upload-info">
        <div className="info-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span>Diabetes Panel</span>
        </div>
        <div className="info-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span>Cardiovascular Panel</span>
        </div>
        <div className="info-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span>Kidney Function Panel</span>
        </div>
      </div>
    </div>
  );
}

export default PDFUploader;
