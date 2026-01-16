# AI Resume Matcher

An advanced AI-powered platform that semantically matches candidate resumes with job descriptions using modern NLP and transformer models.

## Features

- **Advanced AI Matching**: Uses multiple transformer models (GPT-2, Sentence Transformers, Qwen2.5-3B-Instruct) for semantic analysis
- **Detailed Explanations**: Provides comprehensive explanations of why matches occur
- **Skills Gap Analysis**: Identifies missing skills and suggests improvements
- **Visualizations**: Interactive charts showing match scores and candidate rankings
- **Multi-Format Support**: Handles PDF and DOCX resume uploads

## Architecture

- **Frontend**: Next.js/React with aesthetic CSS styling
- **Backend**: FastAPI with Python
- **AI Models**: Hugging Face Transformers integration
- **NLP**: spaCy for skill and experience extraction

## Deployment Instructions

### Backend Deployment (e.g., on Render)

1. Deploy the backend service to a cloud provider like Render:
   - Create a new web service
   - Use the `resumematch-backend` directory
   - Use the provided Dockerfile
   - Set up requirements from `requirements.txt`
   - Expose port 8000
   - Note the deployment URL

### Frontend Deployment (on Vercel)

1. Fork this repository
2. Connect to Vercel
3. Set environment variable in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL` = [your backend deployment URL]
4. Deploy the frontend

### Environment Variables

- `NEXT_PUBLIC_API_URL`: URL of your deployed backend service

## Local Development

### Backend
```bash
cd resumematch-backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd resumematch-frontend
npm install
npm run dev
```

## API Endpoints

- `POST /upload-resume/`: Upload and parse resume files
- `POST /jobs/`: Create job postings
- `POST /match/{job_id}`: Run matching algorithm
- `GET /matches/{job_id}`: Get match results

## Technology Stack

- **Frontend**: Next.js, React, TypeScript, Recharts
- **Backend**: Python, FastAPI, Pydantic
- **AI/ML**: Transformers, Sentence Transformers, spaCy, PyTorch
- **Models**: GPT-2, Sentence Transformers, Qwen2.5-3B-Instruct

## How It Works

1. Upload resumes in PDF or DOCX format
2. Enter job description
3. System automatically matches resumes to job requirements
4. View detailed match scores and explanations
5. Get recommendations for improving matches

## Troubleshooting Vercel Deployment

If you encounter 404 errors on Vercel:
1. Make sure you've set the NEXT_PUBLIC_API_URL environment variable
2. The frontend needs to communicate with the deployed backend API
3. Check that your backend is deployed and accessible
4. Verify CORS settings in the backend

## License

MIT
