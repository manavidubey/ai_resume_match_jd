# AI Resume Matcher

An intelligent resume matching system that uses AI and NLP to semantically match candidate resumes with job descriptions.

## Features

- **Semantic Matching**: Uses transformer-based embeddings to understand context and meaning rather than simple keyword matching
- **Multi-format Support**: Handles PDF and DOCX resume formats
- **Comprehensive Scoring**: Weighted scoring across skills, experience, role fit, and bonus signals
- **Visual Analytics**: Charts and graphs to visualize match results
- **Explainable AI**: Clear explanations of match decisions and recommendations
- **Scalable Architecture**: Built with FastAPI for backend and React for frontend

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Document Parsing**: PyMuPDF, python-docx
- **AI/NLP**: Sentence Transformers, spaCy
- **Embeddings**: Semantic similarity using cosine distance
- **Database**: PostgreSQL (for production), in-memory storage (for demo)

### Frontend
- **Framework**: React with Next.js
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Heroicons

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   AI/NLP        │
│   (React)       │◄──►│   (FastAPI)      │◄──►│   (Transformers)│
│                 │    │                  │    │                 │
│ - Upload UI     │    │ - API Endpoints  │    │ - Embeddings    │
│ - Job Form      │    │ - Document       │    │ - Semantic      │
│ - Visualizations│    │   Parsing        │    │   Matching      │
│ - Results       │    │ - Matching       │    │ - Scoring       │
└─────────────────┘    │   Engine         │    └─────────────────┘
                       └──────────────────┘
```

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd resumematch-backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install spaCy English model:
```bash
python -m spacy download en_core_web_sm
```

4. Run the backend server:
```bash
cd resumematch-backend
python -m uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd resumematch-frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

## Usage

1. Upload candidate resumes (PDF/DOCX) using the upload interface
2. Create a job posting with requirements and responsibilities
3. Run the matching algorithm to get ranked results
4. View detailed analytics and recommendations

## API Endpoints

- `POST /upload-resume/` - Upload and parse a resume
- `POST /jobs/` - Create a new job posting
- `GET /jobs/{job_id}` - Get job details
- `POST /match/{job_id}` - Run matching algorithm for a job
- `GET /matches/{job_id}` - Get match results for a job

## Scoring Algorithm

The system uses a weighted scoring approach:

- **Skills (40%)**: Coverage of required and preferred skills
- **Experience (30%)**: Relevance and duration of past experience
- **Role Fit (20%)**: Semantic similarity between resume and job description
- **Bonus Signals (10%)**: Certifications, leadership, achievements

## File Structure

```
resumematch-project1/
├── resumematch-backend/
│   ├── api/                 # API route definitions
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   ├── nlp/                 # NLP processing
│   ├── parsers/             # Document parsing
│   ├── utils/               # Utility functions
│   ├── config.py            # Configuration
│   ├── main.py              # Application entry point
│   └── requirements.txt     # Dependencies
└── resumematch-frontend/
    ├── components/          # React components
    ├── pages/              # Next.js pages
    ├── lib/                # API client
    ├── styles/             # Global styles
    ├── public/             # Static assets
    ├── package.json        # Frontend dependencies
    └── tailwind.config.js  # Tailwind CSS config
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
