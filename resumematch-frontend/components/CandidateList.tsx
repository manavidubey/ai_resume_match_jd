import React from 'react';

interface CandidateListProps {
  candidates: any[];
  onSelectCandidate?: (candidate: any) => void;
}

const CandidateList: React.FC<CandidateListProps> = ({ candidates, onSelectCandidate }) => {
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-100';
    if (score >= 0.6) return 'text-yellow-600 bg-yellow-100';
    if (score >= 0.4) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreClass = (score: number) => {
    if (score >= 0.8) return 'score-excellent';
    if (score >= 0.6) return 'score-good';
    if (score >= 0.4) return 'score-fair';
    return 'score-poor';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 0.8) return 'Excellent';
    if (score >= 0.6) return 'Good';
    if (score >= 0.4) return 'Fair';
    return 'Poor';
  };

  return (
    <div className="candidate-list">
      <ul style={{listStyle: 'none', padding: 0, margin: 0}}>
        {candidates.map((candidate, index) => {
          const overallScore = candidate.match_analysis?.match_score?.overall_score || 0;
          const skillsScore = candidate.match_analysis?.match_score?.skills_score || 0;
          const experienceScore = candidate.match_analysis?.match_score?.experience_score || 0;
          
          return (
            <li key={index} onClick={() => onSelectCandidate && onSelectCandidate(candidate)}>
              <div className="candidate-item">
                <div className="candidate-header">
                  <div className="candidate-name">
                    Candidate {index + 1}
                  </div>
                  <div>
                    <span className={`score-badge ${getScoreClass(overallScore)}`}>
                      {getScoreLabel(overallScore)} ({(overallScore * 100).toFixed(1)}%)
                    </span>
                  </div>
                </div>
                <div className="candidate-details">
                  <div className="detail-item">
                    <svg className="detail-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                    </svg>
                    Skills: {(skillsScore * 100).toFixed(1)}%
                  </div>
                  <div className="detail-item">
                    <svg className="detail-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clipRule="evenodd" />
                      <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A7.99 7.99 0 0010 10c-4.411 0-8 3.589-8 8z" />
                    </svg>
                    Experience: {(experienceScore * 100).toFixed(1)}%
                  </div>
                  <div className="detail-item">
                    <svg className="detail-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                    </svg>
                    <span>Matched Skills: {candidate.match_analysis?.matched_skills?.length || 0}</span>
                  </div>
                </div>
                <div style={{marginTop: '0.5rem'}}>
                  <p style={{fontSize: '0.875rem', color: '#4b5563'}}>
                    <span style={{color: '#6b7280'}}>Recommendation:</span> {candidate.match_analysis?.role_recommendation || 'No recommendation available'}
                  </p>
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default CandidateList;
