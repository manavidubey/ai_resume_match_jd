import React, { useState } from 'react';
import Header from '../components/Header';
import UploadArea from '../components/UploadArea';
import CandidateList from '../components/CandidateList';
import MatchVisualization from '../components/MatchVisualization';
import { resumeApi } from '../lib/api';

const HomePage = () => {
  const [activeTab, setActiveTab] = useState<'all'>('all');
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [jobDescriptionSubmitted, setJobDescriptionSubmitted] = useState(false);
  const [matchResults, setMatchResults] = useState<any[]>([]);
  const [matchHistory, setMatchHistory] = useState<any[]>([]);
  const [currentMatchExplanation, setCurrentMatchExplanation] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);

  const handleFileUpload = async (files: File[]) => {
    setIsLoading(true);
    try {
      for (const file of files) {
        await resumeApi.uploadResume(file);
        setUploadedFiles(prev => [...prev, file]);
      }
      alert(`Successfully uploaded ${files.length} resume(s)`);
    } catch (error) {
      console.error('Error uploading files:', error);
      alert('Error uploading files. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleJobDescriptionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      // Create a job object with just the description
      const jobData = {
        title: 'Position',
        description: jobDescription,
        requirements: jobDescription,
        responsibilities: jobDescription,
        skills_required: [],
        skills_preferred: []
      };
      
      const response = await resumeApi.createJob(jobData);
      setJobId(response.data.id);
      setJobDescriptionSubmitted(true);
      
      // Automatically run matching algorithm after job submission
      const matchResponse = await resumeApi.runMatching(response.data.id);
      
      // Store previous results in history
      if (matchResults.length > 0) {
        setMatchHistory(prev => [matchResults[0], ...prev]); // Store the first/top result
      }
      
      setMatchResults(matchResponse.data);
      
      // Get explanation for the top match if available
      if (matchResponse.data && matchResponse.data.length > 0) {
        const topMatch = matchResponse.data[0];
        // Access explanation from the nested match_analysis object
        const explanation = topMatch.match_analysis?.explanation || topMatch.explanation || 'Detailed explanation of the match will be shown here.';
        setCurrentMatchExplanation(explanation);
      }
      
      alert('Job description submitted and matching completed successfully!');
    } catch (error) {
      console.error('Error submitting job description:', error);
      alert('Error submitting job description. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRunMatching = async () => {
    if (!jobId) {
      alert('Please enter a job description first');
      return;
    }
    
    setIsLoading(true);
    try {
      const response = await resumeApi.runMatching(jobId);
      setMatchResults(response.data);
    } catch (error) {
      console.error('Error running matching:', error);
      alert('Error running matching algorithm. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{minHeight: '100vh', background: 'linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%)'}}>
      <Header />
      
      <main className="main">
        <div className="container">
          <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2rem'}}>
            <div>
              <h2 style={{fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--dark)', marginBottom: '0.25rem'}}>
                AI Resume Matcher
              </h2>
              <p style={{fontSize: '0.875rem', color: 'var(--gray)'}}>
                Upload resumes and job descriptions to find the best matches using AI-powered semantic analysis
              </p>
            </div>
          </div>

          {/* Single Page Layout with All Components */}
          <div style={{marginTop: '1.5rem'}}>
            {/* Upload Section */}
            <div className="card" style={{marginBottom: '1.5rem'}}>
              <div style={{display: 'grid', gridTemplateColumns: '1fr', gap: '1.5rem'}}>
                <div>
                  <h3 style={{fontSize: '1.125rem', fontWeight: '500', color: 'var(--dark)', marginBottom: '0.5rem'}}>Upload Resumes</h3>
                  <p style={{fontSize: '0.875rem', color: 'var(--gray)'}}>
                    Upload candidate resumes in PDF or DOCX format for analysis.
                  </p>
                </div>
                <div style={{marginTop: '1.25rem'}}>
                  <UploadArea onFileUpload={handleFileUpload} />
                </div>
              </div>
            </div>
            
            {/* Job Description Section */}
            <div className="card" style={{marginBottom: '1.5rem'}}>
              <div style={{display: 'grid', gridTemplateColumns: '1fr', gap: '1.5rem'}}>
                <div>
                  <h3 style={{fontSize: '1.125rem', fontWeight: '500', color: 'var(--dark)', marginBottom: '0.5rem'}}>Enter Job Description</h3>
                  <p style={{fontSize: '0.875rem', color: 'var(--gray)'}}>
                    Enter the job description to match against uploaded resumes.
                  </p>
                </div>
                <div style={{marginTop: '1.25rem'}}>
                  <form onSubmit={handleJobDescriptionSubmit}>
                    <div style={{marginBottom: '1rem'}}>
                      <label htmlFor="jobDescription" style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', color: 'var(--dark)', marginBottom: '0.5rem'}}>
                        Job Description
                      </label>
                      <textarea
                        id="jobDescription"
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        placeholder="Enter job description, requirements, and responsibilities..."
                        rows={6}
                        style={{
                          width: '100%',
                          padding: '0.75rem',
                          border: '1px solid var(--border)',
                          borderRadius: '0.5rem',
                          fontSize: '0.875rem',
                          resize: 'vertical',
                          minHeight: '120px',
                          background: 'var(--light)',
                          color: 'var(--dark)'
                        }}
                        required
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={isLoading || !jobDescription.trim()}
                      className="btn btn-primary"
                    >
                      {isLoading ? (
                        <>
                          <span className="spinner"></span>
                          Processing...
                        </>
                      ) : 'Submit & Match'}
                    </button>
                  </form>
                </div>
              </div>
            </div>
            
            {/* Results Section */}
            <div>
              {!matchResults.length ? (
                <div className="card">
                  <div className="results-empty">
                    <svg
                      className="results-icon"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                    <h3 className="results-title">No matching results</h3>
                    <p className="results-text">
                      Upload resumes and enter a job description to see matching results.
                    </p>
                    <div style={{marginTop: '1.5rem'}}>
                      <button
                        type="button"
                        onClick={handleRunMatching}
                        disabled={isLoading || !jobId}
                        className="btn btn-primary"
                      >
                        {isLoading ? (
                          <>
                            <span className="spinner"></span>
                            Processing...
                          </>
                        ) : 'Re-run Matching Algorithm'}
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                <div style={{display: 'flex', flexDirection: 'column', gap: '1.5rem'}}>
                  {/* Latest Match at the Top */}
                  <div className="card">
                    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
                      <h3 style={{fontSize: '1.125rem', fontWeight: '500', color: 'var(--dark)'}}>Latest Match Results</h3>
                      <button
                        type="button"
                        onClick={handleRunMatching}
                        disabled={isLoading}
                        className="btn btn-outline"
                      >
                        Re-run Analysis
                      </button>
                    </div>
                    
                    <div style={{marginTop: '1rem'}}>
                      <MatchVisualization matchData={matchResults.slice(0, 5)} />
                    </div>
                    
                    {/* Explanation for Current Match */}
                    <div style={{marginTop: '1.5rem', padding: '1rem', background: 'var(--light)', borderRadius: '0.5rem'}}>
                      <h4 style={{fontWeight: '500', color: 'var(--dark)', marginBottom: '0.5rem'}}>Why This Match Occurred</h4>
                      <p style={{color: 'var(--gray)', lineHeight: '1.5'}}>{currentMatchExplanation}</p>
                    </div>
                  </div>
                  
                  {/* Top Candidate Ranking */}
                  <div className="card">
                    <h3 style={{fontSize: '1.125rem', fontWeight: '500', color: 'var(--dark)', marginBottom: '1rem'}}>Top Candidate</h3>
                    <CandidateList candidates={matchResults.slice(0, 1)} />
                  </div>
                  
                  {/* Previous Matches */}
                  {matchHistory.length > 0 && (
                    <div className="card">
                      <h3 style={{fontSize: '1.125rem', fontWeight: '500', color: 'var(--dark)', marginBottom: '1rem'}}>Previous Matches</h3>
                      <CandidateList candidates={matchHistory} />
                    </div>
                  )}
                  
                  {/* All Other Candidates */}
                  {matchResults.length > 1 && (
                    <div className="card">
                      <h3 style={{fontSize: '1.125rem', fontWeight: '500', color: 'var(--dark)', marginBottom: '1rem'}}>Other Candidates</h3>
                      <CandidateList candidates={matchResults.slice(1)} />
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default HomePage;