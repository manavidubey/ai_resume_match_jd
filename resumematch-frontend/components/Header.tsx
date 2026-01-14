import React from 'react';

interface HeaderProps {
  title?: string;
  subtitle?: string;
}

const Header: React.FC<HeaderProps> = ({ title = "AI Resume Matcher", subtitle = "Intelligent candidate-job matching powered by NLP" }) => {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div>
            <h1 className="header-title">
              {title}
            </h1>
            <p className="header-subtitle">
              {subtitle}
            </p>
          </div>
          <div style={{display: 'flex', gap: '0.5rem'}}>
            <button
              type="button"
              className="btn btn-outline"
            >
              Help
            </button>
            <button
              type="button"
              className="btn btn-primary"
            >
              Dashboard
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;