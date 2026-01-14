import React, { useState } from 'react';

interface UploadAreaProps {
  onFileUpload: (files: File[]) => void;
}

const UploadArea: React.FC<UploadAreaProps> = ({ onFileUpload }) => {
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files.length > 0) {
      const filesArray = Array.from(e.target.files);
      const validFiles = filesArray.filter(file => 
        file.type === 'application/pdf' || 
        file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
        file.name.endsWith('.docx') || file.name.endsWith('.doc')
      );
      
      if (validFiles.length > 0) {
        setUploadedFiles(prev => [...prev, ...validFiles]);
        onFileUpload(validFiles);
      }
    }
  };

  return (
    <div style={{marginBottom: '1.5rem'}}>
      <div className="upload-area" onClick={() => document.getElementById('file-upload')?.click()}>
        <input
          type="file"
          id="file-upload"
          className="hidden"
          multiple
          accept=".pdf,.docx,.doc"
          onChange={handleChange}
        />
        <svg
          className="upload-icon"
          stroke="currentColor"
          fill="none"
          viewBox="0 0 48 48"
        >
          <path
            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        <h3 className="upload-title">
          Upload resumes
        </h3>
        <p className="upload-text">
          PDF, DOCX, or DOC up to 16MB
        </p>
        <p className="upload-text">
          <span className="upload-link">Click to browse</span> or drag and drop
        </p>
      </div>
      
      {uploadedFiles.length > 0 && (
        <div className="upload-files">
          <ul style={{listStyle: 'none', padding: 0, margin: 0}}>
            {uploadedFiles.map((file, index) => (
              <li key={index}>
                <div className="file-item">
                  <div className="file-info">
                    <span className="file-indicator"></span>
                    <p className="file-name">
                      {file.name}
                    </p>
                  </div>
                  <span className="file-status">
                    Ready
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default UploadArea;
